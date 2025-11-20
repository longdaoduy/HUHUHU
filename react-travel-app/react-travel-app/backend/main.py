from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends, Header
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

def load_user_albums(username: str) -> dict:
    """Tải album của người dùng."""
    if not os.path.exists(USERS_ALBUM_FILE):
        return {}
    try:
        with open(USERS_ALBUM_FILE, "r", encoding="utf-8") as f:
            all_albums = json.load(f)
    except json.JSONDecodeError:
        return {}
    
    user_album = all_albums.get(username, {})
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

def save_user_albums(username: str, user_albums: dict):
    """Lưu album của người dùng."""
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

    all_albums_data[username] = albums_to_save
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
    """Kiểm tra JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token không được cung cấp")
    
    try:
        # Extract token from "Bearer <token>"
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = parts[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

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
    """Đăng ký tài khoản mới."""
    try:
        data = load_users()
        users = data.get("users", [])

        # Check if user already exists
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

        # Add new user
        new_user = {
            "id": len(users) + 1,
            "fullname": request.fullname,
            "email": request.email,
            "phone": request.phone or "",
            "password": hash_password(request.password),
            "created_at": datetime.now().isoformat(),
            "username": request.email.split("@")[0]  # Use email prefix as username
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
    """Đăng nhập."""
    try:
        data = load_users()
        users = data.get("users", [])

        # Find user by email
        user = next((u for u in users if u.get("email") == request.email), None)

        if not user:
            return {
                "success": False,
                "message": "Email không tồn tại"
            }

        # Verify password
        if not verify_password(request.password, user.get("password", "")):
            return {
                "success": False,
                "message": "Mật khẩu không chính xác"
            }

        # Create token
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
    """Đăng xuất."""
    try:
        return {
            "success": True,
            "message": "Đăng xuất thành công!"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Lỗi: {str(e)}"
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
    """Nhận dạng địa danh từ ảnh."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File phải là ảnh")
    
    try:
        image_bytes = await file.read()
        image_pil = Image.open(BytesIO(image_bytes))
        result = get_landmark_from_image(image_pil)
        
        # Tạo response với nhiều thông tin hơn
        return {
            "success": True, 
            "landmark": result,
            "description": f"Địa danh được nhận dạng: {result}",
            "confidence": "high" if result and result.lower() != "không có" else "low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recognize/location")
async def recognize_location(file: UploadFile = File(...)):
    """Nhận dạng vị trí từ ảnh (GPS hoặc AI)."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File phải là ảnh")
    
    try:
        image_bytes = await file.read()
        image_pil = Image.open(BytesIO(image_bytes))
        
        # Tạo file-like object từ bytes để detect_location có thể đọc EXIF
        file_obj = BytesIO(image_bytes)
        file_obj.name = file.filename
        
        location = detect_location(file_obj, image_pil)
        landmark = get_landmark_from_image(image_pil)
        
        return {
            "success": True, 
            "location": location or "Không xác định được vị trí",
            "landmark": landmark or "Không có",
            "description": f"Vị trí: {location or 'Không rõ'}"
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
async def create_album(request: AlbumCreateRequest):
    """Tạo album mới."""
    try:
        if request.name in album_storage:
            return {"success": False, "message": "Album đã tồn tại"}
        
        album_storage[request.name] = []
        return {"success": True, "message": f"Đã tạo album '{request.name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums")
async def get_albums():
    """Lấy danh sách album."""
    try:
        albums_info = {}
        for name, items in album_storage.items():
            albums_info[name] = {
                "name": name,
                "count": len(items),
                "created_at": min([item["uploaded_at"] for item in items]) if items else None
            }
        return {"success": True, "albums": albums_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/albums/{album_name}")
async def delete_album(album_name: str):
    """Xóa album."""
    try:
        if album_name not in album_storage:
            return {"success": False, "message": "Album không tồn tại"}
        
        del album_storage[album_name]
        return {"success": True, "message": f"Đã xóa album '{album_name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/albums/{album_name}/images")
async def add_image_to_album(
    album_name: str,
    files: List[UploadFile] = File(...),
    auto_recognize: bool = Form(True)
):
    """Thêm nhiều ảnh vào album với tùy chọn nhận dạng tự động."""
    try:
        # Create album if not exists
        if album_name not in album_storage:
            album_storage[album_name] = []
        
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
                
                album_storage[album_name].append(item)
                success_count += 1
                
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
        
        return {
            "success": True, 
            "message": f"Đã thêm {success_count}/{len(files)} ảnh vào album '{album_name}'",
            "added_count": success_count,
            "total_count": len(files),
            "errors": errors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums/{album_name}/images")
async def get_album_images(
    album_name: str, 
    include_images: bool = False,
    search_landmark: Optional[str] = None,
    search_date: Optional[str] = None
):
    """Lấy danh sách ảnh trong album với tùy chọn lọc."""
    try:
        if album_name not in album_storage:
            return {"success": True, "images": [], "total": 0}
        
        items = album_storage[album_name].copy()
        
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
            "album_total": len(album_storage[album_name])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums/{album_name}/download")
async def download_album(album_name: str):
    """Tải album dưới dạng ZIP."""
    try:
        if album_name not in album_storage:
            raise HTTPException(status_code=404, detail="Album không tồn tại")
        
        from zipfile import ZipFile, ZIP_DEFLATED
        
        buf = BytesIO()
        with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
            for item in album_storage[album_name]:
                # Decode base64 image data
                image_bytes = base64.b64decode(item["image_data"])
                zf.writestr(item["filename"], image_bytes)
        
        buf.seek(0)
        return StreamingResponse(
            BytesIO(buf.getvalue()),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={album_name}.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums/stats")
async def get_albums_stats():
    """Lấy thống kê tổng quan về các album."""
    try:
        stats = {
            "total_albums": len(album_storage),
            "total_images": sum(len(items) for items in album_storage.values()),
            "albums_detail": {}
        }
        
        for album_name, items in album_storage.items():
            landmarks = set(item.get('landmark', 'N/A') for item in items)
            stats["albums_detail"][album_name] = {
                "image_count": len(items),
                "landmark_count": len(landmarks),
                "landmarks": list(landmarks)
            }
        
        return {"success": True, "stats": stats}
    except Exception as e:
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
async def get_user_stats(username: str = Depends(verify_token)):
    """Lấy thống kê hoạt động của user."""
    try:
        # Đếm số reviews
        review_data = load_reviews()
        reviews = review_data.get("reviews", [])
        user_reviews_count = len([r for r in reviews if r["user_email"] == username])
        
        # Đếm số favorites
        fav_data = load_favorites()
        favorites = fav_data.get("favorites", {})
        favorites_count = len(favorites.get(username, []))
        
        # Đếm số albums
        album_data = load_user_albums(username)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)