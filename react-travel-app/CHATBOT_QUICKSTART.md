# 🤖 Travel Chatbot - Hướng Dẫn Nhanh

## ✨ Tính Năng Chatbot

Phần chatbot đã được tích hợp hoàn toàn vào dự án React Travel App:

### 1. **Backend Components**
- ✅ `backend/chatbot.py` - Lớp TravelChatbot chính
- ✅ `backend/main.py` - API endpoints cho chatbot
- ✅ Tích hợp `ai_recommend.py` để gợi ý địa điểm

### 2. **Frontend Components**
- ✅ `chatbot.html` - Giao diện chatbot đầy đủ
- ✅ Hỗ trợ AI Mode và Quick Mode
- ✅ Responsive design, hoạt động trên mobile/desktop

### 3. **API Endpoints**
```
POST   /api/chatbot/chat              - Gửi tin nhắn
GET    /api/chatbot/suggestions       - Lấy gợi ý nhanh
GET    /api/chatbot/history           - Lấy lịch sử
DELETE /api/chatbot/history           - Xóa lịch sử
POST   /api/chatbot/search            - Tìm kiếm nâng cao
GET    /api/chatbot/top-rated         - Lấy top destinations
```

## 🚀 Cách Khởi Động

### Bước 1: Khởi động Backend
```bash
cd react-travel-app/backend
python main.py
```

Server sẽ chạy tại: `http://localhost:8000`

### Bước 2: Mở Chatbot UI
- **Cách 1**: Mở file `react-travel-app/chatbot.html` trực tiếp trong trình duyệt
- **Cách 2**: Sử dụng Live Server (nếu có VS Code extension)
- **Cách 3**: Chạy web server

```bash
# Sử dụng Python web server
cd react-travel-app
python -m http.server 8001
# Mở: http://localhost:8001/chatbot.html
```

## 📖 Sử Dụng Chatbot

### Mode AI (Mặc định)
- Click nút "🤖 AI Mode"
- Sử dụng OpenAI GPT để hiểu và gợi ý thông minh
- Ví dụ: "Tôi muốn đi chơi ở nơi có lịch sử và văn hóa"

### Mode Quick
- Click nút "⚡ Quick Mode"
- Tìm kiếm nhanh dựa trên từ khóa
- Không cần API key
- Ví dụ: "chợ", "mua sắm", "biển"

### Gợi Ý Nhanh
- Sidebar bên trái có danh sách các tags phổ biến
- Click vào bất kỳ tag nào để tìm kiếm ngay

## 🧪 Test Chatbot

Chạy script test từ backend:
```bash
cd react-travel-app/backend
python test_chatbot.py
```

Kết quả mong đợi:
```
✅ Initializing chatbot...
✅ Loaded 21 destinations
✅ All tests passed!
```

## 📚 Tính Năng Chi Tiết

### 1. Chat với AI
```json
POST /api/chatbot/chat
{
    "message": "Tôi muốn mua sắm",
    "use_ai": true
}

Response:
{
    "status": "success",
    "message": "Tôi gợi ý...",
    "recommendations": [
        {
            "name": "Landmark 81",
            "location": "Bình Thạnh",
            "rating": 4.8,
            ...
        }
    ]
}
```

### 2. Lấy Gợi Ý Nhanh
```json
GET /api/chatbot/suggestions

Response:
{
    "status": "success",
    "suggestions": ["check-in", "lịch sử", "mua sắm", ...]
}
```

### 3. Tìm Kiếm Nâng Cao
```json
POST /api/chatbot/search
{
    "tags": ["mua sắm"],
    "min_price": 0,
    "max_price": 500000
}
```

### 4. Top Rated Destinations
```json
GET /api/chatbot/top-rated?limit=5

Response:
{
    "status": "success",
    "results": [
        {"name": "Landmark 81", "rating": 4.8},
        ...
    ]
}
```

## ⚙️ Cấu Hình

### Thêm API Key OpenAI (AI Mode)
Mở `react-travel-app/backend/ai_recommend.py`:
```python
client = OpenAI(api_key = "your-api-key-here")
```

### Đổi Thể Hiện UI
Chỉnh sửa `chatbot.html`:
```css
/* Thay đổi màu chính */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Thành */
background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
```

## 🔧 Troubleshooting

### ❌ Lỗi CORS
Kiểm tra `backend/main.py` có CORS middleware:
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```

### ❌ AI Mode không hoạt động
- Kiểm tra API key OpenAI
- Thử sử dụng Quick Mode thay vì AI Mode

### ❌ Không tìm thấy chatbot.html
Đảm bảo file nằm tại: `react-travel-app/chatbot.html`

## 📝 Cấu Trúc File

```
react-travel-app/
├── chatbot.html              # Giao diện chatbot
├── CHATBOT_GUIDE.md          # Hướng dẫn chi tiết
├── CHATBOT_QUICKSTART.md     # Hướng dẫn này
└── backend/
    ├── chatbot.py            # Lớp TravelChatbot
    ├── ai_recommend.py       # Hàm gợi ý AI
    ├── main.py               # API endpoints
    ├── test_chatbot.py       # Script test
    ├── database.json         # Dữ liệu địa điểm
    └── requirements.txt      # Dependencies
```

## 🎯 Ví Dụ Sử Dụng

### Ví dụ 1: Tìm Địa Điểm Mua Sắm
```
Bạn: "Tôi muốn đi mua sắm"
Bot: "Tôi tìm thấy 5 địa điểm phù hợp..."
     - Landmark 81 (⭐ 4.8/5)
     - Phố đi bộ Nguyễn Huệ (⭐ 4.6/5)
```

### Ví dụ 2: Tìm Địa Điểm Theo Giá
```
/api/chatbot/search
{
    "min_price": 0,
    "max_price": 100000
}
```

### Ví dụ 3: Tìm Top Rated
```
/api/chatbot/top-rated?limit=3
→ Trả về 3 địa điểm được đánh giá cao nhất
```

## 💡 Tips & Tricks

1. **Sử dụng từ khóa chính xác**: "chợ bến thành" cho kết quả tốt hơn "chợ"
2. **Kết hợp tags**: Click nhiều gợi ý nhanh để tìm kiếm chính xác hơn
3. **Kiểm tra rating**: Chọn địa điểm có rating cao nhất
4. **Lịch sử**: Xóa lịch sử khi muốn bắt đầu lại

## 🚀 Tiếp Theo

1. Tích hợp chatbot vào React frontend
2. Thêm real-time location recommendations
3. Lưu lịch sử cho từng user
4. Thêm hỗ trợ voice input/output
5. Tích hợp booking system

---

**Bất kỳ câu hỏi? Kiểm tra `CHATBOT_GUIDE.md` để biết thêm chi tiết!** 📚
