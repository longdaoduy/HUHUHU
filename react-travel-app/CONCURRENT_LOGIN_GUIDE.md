# 🔄 Concurrent Login System - Hỗ Trợ Xử Lý Song Song

## 📋 Giới Thiệu

Phần xử lý đăng nhập đã được cải thiện để hỗ trợ **xử lý song song (concurrent)** cho nhiều người dùng cùng lúc. Điều này cho phép ứng dụng:

- ✅ Xử lý nhiều login requests cùng lúc
- ✅ Quản lý session của nhiều user
- ✅ Áp dụng rate limiting per user
- ✅ Caching dữ liệu để giảm I/O
- ✅ Thread-safe file operations

## 🏗️ Kiến Trúc

### Module: `concurrent_login.py`

```
ConcurrentLoginManager
├── Thread Locks (Thread-Safety)
│   ├── _file_lock - Bảo vệ file operations
│   ├── _cache_lock - Bảo vệ in-memory cache
│   ├── _login_attempts_lock - Bảo vệ login attempts tracking
│   └── _session_lock - Bảo vệ active sessions
│
├── Features
│   ├── User Registration (thread-safe)
│   ├── User Login (with rate limiting)
│   ├── Session Management
│   ├── In-Memory Caching (TTL: 5 phút)
│   ├── Rate Limiting (5 attempts / 5 phút)
│   └── Activity Tracking
│
└── Max Concurrent Users: 100
```

## 🚀 Tính Năng Chính

### 1. Thread-Safe Operations

**Lock Mechanism:**
```python
# File operations được bảo vệ bởi _file_lock
with self._file_lock:
    # Đọc/ghi file Users.json
    ...

# Cache được bảo vệ bởi _cache_lock
with self._cache_lock:
    # Truy cập in-memory cache
    ...
```

### 2. In-Memory Caching

- **Cache TTL**: 5 phút (300 giây)
- **Lợi ích**: Giảm I/O, tăng speed
- **Auto-invalidate**: Khi có thay đổi

```python
# Lần đầu: load từ file
users = login_manager.get_users_cached()

# Lần 2-5 phút tiếp theo: load từ cache
users = login_manager.get_users_cached()

# Sau 5 phút: load lại từ file
users = login_manager.get_users_cached()
```

### 3. Rate Limiting

**Ngăn chặn Brute Force Attack:**
- Max 5 login attempts
- Trong 5 phút
- Tự động reset sau khung thời gian

```python
# Attempt 1-4: OK
# Attempt 5: Được
# Attempt 6: ❌ "Quá nhiều lần đăng nhập sai"
```

### 4. Session Management

- Max 100 concurrent sessions
- Tự động remove session cũ nhất
- Track login time & last activity

## 📡 API Endpoints

### Authentication Endpoints

#### 1. Register (Đăng Ký)
```http
POST /api/register
Content-Type: application/json

{
    "fullname": "Nguyễn Văn A",
    "email": "user@example.com",
    "password": "password123",
    "phone": "0123456789"
}

Response:
{
    "success": true,
    "message": "Đăng ký thành công",
    "user": {...}
}
```

#### 2. Login (Đăng Nhập)
```http
POST /api/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

Response:
{
    "success": true,
    "message": "Đăng nhập thành công",
    "token": "eyJhbGc...",
    "user": {
        "username": "user",
        "name": "Nguyễn Văn A",
        "email": "user@example.com"
    }
}
```

#### 3. Logout (Đăng Xuất)
```http
POST /api/logout
Authorization: Bearer <token>

Response:
{
    "success": true,
    "message": "Đăng xuất thành công"
}
```

### User Management Endpoints

#### 4. Get Active Sessions
```http
GET /api/users/active-sessions

Response:
{
    "status": "success",
    "count": 5,
    "sessions": ["user1", "user2", "user3", "user4", "user5"]
}
```

#### 5. Get User Statistics
```http
GET /api/users/stats

Response:
{
    "status": "success",
    "data": {
        "total_users": 150,
        "active_sessions": 25,
        "max_concurrent_users": 100,
        "cache_status": "valid"
    }
}
```

#### 6. Check User Online
```http
GET /api/users/is-online/{username}

Response:
{
    "status": "success",
    "username": "user1",
    "is_online": true
}
```

#### 7. Update User Activity
```http
POST /api/users/update-activity/{username}

Response:
{
    "status": "success",
    "message": "Activity updated"
}
```

## 🔒 Thread Safety Mechanism

### Scenario: 2 Users Login Cùng Lúc

