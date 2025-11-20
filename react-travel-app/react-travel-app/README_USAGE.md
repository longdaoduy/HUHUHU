# 🚀 Hướng Dẫn Chạy Ứng Dụng Vietnam UrbanQuest

## ✅ Cách Khởi Động Ứng Dụng

### **Phương Pháp 1: Sử dụng QUICK_START.bat (Khuyến nghị)**

1. **Nhấp đúp vào file** `QUICK_START.bat`
2. Ứng dụng sẽ tự động:
   - Kiểm tra và khởi động Backend API Server (port 8000)
   - Mở trang chủ trong trình duyệt mặc định
3. **Bắt đầu sử dụng!**

### **Phương Pháp 2: Khởi động thủ công**

#### Bước 1: Khởi động Backend Server
```bash
cd backend
python main.py
```
Server sẽ chạy tại: `http://localhost:8000`

#### Bước 2: Mở Trang Web
Nhấp đúp vào một trong các file HTML:
- `index.html` - Trang chủ
- `login.html` - Đăng nhập
- `signup.html` - Đăng ký
- `about-us.html` - Về chúng tôi
- `information.html` - Thông tin dự án

---

## 📝 Hướng Dẫn Sử Dụng

### 1️⃣ Đăng Ký Tài Khoản

1. Mở file `signup.html` hoặc click "Đăng ký" trên trang chủ
2. Điền thông tin:
   - **Họ tên**: Tên đầy đủ của bạn
   - **Email**: Địa chỉ email (ví dụ: user@example.com)
   - **Số điện thoại**: Tùy chọn
   - **Mật khẩu**: Ít nhất 6 ký tự
   - **Xác nhận mật khẩu**: Nhập lại mật khẩu
3. Đồng ý với Điều khoản dịch vụ
4. Click **"Đăng Ký"**
5. Sau khi thành công, bạn sẽ được chuyển đến trang đăng nhập

### 2️⃣ Đăng Nhập

1. Mở file `login.html` hoặc click "Đăng nhập"
2. Nhập:
   - **Email**: Email bạn đã đăng ký
   - **Mật khẩu**: Mật khẩu của bạn
3. Click **"Đăng Nhập"**
4. Sau khi đăng nhập thành công, bạn sẽ được chuyển về trang chủ

### 3️⃣ Sử Dụng Các Tính Năng

- **🗺️ Recommendation**: Nhận gợi ý địa điểm du lịch theo sở thích
- **📷 Scan Image**: Nhận diện địa danh từ ảnh
- **📁 Album**: Quản lý album ảnh du lịch

---

## ⚙️ Yêu Cầu Hệ Thống

### Backend Server (bắt buộc):
- Python 3.8+
- Các thư viện trong `backend/requirements.txt`:
  ```
  fastapi
  uvicorn
  pillow
  pyjwt
  python-multipart
  ```

### Cài đặt dependencies:
```bash
cd backend
pip install -r requirements.txt
```

---

## 🔧 Khắc Phục Sự Cố

### ❌ Lỗi: "Lỗi kết nối máy chủ"

**Nguyên nhân**: Backend server chưa chạy hoặc chạy trên port khác

**Giải pháp**:
1. Kiểm tra backend có đang chạy không:
   ```bash
   curl http://localhost:8000/
   ```
   Nếu thành công, sẽ thấy: `{"message":"Vietnam Travel App API"}`

2. Nếu không chạy, khởi động lại:
   ```bash
   cd backend
   python main.py
   ```

### ❌ Lỗi: "POST method not supported" (501)

**Nguyên nhân**: Bạn đang dùng Python's `http.server` đơn giản không hỗ trợ POST

**Giải pháp**: 
- **KHÔNG dùng** `python -m http.server` để mở frontend
- Mở file HTML trực tiếp bằng cách nhấp đúp
- Hoặc dùng `QUICK_START.bat`

### ❌ Lỗi: "CORS policy"

**Nguyên nhân**: Trình duyệt chặn request cross-origin

