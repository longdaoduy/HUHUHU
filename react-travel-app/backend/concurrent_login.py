"""
Login Manager Module - Hỗ trợ xử lý đồng thời (Concurrent) cho nhiều người dùng
Sử dụng threading locks để đảm bảo thread-safety khi đọc/ghi dữ liệu user
"""

import json
import os
import hashlib
from threading import Lock
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConcurrentLoginManager:
    """
    Quản lý đăng nhập với hỗ trợ xử lý đồng thời
    - Thread-safe file operations
    - Connection pooling concept
    - Rate limiting per user
    """
    
    def __init__(self, users_file: str = "Users.json", max_concurrent_users: int = 100):
        self.users_file = users_file
        self.max_concurrent_users = max_concurrent_users
        
        # Thread locks để đảm bảo thread-safety
        self._file_lock = Lock()  # Lock cho file operations
        self._cache_lock = Lock()  # Lock cho in-memory cache
        self._login_attempts_lock = Lock()  # Lock cho login attempts tracking
        
        # In-memory cache để giảm I/O
        self._users_cache: Dict = {}
        self._cache_timestamp = 0
        self._cache_ttl = 300  # Cache hết hạn sau 5 phút
        
        # Rate limiting - theo dõi login attempts
        self._login_attempts: Dict[str, List[datetime]] = {}
        self._max_login_attempts = 5
        self._login_attempt_window = 300  # 5 phút
        
        # Active sessions
        self._active_sessions: Dict[str, Dict] = {}
        self._session_lock = Lock()
        
        logger.info(f"ConcurrentLoginManager initialized with max_concurrent_users={max_concurrent_users}")
    
    def _hash_password(self, password: str) -> str:
        """Mã hóa mật khẩu"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users_from_file(self) -> Dict:
        """Tải users từ file với thread-safety"""
        try:
            with self._file_lock:
                if not os.path.exists(self.users_file):
                    logger.warning(f"Users file not found: {self.users_file}")
                    return {"users": []}
                
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data.get('users', []))} users from file")
                    return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {"users": []}
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return {"users": []}
    
    def _save_users_to_file(self, data: Dict) -> bool:
        """Lưu users vào file với thread-safety"""
        try:
            with self._file_lock:
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    logger.info(f"Saved {len(data.get('users', []))} users to file")
                    return True
        except Exception as e:
            logger.error(f"Error saving users: {e}")
            return False
    
    def get_users_cached(self) -> Dict:
        """Lấy users với caching để giảm I/O"""
        with self._cache_lock:
            current_time = datetime.now().timestamp()
            
            # Nếu cache còn hợp lệ, trả về cache
            if self._users_cache and (current_time - self._cache_timestamp) < self._cache_ttl:
                logger.info("Returning users from cache")
                return self._users_cache.copy()
        
        # Cache hết hạn hoặc trống, load từ file
        data = self._load_users_from_file()
        
        with self._cache_lock:
            self._users_cache = data.copy()
            self._cache_timestamp = datetime.now().timestamp()
        
        return data
    
    def _invalidate_cache(self):
        """Xóa cache khi có thay đổi"""
        with self._cache_lock:
            self._users_cache = {}
            self._cache_timestamp = 0
    
    def _check_rate_limit(self, username: str) -> Tuple[bool, str]:
        """Kiểm tra rate limiting cho login attempts"""
        with self._login_attempts_lock:
            current_time = datetime.now()
            
            # Nếu chưa có attempts, tạo mới
            if username not in self._login_attempts:
                self._login_attempts[username] = []
            
            # Loại bỏ các attempts quá cũ
            attempts = self._login_attempts[username]
            self._login_attempts[username] = [
                attempt_time for attempt_time in attempts
                if (current_time - attempt_time).total_seconds() < self._login_attempt_window
            ]
            
            # Kiểm tra số lần attempts
            if len(self._login_attempts[username]) >= self._max_login_attempts:
                return False, f"Quá nhiều lần đăng nhập sai. Vui lòng thử lại sau {self._login_attempt_window} giây."
            
            return True, ""
    
    def _record_login_attempt(self, username: str):
        """Ghi lại login attempt"""
        with self._login_attempts_lock:
            if username not in self._login_attempts:
                self._login_attempts[username] = []
            self._login_attempts[username].append(datetime.now())
    
    def _clear_login_attempts(self, username: str):
        """Xóa login attempts khi đăng nhập thành công"""
        with self._login_attempts_lock:
            if username in self._login_attempts:
                del self._login_attempts[username]
    
    def register_user(self, name: str, username: str, password: str, email: str = "") -> Tuple[bool, str]:
        """
        Đăng ký user mới với thread-safety
        """
        # Validate input
        if not all([name, username, password]):
            return False, "Vui lòng nhập đầy đủ thông tin"
        
        if len(password) < 6:
            return False, "Mật khẩu phải ít nhất 6 ký tự"
        
        # Load users
        data = self.get_users_cached()
        users = data.get("users", [])
        
        # Kiểm tra username đã tồn tại
        if any(u["username"] == username for u in users):
            return False, "Tên đăng nhập đã tồn tại"
        
        # Thêm user mới
        new_user = {
            "name": name,
            "username": username,
            "email": email,
            "password": self._hash_password(password),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "status": "active"
        }
        
        users.append(new_user)
        data["users"] = users
        
        # Lưu file và invalidate cache
        if self._save_users_to_file(data):
            self._invalidate_cache()
            logger.info(f"User registered successfully: {username}")
            return True, "Đăng ký thành công"
        else:
            return False, "Lỗi khi lưu dữ liệu"
    
    def login_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Đăng nhập user với hỗ trợ concurrent
        """
        # Strip whitespace from inputs
        username = username.strip() if username else ""
        password = password.strip() if password else ""
        
        logger.info(f"🔍 Login attempt - Username: '{username}', Password length: {len(password)}")
        logger.info(f"🔍 Password first/last chars: '{password[0] if password else 'EMPTY'}' / '{password[-1] if password else 'EMPTY'}'")
        
        # Kiểm tra rate limit
        allowed, message = self._check_rate_limit(username)
        if not allowed:
            return False, message, None
        
        # Load users (có thể từ cache)
        data = self.get_users_cached()
        users = data.get("users", [])
        
        logger.info(f"🔍 Total users in database: {len(users)}")
        
        # Tìm user theo username HOẶC email
        user = next((u for u in users if u.get("username") == username or u.get("email") == username or (u.get("email", "").split("@")[0] == username)), None)
        
        if not user:
            logger.warning(f"❌ User not found: '{username}'")
            self._record_login_attempt(username)
            return False, "Tài khoản không tồn tại", None
        
        logger.info(f"✅ User found: {user.get('email')} (username: {user.get('username')})")
        
        # Kiểm tra mật khẩu
        hashed_password = self._hash_password(password)
        logger.info(f"🔐 Password comparison:")
        logger.info(f"   Stored hash: {user['password']}")
        logger.info(f"   Input hash:  {hashed_password}")
        logger.info(f"   Match: {user['password'] == hashed_password}")
        if user["password"] != hashed_password:
            self._record_login_attempt(username)
            return False, "Mật khẩu không chính xác", None
        
        # Kiểm tra trạng thái account
        if user.get("status") != "active":
            return False, "Tài khoản đã bị khóa", None
        
        # Đăng nhập thành công
        self._clear_login_attempts(username)
        
        # Cập nhật last_login
        user["last_login"] = datetime.now().isoformat()
        if self._save_users_to_file(data):
            self._invalidate_cache()
        
        # Tạo session
        session_info = {
            "username": username,
            "name": user.get("name"),
            "email": user.get("email"),
            "login_time": datetime.now(),
            "last_activity": datetime.now()
        }
        
        with self._session_lock:
            # Kiểm tra active sessions
            if len(self._active_sessions) >= self.max_concurrent_users:
                # Loại bỏ session cũ nhất
                oldest_session = min(
                    self._active_sessions.items(),
                    key=lambda x: x[1]["login_time"]
                )
                del self._active_sessions[oldest_session[0]]
                logger.warning(f"Removed oldest session: {oldest_session[0]}")
            
            self._active_sessions[username] = session_info
        
        logger.info(f"User logged in successfully: {username}")
        return True, "Đăng nhập thành công", {
            "username": username,
            "name": user.get("name"),
            "email": user.get("email")
        }
    
    def logout_user(self, username: str) -> bool:
        """Đăng xuất user"""
        with self._session_lock:
            if username in self._active_sessions:
                del self._active_sessions[username]
                logger.info(f"User logged out: {username}")
                return True
        return False
    
    def get_active_sessions_count(self) -> int:
        """Lấy số lượng active sessions"""
        with self._session_lock:
            return len(self._active_sessions)
    
    def get_active_sessions(self) -> List[str]:
        """Lấy danh sách active sessions"""
        with self._session_lock:
            return list(self._active_sessions.keys())
    
    def is_user_online(self, username: str) -> bool:
        """Kiểm tra user có online không"""
        with self._session_lock:
            return username in self._active_sessions
    
    def update_user_activity(self, username: str):
        """Cập nhật last_activity của user"""
        with self._session_lock:
            if username in self._active_sessions:
                self._active_sessions[username]["last_activity"] = datetime.now()
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Lấy thông tin user"""
        data = self.get_users_cached()
        users = data.get("users", [])
        user = next((u for u in users if u["username"] == username), None)
        
        if user:
            # Không trả về password hash
            user_info = user.copy()
            del user_info["password"]
            return user_info
        
        return None
    
    def update_user_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Thay đổi mật khẩu user"""
        if len(new_password) < 6:
            return False, "Mật khẩu phải ít nhất 6 ký tự"
        
        data = self.get_users_cached()
        users = data.get("users", [])
        user = next((u for u in users if u["username"] == username), None)
        
        if not user:
            return False, "User không tồn tại"
        
        # Kiểm tra old password
        if user["password"] != self._hash_password(old_password):
            return False, "Mật khẩu cũ không chính xác"
        
        # Cập nhật password
        user["password"] = self._hash_password(new_password)
        
        if self._save_users_to_file(data):
            self._invalidate_cache()
            logger.info(f"Password updated for user: {username}")
            return True, "Cập nhật mật khẩu thành công"
        else:
            return False, "Lỗi khi cập nhật mật khẩu"
    
    def get_statistics(self) -> Dict:
        """Lấy thống kê"""
        data = self.get_users_cached()
        users = data.get("users", [])
        active_count = self.get_active_sessions_count()
        
        return {
            "total_users": len(users),
            "active_sessions": active_count,
            "max_concurrent_users": self.max_concurrent_users,
            "cache_status": "valid" if self._users_cache else "invalid"
        }


# Global instance
login_manager = ConcurrentLoginManager(max_concurrent_users=100)
