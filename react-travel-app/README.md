# 🇻🇳 Vietnam UrbanQuest - AI-Powered Travel Companion

Ứng dụng web du lịch Việt Nam thông minh sử dụng AI để nhận dạng địa danh, gợi ý điểm tham quan và quản lý album ảnh.

> **📌 Cập nhật mới nhất:** Backend và Frontend đã được tích hợp đầy đủ các chức năng từ demo.py
> - ✅ Nhận dạng ảnh hoàn chỉnh (landmark + location)
> - ✅ Gợi ý địa điểm theo sở thích và AI
> - ✅ Quản lý album với tự động nhận dạng
> - ✅ Download ZIP, thống kê, nhóm theo địa danh
> 
> Xem chi tiết trong [CHANGES.md](CHANGES.md) và [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🚀 Quick Start

```bash
# 1. Cài đặt dependencies
cd backend
pip install -r requirements.txt

# 2. Chạy backend
python main.py

# 3. Mở index.html trong trình duyệt
# Backend: http://localhost:8000
# Frontend: Mở file HTML hoặc dùng Live Server
```

## ✨ Tính năng chính

### 🔍 Nhận dạng ảnh thông minh (Scan)
- Nhận dạng địa danh từ ảnh bằng OpenAI GPT-4o Vision
- Trích xuất vị trí GPS từ EXIF data  
- Phát hiện địa điểm tự động bằng AI
- Kết quả chi tiết với độ tin cậy (confidence)

### 🎯 Gợi ý địa điểm du lịch (Recommendation)
- **Tìm theo sở thích**: Nhập từ khóa (biển, núi, văn hóa, lịch sử...)
- **AI Recommendations**: ChatGPT phân tích và đề xuất
- **Tìm kiếm gần đây**: Dựa trên GPS location và bán kính
- Hiển thị thông tin chi tiết: rating, giá cả, review
- Quick tags để tìm kiếm nhanh

### 📸 Quản lý Album ảnh (Album)
- Tạo và quản lý nhiều album
- Upload nhiều ảnh cùng lúc
- Tự động nhận dạng địa danh cho mỗi ảnh
- Nhóm ảnh theo địa danh
- Download album dưới dạng ZIP

## Cấu trúc dự án

```
react-travel-app/
├── backend/               # Backend API (FastAPI)
│   ├── main.py           # FastAPI server chính
│   ├── recognize.py      # Module nhận diện ảnh
│   ├── ai_recommend.py   # Module đề xuất du lịch
│   ├── album_manager.py  # Module quản lý album
│   ├── database.json     # Database đơn giản
│   └── requirements.txt  # Dependencies Python
├── index.html            # Frontend chính
├── script.js            # JavaScript logic
├── start_app.bat        # Script khởi động ứng dụng
└── start_backend.bat    # Script khởi động backend
```

## Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8 trở lên
- OpenAI API key
- Internet connection

### Bước 1: Cấu hình OpenAI API
1. Tạo file `.env` trong thư mục `backend/`
2. Thêm OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### Bước 2: Khởi động ứng dụng
**Cách 1: Khởi động tự động (khuyến nghị)**
```bash
# Chạy script tự động
start_app.bat
```

**Cách 2: Khởi động thủ công**
```bash
# Terminal 1: Khởi động backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Terminal 2: Mở frontend
# Mở file index.html trong trình duyệt
```

## Cách sử dụng

### 1. Nhận diện ảnh
1. Chọn tab "Scan image"
2. Upload ảnh bằng cách drag & drop hoặc click "Browse files"
3. Click "Scan image" để phân tích
4. Xem kết quả nhận diện và click "Get Recommendations" để lấy đề xuất

### 2. Tìm đề xuất du lịch
1. Chọn tab "Recommendation"  
2. Nhập sở thích (ví dụ: "beach, culture, food")
3. Click "Search" để lấy đề xuất
4. Click "View Detail" để xem thông tin chi tiết

### 3. Quản lý Album
1. Chọn tab "Album"
2. Nhập tên album
3. Upload ảnh bằng drag & drop
4. Click "Add to album" để tạo album
5. Sử dụng "Download" để tải album hoặc "Delete" để xóa

## API Endpoints

### Nhận diện ảnh
- `POST /recognize` - Upload và nhận diện ảnh
- `POST /recognize/batch` - Nhận diện nhiều ảnh

### Đề xuất du lịch
- `GET /recommend` - Lấy đề xuất theo sở thích
- `GET /recommend/nearby` - Tìm địa điểm gần
- `POST /recommend/ai` - Đề xuất bằng AI

### Quản lý Album
- `GET /albums` - Lấy danh sách album
- `POST /albums` - Tạo album mới
- `GET /albums/{id}` - Lấy thông tin album
- `DELETE /albums/{id}` - Xóa album
- `GET /albums/{id}/download` - Download album

## Công nghệ sử dụng

### Backend
- **FastAPI**: Web framework hiệu suất cao
- **OpenAI GPT-4 Vision**: AI nhận diện ảnh và mô tả
- **Pillow**: Xử lý ảnh
- **ExifRead**: Đọc metadata ảnh
- **Geopy**: Xử lý địa lý và geocoding

### Frontend  
- **HTML5 + CSS3**: Giao diện responsive
- **TailwindCSS**: CSS framework
- **Vanilla JavaScript**: Logic frontend
- **Font Awesome**: Icon library

## Khắc phục sự cố

### Lỗi thường gặp

**1. Lỗi "OpenAI API key not found"**
```bash
# Giải pháp: Tạo file .env với API key
echo OPENAI_API_KEY=your_key > backend/.env
```

**2. Lỗi "Module not found"**
```bash
# Giải pháp: Cài đặt dependencies
cd backend
pip install -r requirements.txt
```

**3. Lỗi CORS khi gọi API**
```bash
# Giải pháp: Khởi động backend trước, sau đó mở frontend
```

**4. Lỗi upload file quá lớn**
- Giới hạn file: 10MB
- Format hỗ trợ: JPG, PNG, GIF, WebP

### Logs và debugging
- Backend logs: Xem trong terminal chạy uvicorn
- Frontend errors: Mở Developer Tools (F12) trong browser
- API testing: Truy cập http://localhost:8000/docs

## Phát triển thêm

### Thêm tính năng mới
1. Tạo endpoint mới trong `main.py`
2. Cập nhật frontend trong `script.js`
3. Test qua Swagger UI tại `/docs`

### Tùy chỉnh AI model
- Chỉnh sửa prompts trong `recognize.py`
- Cập nhật scoring algorithm trong `ai_recommend.py`

## Liên hệ hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần "Khắc phục sự cố" ở trên
2. Xem logs để tìm lỗi cụ thể  
3. Đảm bảo đã cài đặt đúng requirements

---
**Vietnam UrbanQuest** - Khám phá Việt Nam thông minh với AI