**Giải pháp**:
1. Backend đã cấu hình CORS với `allow_origins=["*"]`
2. Đảm bảo mở file HTML từ file system (file:///) hoặc localhost
3. Nếu vẫn lỗi, thử trình duyệt khác (Chrome/Firefox/Edge)

### ❌ Không đăng ký/đăng nhập được

**Kiểm tra**:
1. Mở Developer Tools (F12) → Console
2. Xem lỗi trong console
3. Kiểm tra Network tab xem request có được gửi không

**Giải pháp**:
1. Đảm bảo backend đang chạy
2. Kiểm tra URL API trong code là `http://localhost:8000`
3. Thử với tài khoản khác nếu email đã tồn tại

---

## 📊 Cấu Trúc API

### Authentication APIs:
- `POST /api/register` - Đăng ký tài khoản
- `POST /api/login` - Đăng nhập
- `POST /api/logout` - Đăng xuất (cần token)
- `GET /api/user/profile` - Lấy thông tin user (cần token)

### Recommendation APIs:
- `POST /api/recommend/interest` - Gợi ý theo sở thích
- `POST /api/recommend/ai` - Gợi ý bằng AI
- `POST /api/recommend/nearby` - Gợi ý địa điểm gần
- `GET /api/destinations` - Lấy tất cả địa điểm

### Image Recognition APIs:
- `POST /api/recognize/landmark` - Nhận diện địa danh
- `POST /api/recognize/location` - Nhận diện vị trí

### Album APIs:
- `POST /api/albums` - Tạo album
- `GET /api/albums` - Lấy danh sách album
- `DELETE /api/albums/{name}` - Xóa album
- `POST /api/albums/{name}/images` - Thêm ảnh vào album

---

## 📁 Cấu Trúc Thư Mục

```
react-travel-app/
├── backend/
│   ├── main.py              # FastAPI server chính
│   ├── login.py             # Xử lý authentication (Streamlit)
│   ├── recognize.py         # Nhận diện ảnh
│   ├── ai_recommend.py      # Gợi ý địa điểm
│   ├── album_manager.py     # Quản lý album
│   ├── requirements.txt     # Dependencies Python
│   ├── Users.json           # Database người dùng
│   └── Users_album.json     # Database album
├── index.html               # Trang chủ
├── login.html               # Trang đăng nhập
├── signup.html              # Trang đăng ký
├── about-us.html            # Trang về nhóm
├── information.html         # Trang thông tin dự án
├── recommendation.html      # Trang gợi ý
├── scan.html                # Trang quét ảnh
├── album.html               # Trang album
├── auth-modal.js            # JavaScript xử lý auth
├── QUICK_START.bat          # Script khởi động nhanh
└── README_USAGE.md          # File này
```

---

## 💡 Tips & Tricks

### Đăng nhập tự động
Sau khi đăng nhập thành công, token sẽ được lưu trong `localStorage`. Bạn sẽ tự động đăng nhập khi mở lại trang.

### Đăng xuất
Click vào biểu tượng user ở góc phải → "Đăng xuất"

### Kiểm tra trạng thái đăng nhập
Mở Console (F12) và chạy:
```javascript
console.log(localStorage.getItem('authToken'));
console.log(localStorage.getItem('userEmail'));
```

### Test API trực tiếp
Sử dụng file `test-register.html` để test API đăng ký nhanh

---

## 👥 Hỗ Trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra lại các bước trong mục "Khắc Phục Sự Cố"
2. Xem log trong console (F12)
3. Kiểm tra terminal backend có lỗi không

---

## 🎯 Phát Triển Bởi

**Nhóm 6 - Vietnam UrbanQuest**

6 thành viên:
- Nguyễn Văn A - Team Leader & Backend Developer
- Trần Thị B - Frontend Developer
- Lê Văn C - AI/ML Engineer
- Phạm Thị D - Database Administrator
- Hoàng Văn E - UI/UX Designer
- Vũ Thị F - Content Manager & Tester

---

**Chúc bạn có trải nghiệm tuyệt vời với Vietnam UrbanQuest! 🇻🇳✨**
