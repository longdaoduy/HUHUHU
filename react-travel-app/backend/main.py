from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import math
from io import BytesIO
import base64
from datetime import datetime, timedelta
from PIL import Image
import os
import hashlib
import jwt

# Import our modules
try:
    from recognize import (
        analyze_image, get_landmark_from_image, get_landmark_with_confidence,
        detect_location, OPENAI_ENABLED
    )
    from ai_recommend import recommend, loadDestination, ai_recommend
    from album_manager import (
        zip_album, create_album_item, filter_album_items, 
        group_items_by_landmark, sort_items_by_date, add_images_to_album,
        get_album_stats
    )
    from chatbot import TravelChatbot, chatbot_instance
    from concurrent_login import login_manager
    from social_feed import social_feed_manager
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback if modules not available
    def analyze_image(*args, **kwargs):
        return "Module not available"
    def get_landmark_from_image(*args, **kwargs):
        return "Module not available"
    def get_landmark_with_confidence(*args, **kwargs):
        return {"landmark": "Module not available", "description": "", "confidence": "low"}
    def detect_location(*args, **kwargs):
        return "Module not available"
    def recommend(*args, **kwargs):
        return []
    def loadDestination():
        return []
    def ai_recommend(*args, **kwargs):
        return "Module not available"
    def zip_album(*args, **kwargs):
        return None
    def create_album_item(*args, **kwargs):
        return {}
    def filter_album_items(*args, **kwargs):
        return []
    def group_items_by_landmark(*args, **kwargs):
        return {}
    def sort_items_by_date(*args, **kwargs):
        return []
    def add_images_to_album(*args, **kwargs):
        return 0, 0, []
    def get_album_stats(*args, **kwargs):
        return {}
    class TravelChatbot:
        pass
    chatbot_instance = None
    class ConcurrentLoginManager:
        pass
    login_manager = None
    OPENAI_ENABLED = False

app = FastAPI(title="Vietnam Travel App API")

# ===== Authentication Configuration =====
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
USERS_FILE = "Users.json"
USERS_ALBUM_FILE = "Users_album.json"
REVIEWS_FILE = "Reviews.json"
FAVORITES_FILE = "Favorites.json"

# ===== Helper Functions for User Management =====
def hash_password(password: str) -> str:
    """Mã hóa mật khẩu."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu."""
    return hash_password(plain_password) == hashed_password

def load_users() -> dict:
    """Tải danh sách người dùng từ file."""
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": []}

def save_users(data: dict):
    """Lưu danh sách người dùng vào file."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_user_albums(user_email: str) -> dict:
    """Tải album của người dùng theo email."""
    if not os.path.exists(USERS_ALBUM_FILE):
        return {}
    try:
        with open(USERS_ALBUM_FILE, "r", encoding="utf-8") as f:
            all_albums = json.load(f)
    except json.JSONDecodeError:
        return {}
    
    user_album = all_albums.get(user_email, {})
    loaded_albums = {}
    for album_name, items in user_album.items():
        loaded_albums[album_name] = []
        for item in items:
            new_item = item.copy()
            if 'bytes' in new_item and isinstance(new_item['bytes'], str):
                try:
                    decoded_bytes = base64.b64decode(new_item['bytes'])
                    new_item['bytes'] = decoded_bytes
                except:
                    new_item['bytes'] = None
            loaded_albums[album_name].append(new_item)
    
    return loaded_albums

def save_user_albums(user_email: str, user_albums: dict):
    """Lưu album của người dùng theo email."""
    if os.path.exists(USERS_ALBUM_FILE):
        try:
            with open(USERS_ALBUM_FILE, "r", encoding="utf-8") as f:
                all_albums_data = json.load(f)
        except json.JSONDecodeError:
            all_albums_data = {}
    else:
        all_albums_data = {}

    albums_to_save = {}
    for album_name, items in user_albums.items():
        albums_to_save[album_name] = []
        for item in items:
            new_item = item.copy()
            if 'bytes' in new_item and isinstance(new_item['bytes'], bytes):
                encoded_bytes = base64.b64encode(new_item['bytes']).decode('utf-8')
                new_item['bytes'] = encoded_bytes
            albums_to_save[album_name].append(new_item)

    all_albums_data[user_email] = albums_to_save
    with open(USERS_ALBUM_FILE, "w", encoding="utf-8") as f:
        json.dump(all_albums_data, f, indent=4, ensure_ascii=False)

def create_access_token(data: dict) -> str:
    """Tạo JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(authorization: str = Header(None)) -> str:
    """Kiểm tra JWT token và trả về email."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token không được cung cấp")
    
    try:
        # Extract token from "Bearer <token>"
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = parts[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Lấy email từ token
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email  # Trả về email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

def verify_token_from_string(token: str) -> str:
    """Kiểm tra JWT token từ string và trả về email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

