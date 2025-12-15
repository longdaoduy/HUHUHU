# 🔐 Authentication Integration - Vietnam Travel App

## ✅ Đã Tích Hợp Login.py vào Main.py

### 📋 Tóm Tắt Những Gì Được Thêm:

#### 1. **Helper Functions (Từ login.py)**
- `hash_password()` - Mã hóa mật khẩu bằng SHA256
- `verify_password()` - Kiểm tra mật khẩu
- `load_users()` - Tải danh sách người dùng từ file JSON
- `save_users()` - Lưu danh sách người dùng vào file JSON
- `load_user_albums()` - Tải album của người dùng
- `save_user_albums()` - Lưu album của người dùng

#### 2. **JWT Token Management**
- `create_access_token()` - Tạo JWT token
- `verify_token()` - Kiểm tra JWT token (Dependency)
- Token hết hạn sau 30 ngày

#### 3. **Pydantic Models**
- `RegisterRequest` - Yêu cầu đăng ký
- `LoginRequest` - Yêu cầu đăng nhập
- `InterestRequest`, `LocationRequest`, `AlbumCreateRequest` - Models khác

#### 4. **API Endpoints**

##### 📝 **Đăng Ký**
```
POST /api/register
Content-Type: application/json

{
  "fullname": "Nguyễn Văn A",
  "email": "user@example.com",
  "password": "Password123",
  "phone": "0123456789"  # tuỳ chọn
}

Response:
{
  "success": true,
  "message": "Đăng ký thành công!",
  "user": {
    "id": 1,
    "fullname": "Nguyễn Văn A",
    "email": "user@example.com"
  }
}
```

##### 🔑 **Đăng Nhập**
```
POST /api/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123"
}

Response:
{
  "success": true,
  "message": "Đăng nhập thành công!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "fullname": "Nguyễn Văn A",
    "email": "user@example.com",
    "username": "user"
  }
}
```

##### 👤 **Lấy Hồ Sơ**
```
GET /api/user/profile
Authorization: Bearer <token>

Response:
{
  "success": true,
  "user": {
    "id": 1,
    "fullname": "Nguyễn Văn A",
    "email": "user@example.com",
    "phone": "0123456789",
    "username": "user",
    "created_at": "2025-11-16T10:30:00"
  }
}
```

##### 🚪 **Đăng Xuất**
```
POST /api/logout
Authorization: Bearer <token>

Response:
{
  "success": true,
  "message": "Đăng xuất thành công!"
}
```

### 📁 File Được Thay Đổi:

1. **backend/main.py**
   - ✅ Thêm imports: `jwt`, `hashlib`, `timedelta`
   - ✅ Thêm security: `HTTPBearer`, `HTTPAuthCredentials`
   - ✅ Thêm configuration: `SECRET_KEY`, `ALGORITHM`, etc.
   - ✅ Thêm helper functions cho user management
   - ✅ Thêm 4 authentication endpoints
   - ✅ Tích hợp JWT token verification

2. **backend/requirements.txt**
   - ✅ Thêm `PyJWT==2.8.1`

### 🔒 Bảo Mật:

1. **Password Hashing**: Sử dụng SHA256
2. **JWT Token**: Hết hạn sau 30 ngày
3. **CORS**: Được cấu hình để allow tất cả origins (dev)
4. **Dependency Injection**: Sử dụng Depends(verify_token) để bảo vệ endpoints

### 📊 Dữ Liệu Lưu Trữ:

- **Users.json**: Danh sách người dùng
  ```json
  {
    "users": [
      {
        "id": 1,
        "fullname": "Nguyễn Văn A",
        "email": "user@example.com",
        "phone": "0123456789",
        "password": "<hashed>",
        "created_at": "2025-11-16T...",
        "username": "user"
      }
    ]
  }
  ```

- **Users_album.json**: Album của mỗi người dùng
  ```json
  {
    "user@example.com": {
      "album_name": [...]
    }
  }
  ```

### 🚀 Cách Sử Dụng:

#### 1. **Cài Đặt Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

#### 2. **Chạy Server**
```bash
python main.py
```

Server sẽ chạy trên `http://localhost:8000`

#### 3. **Test API**
```bash
python test_api.py
```

### 🔄 Flow Đăng Ký/Đăng Nhập:

```
Frontend (React)
    ↓
1. User nhấn "Đăng ký" → SignupPage.js
    ↓
2. Submit form → API /api/register
    ↓
Backend (FastAPI)
    ↓
3. Kiểm tra email tồn tại
4. Hash password
5. Lưu user vào Users.json
    ↓
6. Return success
    ↓
Frontend
    ↓
7. Redirect sang LoginPage
    ↓
8. User nhấn "Đăng nhập"
    ↓
9. Submit form → API /api/login
    ↓
Backend
    ↓
10. Kiểm tra email & password
11. Tạo JWT token
12. Return token
    ↓
13. Frontend lưu token vào localStorage
14. Redirect sang HomePage
    ↓
Authenticated ✅
```

### 🎯 Features:

✅ Đăng ký tài khoản
✅ Đăng nhập
✅ Lấy thông tin hồ sơ
✅ Đăng xuất
✅ JWT Authentication
✅ Password Hashing
✅ User Album Management
✅ CORS Support
✅ Error Handling

### 📝 Notes:

1. **SECRET_KEY**: Nên thay đổi trong production
2. **Token Expiry**: 30 ngày (có thể thay đổi)
3. **Password**: Phải >= 6 ký tự
4. **Email**: Phải là unique

### 🔗 Kết Nối:

- React LoginPage.js → POST /api/login
- React SignupPage.js → POST /api/register
- Navbar profile menu → GET /api/user/profile
- Logout button → POST /api/logout

Tất cả đã sẵn sàng để hoạt động! 🎉