```
User 1 Thread              User 2 Thread
│                          │
├─ Acquire _file_lock      │ (Chờ _file_lock)
│  Read Users.json         │
│  Verify password         │
│  ✓ Success               │
│                          ├─ Acquire _file_lock
├─ Release _file_lock      │  Read Users.json
│                          │  Verify password
│                          │  ✓ Success
│                          │
│                          ├─ Release _file_lock
│                          │
└─ Session Created         └─ Session Created
```

## 💾 Caching Strategy

### Cache Lifecycle

```
Request 1 (T=0s)
├─ Cache miss → Load from file
├─ Store in memory
└─ Return data

Request 2-N (T=1-299s)
├─ Cache hit → Return from memory
└─ Zero file I/O

Request M (T=301s)
├─ Cache expired → Load from file again
├─ Update cache
└─ Return data
```

## 🛡️ Security Features

### 1. Password Hashing
```python
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

### 2. Rate Limiting
- Ngăn brute force attacks
- Log attempts
- Auto-lockout

### 3. Session Management
- Unique session per user
- Activity tracking
- Auto-cleanup old sessions

## 📊 Performance Metrics

### Benchmark (Hypothetical)

| Scenario | Time | Improvement |
|----------|------|------------|
| Single user login | 50ms | - |
| 10 concurrent logins | 55ms | 90% throughput |
| 50 concurrent logins | 100ms | 50% per-user |
| 100 concurrent logins | 150ms | 33% per-user |

### Memory Usage

| Metric | Value |
|--------|-------|
| Cache size (per 100 users) | ~50KB |
| Session per user | ~1KB |
| Max memory (100 users) | ~150KB |

## 🔧 Configuration

### Thay đổi Max Concurrent Users

File: `backend/concurrent_login.py`

```python
# Mặc định: 100
login_manager = ConcurrentLoginManager(max_concurrent_users=100)

# Thay đổi thành:
login_manager = ConcurrentLoginManager(max_concurrent_users=500)
```

### Thay đổi Cache TTL

```python
# Line 30 trong concurrent_login.py
self._cache_ttl = 300  # Mặc định 5 phút

# Thay đổi thành:
self._cache_ttl = 600  # 10 phút
```

### Thay đổi Rate Limit

```python
# Line 32-33 trong concurrent_login.py
self._max_login_attempts = 5  # Mặc định
self._login_attempt_window = 300  # 5 phút

# Thay đổi thành:
self._max_login_attempts = 3  # Chặt chẽ hơn
self._login_attempt_window = 600  # 10 phút
```

## 📝 Example Usage

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/register", json={
    "fullname": "Nguyen Van A",
    "email": "user@example.com",
    "password": "password123",
    "phone": "0123456789"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/login", json={
    "email": "user@example.com",
    "password": "password123"
})
data = response.json()
token = data["token"]

# Get active sessions
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/users/active-sessions", headers=headers)
print(response.json())

# Logout
response = requests.post(f"{BASE_URL}/logout", headers=headers)
print(response.json())
```

### JavaScript/Frontend

```javascript
const API_URL = "http://localhost:8000/api";

// Register
async function register(name, email, password) {
    const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            fullname: name,
            email: email,
            password: password
        })
    });
    return response.json();
}

// Login
async function login(email, password) {
    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email,
            password: password
        })
    });
    const data = response.json();
    localStorage.setItem("token", data.token);
    return data;
}

// Get active sessions
async function getActiveSessions() {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_URL}/users/active-sessions`, {
        headers: {"Authorization": `Bearer ${token}`}
    });
    return response.json();
}
```

## 🐛 Troubleshooting

### Issue: "Quá nhiều lần đăng nhập sai"

**Nguyên nhân**: Login sai password 5 lần trong 5 phút

**Giải pháp**: 
1. Đợi 5 phút
2. Hoặc reset password

### Issue: Session đầy (100/100)

**Nguyên nhân**: Đạt giới hạn concurrent users

**Giải pháp**:
1. Tăng max concurrent users
2. Hoặc logout users cũ

### Issue: Cache không update

**Nguyên nhân**: Cache TTL chưa hết, dữ liệu stale

**Giải pháp**:
1. Chờ 5 phút
2. Hoặc restart server

## 📚 Tài Liệu Thêm

- **Thread Safety**: https://docs.python.org/3/library/threading.html
- **FastAPI Concurrency**: https://fastapi.tiangolo.com/deployment/concepts/#concurrency
- **Password Hashing**: https://docs.python.org/3/library/hashlib.html

## 🎯 Tính Năng Tương Lai

- [ ] OAuth2/JWT refresh tokens
- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, Facebook)
- [ ] Session analytics dashboard
- [ ] Distributed session store (Redis)
- [ ] Load balancing support

---

**Được phát triển với ❤️ để hỗ trợ ứng dụng có lưu lượng cao**