def get_current_user_email(authorization: str = Header(None)) -> str:
    """Lấy email của user từ token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = parts[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Email được lưu trong "sub"
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== Pydantic Models =====
class RegisterRequest(BaseModel):
    fullname: str
    email: str
    password: str
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class InterestRequest(BaseModel):
    interest: str

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius: int = 50

class AlbumCreateRequest(BaseModel):
    name: str

class ReviewRequest(BaseModel):
    destination_name: str
    rating: int  # 1-5
    comment: str
    
class UserProfileUpdate(BaseModel):
    fullname: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserSettingsUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    language: Optional[str] = None
    theme: Optional[str] = None

class ChatbotMessageRequest(BaseModel):
    message: str
    use_ai: Optional[bool] = True

class ChatbotSearchRequest(BaseModel):
    tags: Optional[List[str]] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None

# Cấu hình CORS để cho phép frontend gọi API  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins trong development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory album storage
album_storage = {}

def haversine_distance(lat1, lon1, lat2, lon2):
    """Tính khoảng cách theo công thức haversine."""
    import math
    R = 6371.0  # Bán kính Trái Đất (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# API Routes

@app.get("/")
async def root():
    return {"message": "Vietnam Travel App API"}

# ===== Authentication Routes =====

@app.post("/api/register")
async def register(request: RegisterRequest):
    """Đăng ký tài khoản mới - Thread-safe với ConcurrentLoginManager."""
    try:
        # Sử dụng concurrent login manager
        if login_manager:
            success, message = login_manager.register_user(
                name=request.fullname,
                username=request.email.split("@")[0],
                password=request.password,
                email=request.email
            )
            
            if success:
                return {
                    "success": True,
                    "message": message,
                    "user": {
                        "email": request.email,
                        "fullname": request.fullname
                    }
                }
            else:
                return {
                    "success": False,
                    "message": message
                }
        else:
            # Fallback to old method
            data = load_users()
            users = data.get("users", [])

            if any(u.get("email") == request.email for u in users):
                return {
                    "success": False,
                    "message": "Email đã tồn tại!"
                }

            if not request.fullname or not request.email or not request.password:
                return {
                    "success": False,
                    "message": "Vui lòng nhập đầy đủ thông tin"
                }

            new_user = {
                "id": len(users) + 1,
                "fullname": request.fullname,
                "email": request.email,
                "phone": request.phone or "",
                "password": hash_password(request.password),
                "created_at": datetime.now().isoformat(),
                "username": request.email.split("@")[0]
            }

            users.append(new_user)
            data["users"] = users
            save_users(data)

            return {
                "success": True,
                "message": "Đăng ký thành công! Vui lòng đăng nhập.",
                "user": {
                    "id": new_user["id"],
                    "fullname": new_user["fullname"],
                    "email": new_user["email"]
                }
            }
    except Exception as e:
        print(f"Register error: {e}")
        return {
            "success": False,
            "message": f"Lỗi server: {str(e)}"
        }

@app.post("/api/login")
async def login(request: LoginRequest):
    """Đăng nhập - Thread-safe với ConcurrentLoginManager"""
    try:
        # Sử dụng concurrent login manager
        if login_manager:
            success, message, user_info = login_manager.login_user(
                username=request.email,  # Gửi toàn bộ email để tìm chính xác
                password=request.password
            )
            
            if success:
                # Create token
                token = create_access_token({"sub": request.email})
                
                return {
                    "success": True,
                    "message": message,
                    "token": token,
                    "user": user_info
                }
            else:
                return {
                    "success": False,
                    "message": message
                }
        else:
            # Fallback to old method
            data = load_users()
            users = data.get("users", [])

            user = next((u for u in users if u.get("email") == request.email), None)

            if not user:
                return {
                    "success": False,
                    "message": "Email không tồn tại"
                }

            if not verify_password(request.password, user.get("password", "")):
                return {
                    "success": False,
                    "message": "Mật khẩu không chính xác"
                }

            token = create_access_token({"sub": user.get("email")})

            return {
                "success": True,
                "message": "Đăng nhập thành công!",
                "token": token,
                "user": {
                    "id": user.get("id"),
                    "fullname": user.get("fullname"),
                    "email": user.get("email"),
                    "username": user.get("username")
                }
            }
    except Exception as e:
        print(f"Login error: {e}")
        return {
            "success": False,
            "message": f"Lỗi server: {str(e)}"
        }

@app.post("/api/logout")
async def logout(username: str = Depends(verify_token)):
    """Đăng xuất - Thread-safe"""
    try:
        if login_manager:
            login_manager.logout_user(username)
        
        return {
            "success": True,
            "message": "Đăng xuất thành công!"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Lỗi: {str(e)}"
        }

# ===== Forgot Password Endpoints =====
# Store reset codes temporarily (in production, use Redis or database)
reset_codes_store = {}

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    reset_code: str
    new_password: str

@app.post("/api/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Generate reset code for password recovery"""
    try:
        data = load_users()
        users = data.get("users", [])
        
        # Check if user exists
        user = next((u for u in users if u.get("email") == request.email), None)
        if not user:
            return {
                "success": False,
                "message": "Email not found"
            }
        
        # Generate 6-digit reset code
        import random
        reset_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Store reset code with expiration (10 minutes)
        reset_codes_store[request.email] = {
            "code": reset_code,
            "expires_at": datetime.now() + timedelta(minutes=10)
        }
        
        # In production, send email here
        # For now, return the code in response
        return {
            "success": True,
            "message": "Reset code generated successfully",
            "reset_code": reset_code  # In production, remove this and send via email
        }
    except Exception as e:
        print(f"Forgot password error: {e}")
        return {
            "success": False,
            "message": f"Server error: {str(e)}"
        }

