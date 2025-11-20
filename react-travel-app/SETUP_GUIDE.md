# 🚀 Quick Setup Guide - Authentication System

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Hoặc nếu PyJWT chưa được cài:
```bash
pip install PyJWT==2.8.1
```

## Step 2: Start Backend Server

```bash
python main.py
```

Backend server sẽ chạy trên: `http://localhost:8000`

## Step 3: Start Frontend (React)

```bash
cd ../frontend
npm start
```

Frontend sẽ chạy trên: `http://localhost:3000`

## Step 4: Test Authentication

### Đăng Ký:
1. Click icon người dùng → "Đăng ký"
2. Nhập thông tin:
   - Họ và Tên: "Nguyễn Văn A"
   - Email: "test@example.com"
   - Số điện thoại: "0123456789" (tuỳ chọn)
   - Mật khẩu: "Test123456"
3. Click "Đăng Ký"
4. Được redirect sang trang Đăng nhập

### Đăng Nhập:
1. Nhập Email: "test@example.com"
2. Nhập Mật khẩu: "Test123456"
3. Click "Đăng Nhập"
4. Token được lưu vào localStorage
5. Được redirect sang trang chủ

### Kiểm Tra Đăng Nhập:
1. Icon người dùng sẽ hiển thị email
2. Click vào sẽ thấy dropdown menu:
   - Xin chào! test@example.com
   - Hồ sơ
   - Cài đặt
   - Yêu thích
   - Đăng xuất

## API Endpoints

### Authentication
- `POST /api/register` - Đăng ký
- `POST /api/login` - Đăng nhập
- `POST /api/logout` - Đăng xuất
- `GET /api/user/profile` - Lấy hồ sơ

### Existing Features
- `POST /api/recognize/landmark` - Nhận diện địa danh
- `POST /api/recommend/interest` - Gợi ý theo sở thích
- `POST /api/albums` - Tạo album
- Và nhiều endpoints khác...

## File Structure

```
react-travel-app/
├── backend/
│   ├── main.py (✅ Tích hợp login.py)
│   ├── login.py (✅ Source functions)
│   ├── requirements.txt (✅ PyJWT thêm vào)
│   ├── Users.json (📁 Được tạo tự động)
│   ├── Users_album.json (📁 Được tạo tự động)
│   └── test_api.py (🧪 Test script)
│
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── LoginPage.js (✅ Mới)
│       │   ├── SignupPage.js (✅ Mới)
│       │   └── ...
│       ├── App.js (✅ Tích hợp routes)
│       └── ...
│
└── AUTHENTICATION_INTEGRATION.md (📖 Documentation)
```

## Data Storage

### Users.json
```json
{
  "users": [
    {
      "id": 1,
      "fullname": "Nguyễn Văn A",
      "email": "test@example.com",
      "phone": "0123456789",
      "password": "sha256_hash",
      "created_at": "2025-11-16T...",
      "username": "test"
    }
  ]
}
```

### Users_album.json
```json
{
  "test@example.com": {
    "Du Lịch HN": [
      {
        "filename": "image.jpg",
        "bytes": "base64_encoded",
        "uploaded_at": "..."
      }
    ]
  }
}
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'jwt'"
**Fix:**
```bash
pip install PyJWT==2.8.1
```

### Error: "CORS error"
**Solution:** CORS đã được cấu hình trong main.py, restart server

### Error: "Email không tồn tại" khi đăng nhập
**Solution:** Hãy đăng ký tài khoản trước

### Token không hoạt động
**Solution:** Token hết hạn sau 30 ngày, hãy đăng nhập lại

## Security Notes

1. **SECRET_KEY**: Hiện tại là "your-secret-key-change-in-production"
   - Đổi thành key mạnh trong production:
   ```python
   SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
   ```

2. **Password Hashing**: SHA256 (có thể upgrade sang bcrypt)
   ```bash
   pip install bcrypt
   ```

3. **HTTPS**: Dùng HTTPS trong production

4. **CORS**: Cấu hình domain cụ thể trong production

## Features Checklist

- ✅ Register endpoint
- ✅ Login endpoint
- ✅ Logout endpoint
- ✅ Get Profile endpoint
- ✅ JWT Token generation
- ✅ Password hashing
- ✅ User data persistence
- ✅ Album management per user
- ✅ React LoginPage component
- ✅ React SignupPage component
- ✅ Navbar authentication menu
- ✅ localStorage integration
- ✅ Token refresh logic
- ✅ Auto-redirect for protected routes

## Next Steps

1. ✅ **Done:** Backend authentication setup
2. ✅ **Done:** Frontend authentication pages
3. **TODO:** Add "Forgot Password" feature
4. **TODO:** Add email verification
5. **TODO:** Add Google/Facebook OAuth
6. **TODO:** Add refresh token mechanism
7. **TODO:** Add role-based access control
8. **TODO:** Add audit logging

## Contact & Support

Mọi vấn đề hãy kiểm tra:
1. Backend server đang chạy?
2. Frontend server đang chạy?
3. Database files có tồn tại?
4. PyJWT đã được cài đặt?

Happy coding! 🎉