@app.post("/api/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Reset password using reset code"""
    try:
        # Check if reset code exists
        if request.email not in reset_codes_store:
            return {
                "success": False,
                "message": "No reset code found for this email"
            }
        
        stored_data = reset_codes_store[request.email]
        
        # Check if code expired
        if datetime.now() > stored_data["expires_at"]:
            del reset_codes_store[request.email]
            return {
                "success": False,
                "message": "Reset code has expired"
            }
        
        # Verify reset code
        if stored_data["code"] != request.reset_code:
            return {
                "success": False,
                "message": "Invalid reset code"
            }
        
        # Update password
        data = load_users()
        users = data.get("users", [])
        
        user = next((u for u in users if u.get("email") == request.email), None)
        if not user:
            return {
                "success": False,
                "message": "User not found"
            }
        
        # Hash and update password
        user["password"] = hash_password(request.new_password)
        save_users(data)
        
        # Remove used reset code
        del reset_codes_store[request.email]
        
        return {
            "success": True,
            "message": "Password reset successfully"
        }
    except Exception as e:
        print(f"Reset password error: {e}")
        return {
            "success": False,
            "message": f"Server error: {str(e)}"
        }

@app.get("/api/user/profile")
async def get_user_profile(username: str = Depends(verify_token)):
    """Lấy thông tin hồ sơ người dùng."""
    try:
        data = load_users()
        users = data.get("users", [])
        user = next((u for u in users if u.get("email") == username), None)

        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        return {
            "success": True,
            "user": {
                "id": user.get("id"),
                "fullname": user.get("fullname"),
                "email": user.get("email"),
                "phone": user.get("phone"),
                "username": user.get("username"),
                "created_at": user.get("created_at")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image Recognition Routes
@app.post("/api/recognize/landmark")
async def recognize_landmark(file: UploadFile = File(...)):
    """Nhận dạng địa danh từ ảnh - trả về tên, tọa độ, địa chỉ."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File phải là ảnh")
    
    try:
        image_bytes = await file.read()
        image_pil = Image.open(BytesIO(image_bytes))
        
        # Gọi OpenAI Vision API - trả về đầy đủ thông tin
        result = get_landmark_with_confidence(image_pil)
        
        # Format coordinates và address
        lat = result.get("lat")
        lon = result.get("lon")
        address = result.get("address")
        
        # Tạo coordinate string
        coordinates_str = f"{lat}, {lon}" if lat and lon else "N/A"
        
        # Trả về response với coordinates và address đầy đủ
        return {
            "success": True, 
            "landmark": result.get("landmark", "Không rõ địa danh"),
            "description": result.get("description", ""),
            "confidence": result.get("confidence", "low"),
            "lat": lat,
            "lon": lon,
            "coordinates": coordinates_str,
            "address": address or "Không có thông tin địa chỉ",
            "full_info": f"📍 {result.get('landmark', 'N/A')}\n🌍 Tọa độ: {coordinates_str}\n📮 Địa chỉ: {address or 'N/A'}" if lat else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recognize/location")
async def recognize_location(file: UploadFile = File(...)):
    """Nhận dạng vị trí từ ảnh (GPS hoặc AI) - trả về tọa độ và địa chỉ."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File phải là ảnh")
    
    try:
        image_bytes = await file.read()
        image_pil = Image.open(BytesIO(image_bytes))
        
        # Tạo file-like object từ bytes để detect_location có thể đọc EXIF
        file_obj = BytesIO(image_bytes)
        file_obj.name = file.filename
        
        # Gọi OpenAI Vision API để nhận dạng địa điểm
        result = get_landmark_with_confidence(image_pil)
        
        # Lấy thông tin
        lat = result.get("lat")
        lon = result.get("lon")
        address = result.get("address")
        landmark = result.get("landmark", "Không rõ")
        
        # Tạo location string từ address hoặc landmark name
        location = address or landmark or "Không xác định được vị trí"
        coordinates_str = f"{lat}, {lon}" if lat and lon else "N/A"
        
        return {
            "success": True, 
            "location": location,
            "landmark": landmark,
            "description": result.get("description", ""),
            "lat": lat,
            "lon": lon,
            "coordinates": coordinates_str,
            "address": address or "Không có thông tin địa chỉ",
            "confidence": result.get("confidence", "low"),
            "display_text": f"🏛️ {landmark}\n📍 {coordinates_str}\n📮 {address or 'N/A'}" if lat else landmark
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Recommendation Routes
@app.post("/api/recommend/interest")
async def recommend_by_interest_api(request: InterestRequest):
    """Gợi ý địa điểm theo sở thích."""
    try:
        destinations = loadDestination()
        results = recommend(request.interest, destinations)
        # Convert to expected format
        formatted_results = []
        for dest in results:
            formatted_results.append({
                "destination": dest,
                "score": 5  # Default score
            })
        return {"success": True, "recommendations": formatted_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommend/ai")
async def ai_recommend_api(request: InterestRequest):
    """Gợi ý địa điểm bằng AI."""
    try:
        destinations = loadDestination()
        result = ai_recommend(request.interest, destinations)
        return {"success": True, "recommendation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommend/nearby")
async def recommend_nearby(request: LocationRequest):
    """Gợi ý địa điểm gần vị trí hiện tại."""
    try:
        destinations = loadDestination()
        results = []
        
        for dest in destinations:
            if dest.get("lat") and dest.get("lon"):
                distance = haversine_distance(
                    request.latitude, 
                    request.longitude, 
                    dest["lat"], 
                    dest["lon"]
                )
                if distance <= request.radius:
                    dest_copy = dest.copy()
                    dest_copy["distance_km"] = round(distance, 2)
                    results.append(dest_copy)
        
        # Sort by distance
        results.sort(key=lambda x: x["distance_km"])
        return {"success": True, "destinations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/destinations")
async def get_all_destinations():
    """Lấy tất cả địa điểm."""
    try:
        destinations = loadDestination()
        return {"success": True, "destinations": destinations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/destinations/popular")
async def get_popular_destinations():
    """Lấy 6 địa điểm phổ biến dựa trên rating."""
    try:
        destinations = loadDestination()
        # Sắp xếp theo rating giảm dần và lấy 6 địa điểm đầu
        sorted_destinations = sorted(destinations, key=lambda x: x.get('rating', 0), reverse=True)
        popular = sorted_destinations[:6]
        return {"success": True, "destinations": popular}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/districts")
async def get_districts():
    """Lấy danh sách khu vực từ CSV."""
    try:
        import csv
        districts = []
        csv_path = os.path.join(os.path.dirname(__file__), 'vn_provinces_coords.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('district') and row.get('name') and row.get('lat') and row.get('lon'):
                    try:
                        districts.append({
                            'district': row['district'].strip(),
                            'name': row['name'].strip(),
                            'lat': float(row['lat']),
                            'lon': float(row['lon'])
                        })
                    except ValueError:
                        # Skip rows with invalid lat/lon
                        continue
        
        return {"success": True, "districts": districts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/destinations/random")
async def get_random_destinations(count: int = 4):
    """Lấy địa điểm random có rating cao."""
    try:
        import random
        destinations = loadDestination()
        # Lọc những địa điểm có rating >= 4.5
        high_rated = [d for d in destinations if d.get('rating', 0) >= 4.5]
        # Random chọn count địa điểm
        selected = random.sample(high_rated, min(count, len(high_rated)))
        return {"success": True, "destinations": selected}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Album Management Routes
@app.post("/api/albums")
async def create_album(request: AlbumCreateRequest, user_email: str = Depends(verify_token)):
    """Tạo album mới cho user đã đăng nhập."""
    try:
        user_albums = load_user_albums(user_email)
        
        if request.name in user_albums:
            return {"success": False, "message": "Album đã tồn tại"}
        
        user_albums[request.name] = []
        save_user_albums(user_email, user_albums)
        return {"success": True, "message": f"Đã tạo album '{request.name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums")
async def get_albums(user_email: str = Depends(verify_token)):
    """Lấy danh sách album của user."""
    try:
        user_albums = load_user_albums(user_email)
        albums_info = {}
        
        for name, items in user_albums.items():
            albums_info[name] = {
                "name": name,
                "count": len(items),
                "created_at": min([item["uploaded_at"] for item in items]) if items else None
            }
        return {"success": True, "albums": albums_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/albums/{album_name}")
async def delete_album(album_name: str, user_email: str = Depends(verify_token)):
    """Xóa album của user."""
    try:
        user_albums = load_user_albums(user_email)
        
        # Debug logging
        print(f"[DELETE ALBUM] User: {user_email}")
        print(f"[DELETE ALBUM] Requested album name: '{album_name}'")
        print(f"[DELETE ALBUM] Available albums: {list(user_albums.keys())}")
        
        if album_name not in user_albums:
            return {"success": False, "message": f"Album không tồn tại. Available: {list(user_albums.keys())}"}
        
        del user_albums[album_name]
        save_user_albums(user_email, user_albums)
        print(f"[DELETE ALBUM] Successfully deleted album '{album_name}'")
        return {"success": True, "message": f"Đã xóa album '{album_name}'"}
    except Exception as e:
        print(f"[DELETE ALBUM] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/albums/{album_name}/images/{filename}")
async def delete_image_from_album(album_name: str, filename: str, user_email: str = Depends(verify_token)):
    """Xóa một ảnh cụ thể khỏi album."""
    try:
        user_albums = load_user_albums(user_email)
        
        print(f"[DELETE IMAGE] User: {user_email}")
        print(f"[DELETE IMAGE] Album: '{album_name}'")
        print(f"[DELETE IMAGE] Filename: '{filename}'")
        
        if album_name not in user_albums:
            print(f"[DELETE IMAGE] Album not found")
            return {"success": False, "message": f"Album '{album_name}' không tồn tại"}
        
        # user_albums[album_name] is a list of image dictionaries
        images = user_albums[album_name]
        
        print(f"[DELETE IMAGE] Current image count: {len(images)}")
        print(f"[DELETE IMAGE] Images in album: {[img.get('filename') for img in images]}")
        
        # Find and remove the image
        original_count = len(images)
        images = [img for img in images if img.get("filename") != filename]
        
        if len(images) == original_count:
            print(f"[DELETE IMAGE] Image not found in album")
            return {"success": False, "message": f"Ảnh '{filename}' không tồn tại trong album"}
        
        # Update album with filtered images list
        user_albums[album_name] = images
        
        # Save updated albums
        save_user_albums(user_email, user_albums)
        
        print(f"[DELETE IMAGE] Successfully deleted. Remaining: {len(images)}")
        return {
            "success": True, 
            "message": f"Đã xóa ảnh '{filename}' khỏi album '{album_name}'",
            "remaining_count": len(images)
        }
    except Exception as e:
        print(f"[DELETE IMAGE] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/albums/{album_name}/images")
async def add_image_to_album(
    album_name: str,
    files: List[UploadFile] = File(...),
    auto_recognize: bool = Form(True),
    user_email: str = Depends(verify_token)
):
    """Thêm nhiều ảnh vào album với tùy chọn nhận dạng tự động."""
    try:
        print(f"[ADD IMAGES] User: {user_email}")
        print(f"[ADD IMAGES] Album name: '{album_name}'")
        print(f"[ADD IMAGES] Number of files: {len(files)}")
        print(f"[ADD IMAGES] Auto recognize: {auto_recognize}")
        
        user_albums = load_user_albums(user_email)
        
        # Create album if not exists
        if album_name not in user_albums:
            print(f"[ADD IMAGES] Creating new album: '{album_name}'")
            user_albums[album_name] = []
        else:
            print(f"[ADD IMAGES] Album exists with {len(user_albums[album_name])} images")
        
        success_count = 0
        errors = []
        
        for file in files:
            if not file.content_type.startswith('image/'):
                errors.append(f"{file.filename}: Không phải file ảnh")
                continue
            
            try:
                image_bytes = await file.read()
                landmark = "N/A"
                description = ""
                confidence = "low"
                
                if auto_recognize and OPENAI_ENABLED:
                    try:
                        image_pil = Image.open(BytesIO(image_bytes))
                        # Use the new function that returns dict
                        result = get_landmark_with_confidence(image_pil)
                        landmark = result.get("landmark", "N/A")
                        description = result.get("description", "")
                        confidence = result.get("confidence", "low")
                    except Exception as e:
                        landmark = "Không rõ địa danh"
                        description = f"Lỗi: {str(e)[:50]}"
                        confidence = "low"
                
                # Encode image to base64
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                
                item = {
                    "filename": file.filename,
                    "image_data": image_b64,
                    "uploaded_at": datetime.now().isoformat(),
                    "album_name": album_name,
                    "landmark": landmark,
                    "description": description,
                    "confidence": confidence
                }
                
                print(f"[DEBUG] Saving image to album: {file.filename}")
                print(f"[DEBUG]   - Original bytes: {len(image_bytes)}")
                print(f"[DEBUG]   - Base64 length: {len(image_b64)}")
                print(f"[DEBUG]   - Has image_data: {'image_data' in item}")
                
                user_albums[album_name].append(item)
                success_count += 1
                
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
        
        # Save albums to file
        save_user_albums(user_email, user_albums)
        
        print(f"[ADD IMAGES] Successfully added {success_count}/{len(files)} images")
        if errors:
            print(f"[ADD IMAGES] Errors: {errors}")
        
        return {
            "success": True, 
            "message": f"Đã thêm {success_count}/{len(files)} ảnh vào album '{album_name}'",
            "added_count": success_count,
            "total_count": len(files),
            "errors": errors
        }
    except Exception as e:
        print(f"[ADD IMAGES] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums/{album_name}/images")
async def get_album_images(
    album_name: str, 
    include_images: bool = False,
    search_landmark: Optional[str] = None,
    search_date: Optional[str] = None,
    user_email: str = Depends(verify_token)
):
    """Lấy danh sách ảnh trong album của user."""
    try:
        user_albums = load_user_albums(user_email)
        
        if album_name not in user_albums:
            return {"success": True, "images": [], "total": 0}
        
        items = user_albums[album_name].copy()
        
        # Áp dụng filter nếu có
        if search_landmark:
            items = [item for item in items if search_landmark.lower() in item.get('landmark', '').lower()]
        
        if search_date:
            items = [item for item in items 
                    if datetime.fromisoformat(item['uploaded_at']).date().isoformat() == search_date]
        
        if not include_images:
            # Loại bỏ data ảnh để giảm kích thước response
            for item in items:
                item.pop("image_data", None)
        
        return {
            "success": True, 
            "images": items,
            "total": len(items),
            "album_total": len(user_albums[album_name])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums/{album_name}/images/{filename}/view")
async def view_album_image(album_name: str, filename: str, token: str = Query(...)):
    """Serve ảnh từ album để hiển thị."""
    try:
        # Verify token từ query parameter
        user_email = verify_token_from_string(token)
        user_albums = load_user_albums(user_email)
        
        print(f"[VIEW IMAGE] User: {user_email}")
        print(f"[VIEW IMAGE] Album: '{album_name}'")
        print(f"[VIEW IMAGE] Filename: '{filename}'")
        
        if album_name not in user_albums:
            raise HTTPException(status_code=404, detail="Album không tồn tại")
        
        # Tìm ảnh trong album
        images = user_albums[album_name]
        image_item = None
        for img in images:
            if img.get("filename") == filename:
                image_item = img
                break
        
        if not image_item:
            raise HTTPException(status_code=404, detail="Ảnh không tồn tại trong album")
        
        # Lấy image_data (base64)
        image_data = image_item.get("image_data")
        if not image_data:
            raise HTTPException(status_code=404, detail="Dữ liệu ảnh không tồn tại")
        
        # Decode base64
        import base64
        from io import BytesIO
        from fastapi.responses import StreamingResponse
        
        # Remove data URI prefix if exists
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Determine content type
        content_type = "image/jpeg"
        if filename.lower().endswith('.png'):
            content_type = "image/png"
        elif filename.lower().endswith('.gif'):
            content_type = "image/gif"
        elif filename.lower().endswith('.webp'):
            content_type = "image/webp"
        
        return StreamingResponse(BytesIO(image_bytes), media_type=content_type)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[VIEW IMAGE] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums/{album_name}/download")
async def download_album(album_name: str, user_email: str = Depends(verify_token)):
    """Tải album dưới dạng ZIP."""
    try:
        user_albums = load_user_albums(user_email)
        
        if album_name not in user_albums:
            raise HTTPException(status_code=404, detail="Album không tồn tại")
        
        items = user_albums[album_name]
        if not items:
            raise HTTPException(status_code=400, detail="Album trống, không có ảnh để tải")
        
        print(f"[DEBUG] Downloading album '{album_name}' with {len(items)} items")
        
        # Debug: check first item structure
        if items:
            first_item = items[0]
            print(f"[DEBUG] First item keys: {list(first_item.keys())}")
            print(f"[DEBUG] First item has image_data: {'image_data' in first_item}")
            print(f"[DEBUG] First item has bytes: {'bytes' in first_item}")
            if 'image_data' in first_item:
                img_data_len = len(first_item['image_data']) if first_item['image_data'] else 0
                print(f"[DEBUG] image_data length: {img_data_len} chars")
        
        from zipfile import ZipFile, ZIP_DEFLATED
        
        buf = BytesIO()
        added_count = 0
        
        with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
            for idx, item in enumerate(items):
                try:
                    filename = item.get("filename", f"image_{idx}.jpg")
                    # Sanitize filename
                    filename = filename.replace('/', '_').replace('\\', '_')
                    
                    image_bytes = None
                    
                    # Try different data formats
                    # Priority 1: image_data (base64 string)
                    if "image_data" in item and item["image_data"]:
                        try:
                            # Handle base64 encoded image
                            img_data = item["image_data"]
                            # Remove data URL prefix if present (data:image/jpeg;base64,...)
                            if isinstance(img_data, str) and 'base64,' in img_data:
                                img_data = img_data.split('base64,')[1]
                            image_bytes = base64.b64decode(img_data)
                            print(f"[DEBUG] Decoded base64 for {filename}: {len(image_bytes)} bytes")
                        except Exception as e:
                            print(f"[DEBUG] Failed to decode base64 for {filename}: {e}")
                    
                    # Priority 2: bytes field
                    if image_bytes is None and "bytes" in item and item["bytes"]:
                        # Use direct bytes
                        if isinstance(item["bytes"], bytes):
                            image_bytes = item["bytes"]
                            print(f"[DEBUG] Using direct bytes for {filename}: {len(image_bytes)} bytes")
                        elif isinstance(item["bytes"], str):
                            # Maybe it's base64 string stored as bytes
                            try:
                                image_bytes = base64.b64decode(item["bytes"])
                                print(f"[DEBUG] Decoded bytes field for {filename}: {len(image_bytes)} bytes")
                            except:
                                pass
                    
                    if image_bytes and len(image_bytes) > 0:
                        zf.writestr(filename, image_bytes)
                        added_count += 1
                        print(f"[DEBUG] Added {filename} to ZIP")
                    else:
                        print(f"[DEBUG] Skipped {filename}: no valid image data")
                        
                except Exception as e:
                    print(f"[ERROR] Error adding {item.get('filename', f'image_{idx}')}: {e}")
                    continue
        
        buf.seek(0)
        zip_data = buf.getvalue()
        
        print(f"[DEBUG] Created ZIP: {len(zip_data)} bytes, {added_count} images added")
        
        if len(zip_data) <= 100:  # ZIP header is at least 22 bytes, so empty ZIP is very small
            raise HTTPException(status_code=400, detail=f"Không thể tạo file ZIP (chỉ thêm {added_count}/{len(items)} ảnh)")
        
        safe_name = album_name.replace('/', '_').replace('"', '')
        return StreamingResponse(
            BytesIO(zip_data),
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{safe_name}.zip"'}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Download album error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi tải album: {str(e)}")

@app.get("/api/albums/debug/{album_name}")
async def debug_album_storage(album_name: str):
    """Debug endpoint để kiểm tra album storage trực tiếp."""
    if album_name not in album_storage:
        return {"error": "Album not found", "available_albums": list(album_storage.keys())}
    
    items = album_storage[album_name]
    debug_info = {
        "album_name": album_name,
        "total_items": len(items),
        "items_info": []
    }
    
    for idx, item in enumerate(items):
        item_info = {
            "index": idx,
            "filename": item.get("filename"),
            "keys": list(item.keys()),
            "has_image_data": "image_data" in item,
            "has_bytes": "bytes" in item
        }
        if "image_data" in item:
            item_info["image_data_length"] = len(item["image_data"]) if item["image_data"] else 0
        if "bytes" in item:
            item_info["bytes_length"] = len(item["bytes"]) if item["bytes"] else 0
        debug_info["items_info"].append(item_info)
    
    return debug_info

@app.get("/api/albums/stats")
async def get_albums_stats(user_email: str = Depends(verify_token)):
    """Lấy thống kê tổng quan về các album của user."""
    try:
        user_albums = load_user_albums(user_email)
        
        stats = {
            "total_albums": len(user_albums),
            "total_images": sum(len(items) for items in user_albums.values()),
            "albums": {}
        }
        
        for album_name, items in user_albums.items():
            item_data = {
                "image_count": len(items),
                "last_modified": max((item.get("uploaded_at", "") for item in items), default=""),
                "landmarks": list(set(item.get("landmark", "N/A") for item in items))
            }
            # Add debug info for first item
            if items:
                first_item = items[0]
                item_data["first_item_keys"] = list(first_item.keys())
                item_data["first_item_data_type"] = type(first_item.get("image_data", "N/A")).__name__
                if "image_data" in first_item:
                    item_data["image_data_length"] = len(first_item.get("image_data", ""))
            stats["albums"][album_name] = item_data
        
        print(f"[DEBUG] Album stats: {stats}")
        return stats
    except Exception as e:
        print(f"[ERROR] Error getting album stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoint for grouping images by landmark
@app.get("/api/albums/{album_name}/group-by-landmark")
async def get_album_grouped_by_landmark(album_name: str):
    """Lấy ảnh trong album được nhóm theo địa danh."""
    try:
        if album_name not in album_storage:
            return {"success": True, "groups": {}}
        
        items = album_storage[album_name]
        groups = {}
        
        for item in items:
            landmark = item.get('landmark', 'Chưa nhận dạng')
            if landmark not in groups:
                groups[landmark] = []
            
            # Tạo bản sao không có image_data để giảm kích thước
            item_copy = {k: v for k, v in item.items() if k != "image_data"}
            groups[landmark].append(item_copy)
        
        return {"success": True, "groups": groups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Review & Rating Routes =====

def load_reviews() -> dict:
    """Tải đánh giá từ file."""
    if not os.path.exists(REVIEWS_FILE):
        return {"reviews": []}
    try:
        with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"reviews": []}

def save_reviews(data: dict):
    """Lưu đánh giá vào file."""
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.post("/api/reviews")
async def create_review(request: ReviewRequest, username: str = Depends(verify_token)):
    """Tạo đánh giá mới cho địa điểm."""
    try:
        if request.rating < 1 or request.rating > 5:
            return {"success": False, "message": "Rating phải từ 1-5"}
        
        data = load_reviews()
        reviews = data.get("reviews", [])
        
        # Kiểm tra user đã review chưa
        existing = next((r for r in reviews 
                        if r["user_email"] == username 
                        and r["destination_name"] == request.destination_name), None)
        
        if existing:
            return {"success": False, "message": "Bạn đã đánh giá địa điểm này rồi"}
        
        new_review = {
            "id": len(reviews) + 1,
            "user_email": username,
            "destination_name": request.destination_name,
            "rating": request.rating,
            "comment": request.comment,
            "created_at": datetime.now().isoformat(),
            "helpful_count": 0
        }
        
        reviews.append(new_review)
        data["reviews"] = reviews
        save_reviews(data)
        
        return {
            "success": True,
            "message": "Đánh giá thành công!",
            "review": new_review
        }
    except Exception as e:
        print(f"Review error: {e}")
        return {"success": False, "message": f"Lỗi: {str(e)}"}

@app.get("/api/reviews/{destination_name}")
async def get_destination_reviews(destination_name: str):
    """Lấy tất cả đánh giá của một địa điểm."""
    try:
        data = load_reviews()
        reviews = data.get("reviews", [])
        
        dest_reviews = [r for r in reviews if r["destination_name"] == destination_name]
        
        # Tính rating trung bình
        avg_rating = 0
        if dest_reviews:
            avg_rating = sum(r["rating"] for r in dest_reviews) / len(dest_reviews)
        
        return {
            "success": True,
            "reviews": dest_reviews,
            "total": len(dest_reviews),
            "average_rating": round(avg_rating, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews/user/my-reviews")
async def get_my_reviews(username: str = Depends(verify_token)):
    """Lấy tất cả đánh giá của user hiện tại."""
    try:
        data = load_reviews()
        reviews = data.get("reviews", [])
        
        my_reviews = [r for r in reviews if r["user_email"] == username]
        
        return {
            "success": True,
            "reviews": my_reviews,
            "total": len(my_reviews)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/reviews/{review_id}")
async def delete_review(review_id: int, username: str = Depends(verify_token)):
    """Xóa đánh giá của mình."""
    try:
        data = load_reviews()
        reviews = data.get("reviews", [])
        
        review = next((r for r in reviews if r["id"] == review_id), None)
        if not review:
            return {"success": False, "message": "Đánh giá không tồn tại"}
        
        if review["user_email"] != username:
            return {"success": False, "message": "Bạn không có quyền xóa đánh giá này"}
        
        reviews = [r for r in reviews if r["id"] != review_id]
        data["reviews"] = reviews
        save_reviews(data)
        
        return {"success": True, "message": "Đã xóa đánh giá"}
    except Exception as e:
        return {"success": False, "message": f"Lỗi: {str(e)}"}

# ===== Favorites Routes =====

def load_favorites() -> dict:
    """Tải danh sách yêu thích từ file."""
    if not os.path.exists(FAVORITES_FILE):
        return {"favorites": {}}
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"favorites": {}}

def save_favorites(data: dict):
    """Lưu danh sách yêu thích vào file."""
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.post("/api/favorites/{destination_name}")
async def add_favorite(destination_name: str, username: str = Depends(verify_token)):
    """Thêm địa điểm vào yêu thích."""
    try:
        data = load_favorites()
        favorites = data.get("favorites", {})
        
        if username not in favorites:
            favorites[username] = []
        
        if destination_name in favorites[username]:
            return {"success": False, "message": "Địa điểm đã có trong danh sách yêu thích"}
        
        favorites[username].append(destination_name)
        data["favorites"] = favorites
        save_favorites(data)
        
        return {
            "success": True,
            "message": "Đã thêm vào yêu thích",
            "favorites": favorites[username]
        }
    except Exception as e:
        return {"success": False, "message": f"Lỗi: {str(e)}"}

@app.delete("/api/favorites/{destination_name}")
async def remove_favorite(destination_name: str, username: str = Depends(verify_token)):
    """Xóa địa điểm khỏi yêu thích."""
    try:
        data = load_favorites()
        favorites = data.get("favorites", {})
        
        if username not in favorites or destination_name not in favorites[username]:
            return {"success": False, "message": "Địa điểm không có trong danh sách yêu thích"}
        
        favorites[username].remove(destination_name)
        data["favorites"] = favorites
        save_favorites(data)
        
        return {
            "success": True,
            "message": "Đã xóa khỏi yêu thích",
            "favorites": favorites[username]
        }
    except Exception as e:
        return {"success": False, "message": f"Lỗi: {str(e)}"}

@app.get("/api/favorites")
async def get_favorites(username: str = Depends(verify_token)):
    """Lấy danh sách yêu thích của user."""
    try:
        data = load_favorites()
        favorites = data.get("favorites", {})
        
        user_favorites = favorites.get(username, [])
        
        return {
            "success": True,
            "favorites": user_favorites,
            "total": len(user_favorites)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/favorites/check/{destination_name}")
async def check_favorite(destination_name: str, username: str = Depends(verify_token)):
    """Kiểm tra địa điểm có trong yêu thích không."""
    try:
        data = load_favorites()
        favorites = data.get("favorites", {})
        
        is_favorite = destination_name in favorites.get(username, [])
        
        return {
            "success": True,
            "is_favorite": is_favorite
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== User Profile Routes =====

@app.put("/api/user/profile")
async def update_profile(request: UserProfileUpdate, username: str = Depends(verify_token)):
    """Cập nhật thông tin hồ sơ người dùng."""
    try:
        data = load_users()
        users = data.get("users", [])
        user = next((u for u in users if u.get("email") == username), None)
        
        if not user:
            return {"success": False, "message": "Người dùng không tồn tại"}
        
        # Cập nhật thông tin
        if request.fullname:
            user["fullname"] = request.fullname
        if request.phone:
            user["phone"] = request.phone
        if request.bio is not None:
            user["bio"] = request.bio
        if request.avatar_url:
            user["avatar_url"] = request.avatar_url
        
        user["updated_at"] = datetime.now().isoformat()
        
        save_users(data)
        
        return {
            "success": True,
            "message": "Cập nhật thông tin thành công",
            "user": {
                "fullname": user.get("fullname"),
                "email": user.get("email"),
                "phone": user.get("phone"),
                "bio": user.get("bio", ""),
                "avatar_url": user.get("avatar_url", ""),
                "updated_at": user.get("updated_at")
            }
        }
    except Exception as e:
        return {"success": False, "message": f"Lỗi: {str(e)}"}

@app.put("/api/user/settings")
async def update_settings(request: UserSettingsUpdate, username: str = Depends(verify_token)):
    """Cập nhật cài đặt người dùng."""
    try:
        data = load_users()
        users = data.get("users", [])
        user = next((u for u in users if u.get("email") == username), None)
        
        if not user:
            return {"success": False, "message": "Người dùng không tồn tại"}
        
        # Khởi tạo settings nếu chưa có
        if "settings" not in user:
            user["settings"] = {
                "email_notifications": True,
                "language": "vi",
                "theme": "light"
            }
        
        # Cập nhật settings
        if request.email_notifications is not None:
            user["settings"]["email_notifications"] = request.email_notifications
        if request.language:
            user["settings"]["language"] = request.language
        if request.theme:
            user["settings"]["theme"] = request.theme
        
        save_users(data)
        
        return {
            "success": True,
            "message": "Cập nhật cài đặt thành công",
            "settings": user["settings"]
        }
    except Exception as e:
        return {"success": False, "message": f"Lỗi: {str(e)}"}

@app.get("/api/user/settings")
async def get_settings(username: str = Depends(verify_token)):
    """Lấy cài đặt người dùng."""
    try:
        data = load_users()
        users = data.get("users", [])
        user = next((u for u in users if u.get("email") == username), None)
        
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
        
        # Khởi tạo settings mặc định nếu chưa có
        if "settings" not in user:
            user["settings"] = {
                "email_notifications": True,
                "language": "vi",
                "theme": "light"
            }
            save_users(data)
        
        return {
            "success": True,
            "settings": user["settings"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/stats")
async def get_user_stats(user_email: str = Depends(verify_token)):
    """Lấy thống kê hoạt động của user."""
    try:
        # Đếm số reviews
        review_data = load_reviews()
        reviews = review_data.get("reviews", [])
        user_reviews_count = len([r for r in reviews if r["user_email"] == user_email])
        
        # Đếm số favorites
        fav_data = load_favorites()
        favorites = fav_data.get("favorites", {})
        favorites_count = len(favorites.get(user_email, []))
        
        # Đếm số albums
        album_data = load_user_albums(user_email)
        albums_count = len(album_data)
        
        # Tổng số ảnh
        total_images = sum(len(items) for items in album_data.values())
        
        return {
            "success": True,
            "stats": {
                "reviews_count": user_reviews_count,
                "favorites_count": favorites_count,
                "albums_count": albums_count,
                "images_count": total_images
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Chatbot Routes =====

@app.post("/api/chatbot/chat")
async def chatbot_chat(request: ChatbotMessageRequest):
    """
    Gửi tin nhắn tới chatbot du lịch.
    Chatbot sẽ sử dụng AI để gợi ý địa điểm phù hợp.
    """
    try:
        if not chatbot_instance:
            raise HTTPException(status_code=500, detail="Chatbot chưa được khởi tạo")
        
        result = chatbot_instance.chat(request.message, use_ai=request.use_ai)
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.get("/api/chatbot/suggestions")
async def chatbot_suggestions():
    """
    Lấy danh sách gợi ý nhanh (các tags phổ biến).
    """
    try:
        if not chatbot_instance:
            raise HTTPException(status_code=500, detail="Chatbot chưa được khởi tạo")
        
        suggestions = chatbot_instance.get_quick_suggestions()
        return {
            "status": "success",
            "suggestions": suggestions
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.get("/api/chatbot/history")
async def chatbot_history():
    """
    Lấy lịch sử cuộc trò chuyện.
    """
    try:
        if not chatbot_instance:
            raise HTTPException(status_code=500, detail="Chatbot chưa được khởi tạo")
        
        history = chatbot_instance.get_conversation_history()
        return {
            "status": "success",
            "history": history
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.delete("/api/chatbot/history")
async def clear_chatbot_history():
    """
    Xóa lịch sử cuộc trò chuyện.
    """
    try:
        if not chatbot_instance:
            raise HTTPException(status_code=500, detail="Chatbot chưa được khởi tạo")
        
        chatbot_instance.clear_history()
        return {
            "status": "success",
            "message": "Lịch sử đã được xóa"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.post("/api/chatbot/search")
async def chatbot_search(request: ChatbotSearchRequest):
    """
    Tìm kiếm địa điểm theo các tiêu chí:
    - tags: Danh sách các tags cần tìm
    - min_price: Giá tối thiểu
    - max_price: Giá tối đa
    """
    try:
        if not chatbot_instance:
            raise HTTPException(status_code=500, detail="Chatbot chưa được khởi tạo")
        
        results = []
        
        # Tìm theo tags
        if request.tags:
            results = chatbot_instance.search_by_tags(request.tags)
        
        # Tìm theo khoảng giá
        if request.min_price is not None and request.max_price is not None:
            price_results = chatbot_instance.search_by_price_range(
                request.min_price, 
                request.max_price
            )
            if results:
                # Lấy giao của 2 kết quả
                results = [r for r in results if r in price_results]
            else:
                results = price_results
        
        formatted_results = [
            {
                "name": dest.get("name"),
                "location": dest.get("location"),
                "introduction": dest.get("introduction"),
                "price": dest.get("price"),
                "rating": dest.get("rating"),
                "images": dest.get("images", [])
            }
            for dest in results
        ]
        
        return {
            "status": "success",
            "count": len(formatted_results),
            "results": formatted_results
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.get("/api/chatbot/top-rated")
async def chatbot_top_rated(limit: int = 5):
    """
    Lấy các địa điểm được đánh giá cao nhất.
    """
    try:
        if not chatbot_instance:
            raise HTTPException(status_code=500, detail="Chatbot chưa được khởi tạo")
        
        results = chatbot_instance.get_top_rated(limit)
        
        formatted_results = [
            {
                "name": dest.get("name"),
                "location": dest.get("location"),
                "introduction": dest.get("introduction"),
                "price": dest.get("price"),
                "rating": dest.get("rating"),
                "images": dest.get("images", [])
            }
            for dest in results
        ]
        
        return {
            "status": "success",
            "results": formatted_results
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

# ===== Concurrent User Management Routes =====

@app.get("/api/users/stats")
async def get_user_stats():
    """Lấy thống kê người dùng và sessions"""
    try:
        if login_manager:
            stats = login_manager.get_statistics()
            return {
                "status": "success",
                "data": stats
            }
        else:
            return {
                "status": "error",
                "message": "Login manager not available"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.get("/api/users/active-sessions")
async def get_active_sessions():
    """Lấy danh sách active sessions"""
    try:
        if login_manager:
            sessions = login_manager.get_active_sessions()
            return {
                "status": "success",
                "count": len(sessions),
                "sessions": sessions
            }
        else:
            return {
                "status": "error",
                "message": "Login manager not available"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.get("/api/users/is-online/{username}")
async def check_user_online(username: str):
    """Kiểm tra user có online không"""
    try:
        if login_manager:
            is_online = login_manager.is_user_online(username)
            return {
                "status": "success",
                "username": username,
                "is_online": is_online
            }
        else:
            return {
                "status": "error",
                "message": "Login manager not available"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.post("/api/users/update-activity/{username}")
async def update_user_activity(username: str):
    """Cập nhật last activity của user"""
    try:
        if login_manager:
            login_manager.update_user_activity(username)
            return {
                "status": "success",
                "message": "Activity updated"
            }
        else:
            return {
                "status": "error",
                "message": "Login manager not available"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

@app.get("/api/users/info/{username}")
async def get_user_info(username: str, token: str = Depends(verify_token)):
    """Lấy thông tin user"""
    try:
        if login_manager:
            user_info = login_manager.get_user_info(username)
            if user_info:
                return {
                    "status": "success",
                    "user": user_info
                }
            else:
                return {
                    "status": "error",
                    "message": "User not found"
                }
        else:
            return {
                "status": "error",
                "message": "Login manager not available"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi: {str(e)}"
        }

# ===== Social Feed Endpoints =====

@app.post("/api/social/posts")
async def create_post(
    content: Optional[str] = Form(""),
    location: Optional[str] = Form(None),
    user_avatar: Optional[str] = Form(None),
    user_fullname: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    """Tạo post mới với ảnh và nội dung"""
    try:
        print(f"[SOCIAL] Creating post - Content: {content}, Location: {location}, Image: {image is not None}")
        
        user_email = get_current_user_email(authorization)
        print(f"[SOCIAL] User email: {user_email}")
        
        # Validate: phải có content hoặc image
        if not content and not image:
            raise HTTPException(status_code=400, detail="Please provide content or image")
        
        image_data = None
        if image:
            # Đọc và encode ảnh thành base64
            image_bytes = await image.read()
            image_data = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"
            print(f"[SOCIAL] Image encoded, size: {len(image_data)} bytes")
        
        post = social_feed_manager.create_post(
            user_email=user_email,
            content=content or "",
            image_data=image_data,
            location=location,
            user_avatar=user_avatar,
            user_fullname=user_fullname
        )
        
        print(f"[SOCIAL] Post created successfully: {post['post_id']}")
        return {"success": True, "post": post}
    except HTTPException as e:
        print(f"[SOCIAL] HTTP Error: {e.detail}")
        raise e
    except Exception as e:
        print(f"[SOCIAL] Error creating post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/social/posts")
async def get_posts(limit: int = 20, offset: int = 0, authorization: str = Header(None)):
    """Lấy danh sách posts"""
    try:
        # Kiểm tra user đã đăng nhập
        user_email = get_current_user_email(authorization)
        print(f"[SOCIAL] Getting posts for user: {user_email}, limit: {limit}, offset: {offset}")
        
        posts = social_feed_manager.get_posts(limit=limit, offset=offset)
        print(f"[SOCIAL] Found {len(posts)} posts")
        
        # Thêm thông tin liked_by_user
        for post in posts:
            post['liked_by_user'] = social_feed_manager.is_liked_by_user(post['post_id'], user_email)
        
        return {"success": True, "posts": posts, "total": len(posts)}
    except HTTPException as e:
        print(f"[SOCIAL] HTTP Error getting posts: {e.detail}")
        raise e
    except Exception as e:
        print(f"[SOCIAL] Error getting posts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/social/posts/{post_id}")
async def get_post(post_id: str, authorization: str = Header(None)):
    """Lấy chi tiết một post"""
    try:
        user_email = get_current_user_email(authorization)
        
        post = social_feed_manager.get_post_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        post['liked_by_user'] = social_feed_manager.is_liked_by_user(post_id, user_email)
        
        return {"success": True, "post": post}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/social/users/{email}/posts")
async def get_user_posts(email: str, limit: int = 20, authorization: str = Header(None)):
    """Lấy posts của một user"""
    try:
        current_user = get_current_user_email(authorization)
        
        posts = social_feed_manager.get_user_posts(user_email=email, limit=limit)
        
        # Thêm thông tin liked_by_user
        for post in posts:
            post['liked_by_user'] = social_feed_manager.is_liked_by_user(post['post_id'], current_user)
        
        return {"success": True, "posts": posts}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/social/posts/{post_id}")
async def delete_post(post_id: str, authorization: str = Header(None)):
    """Xóa post"""
    try:
        user_email = get_current_user_email(authorization)
        
        success = social_feed_manager.delete_post(post_id, user_email)
        if not success:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")
        
        return {"success": True, "message": "Post deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/social/posts/{post_id}/comments")
async def add_comment(
    post_id: str, 
    content: str = Form(...), 
    user_avatar: Optional[str] = Form(None),
    user_fullname: Optional[str] = Form(None),
    authorization: str = Header(None)
):
    """Thêm comment vào post"""
    try:
        user_email = get_current_user_email(authorization)
        
        comment = social_feed_manager.add_comment(
            post_id, 
            user_email, 
            content,
            user_avatar=user_avatar,
            user_fullname=user_fullname
        )
        if not comment:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return {"success": True, "comment": comment}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/social/posts/{post_id}/comments")
async def get_comments(post_id: str):
    """Lấy comments của một post"""
    try:
        comments = social_feed_manager.get_comments(post_id)
        return {"success": True, "comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/social/posts/{post_id}/comments/{comment_id}")
async def delete_comment(post_id: str, comment_id: str, authorization: str = Header(None)):
    """Xóa comment"""
    try:
        user_email = get_current_user_email(authorization)
        
        success = social_feed_manager.delete_comment(post_id, comment_id, user_email)
        if not success:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this comment")
        
        return {"success": True, "message": "Comment deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/social/posts/{post_id}/like")
async def toggle_like(post_id: str, authorization: str = Header(None)):
    """Like/Unlike post"""
    try:
        user_email = get_current_user_email(authorization)
        
        result = social_feed_manager.toggle_like(post_id, user_email)
        if not result.get('success'):
            raise HTTPException(status_code=404, detail=result.get('message'))
        
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/social/posts/{post_id}/likes")
async def get_likes(post_id: str):
    """Lấy danh sách users đã like post"""
    try:
        likes = social_feed_manager.get_likes(post_id)
        return {"success": True, "likes": likes, "count": len(likes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)