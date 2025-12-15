# Travel Chatbot - Hướng Dẫn Sử Dụng

## 📋 Giới Thiệu

Phần chatbot du lịch thông minh đã được tích hợp vào ứng dụng React Travel App. Chatbot sử dụng:
- **AI Mode**: Sử dụng OpenAI GPT để gợi ý địa điểm thông minh
- **Quick Mode**: Sử dụng matching nhanh với các tags và tên địa điểm

## 🏗️ Cấu Trúc Tệp

### Backend (Python)

1. **`backend/chatbot.py`** - Module chatbot chính
   - Lớp `TravelChatbot` với các phương thức:
     - `chat()` - Xử lý tin nhắn từ người dùng
     - `get_conversation_history()` - Lấy lịch sử cuộc trò chuyện
     - `search_by_tags()` - Tìm kiếm theo tags
     - `search_by_price_range()` - Tìm kiếm theo giá
     - `get_top_rated()` - Lấy những địa điểm đánh giá cao nhất

2. **`backend/ai_recommend.py`** - Module gợi ý
   - `loadDestination()` - Tải dữ liệu địa điểm
   - `recommend()` - Gợi ý dựa trên từ khóa (Quick Mode)
   - `ai_recommend()` - Gợi ý thông minh bằng AI (AI Mode)
   - `compatibality_rate()` - Tính độ tương thích

3. **`backend/main.py`** - API endpoints
   - `POST /api/chatbot/chat` - Gửi tin nhắn
   - `GET /api/chatbot/suggestions` - Lấy gợi ý nhanh
   - `GET /api/chatbot/history` - Lấy lịch sử
   - `DELETE /api/chatbot/history` - Xóa lịch sử
   - `POST /api/chatbot/search` - Tìm kiếm nâng cao
   - `GET /api/chatbot/top-rated` - Lấy top địa điểm

### Frontend (HTML)

**`chatbot.html`** - Giao diện chatbot đầy đủ
- Sidebar với gợi ý nhanh
- Chat messages area
- Input area với mode toggle
- Responsive design

## 🚀 Cách Sử Dụng

### 1. Khởi động Backend

```bash
cd backend
python main.py
```

Server sẽ chạy trên `http://localhost:8000`

### 2. Mở Chatbot Interface

Mở file `chatbot.html` trong trình duyệt hoặc sử dụng Live Server

### 3. Sử Dụng Chatbot

#### AI Mode (Mặc định)
- Sử dụng OpenAI API để gợi ý thông minh
- Hiểu được ý định của người dùng tốt hơn
- Cần API key từ OpenAI

#### Quick Mode
- Sử dụng regex matching nhanh chóng
- Không cần API
- Phù hợp khi API không khả dụng

## 📡 API Endpoints

### 1. Chat với Chatbot
```http
POST /api/chatbot/chat
Content-Type: application/json

{
    "message": "Tôi muốn đi mua sắm",
    "use_ai": true
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Tôi đã tìm thấy 3 địa điểm phù hợp...",
    "use_ai": true,
    "recommendations": [
        {
            "name": "Chợ Bến Thành",
            "location": "Quận 1, TP.HCM",
            "introduction": "Chợ nổi tiếng...",
            "price": "Miễn phí",
            "rating": 4.5,
            "images": []
        }
    ]
}
```

### 2. Lấy Gợi Ý Nhanh
```http
GET /api/chatbot/suggestions
```

**Response:**
```json
{
    "status": "success",
    "suggestions": ["mua sắm", "ăn uống", "du lịch", ...]
}
```

### 3. Lấy Lịch Sử Trò Chuyện
```http
GET /api/chatbot/history
```

**Response:**
```json
{
    "status": "success",
    "history": [
        {
            "timestamp": "2024-11-20T10:30:00",
            "user": "Tôi muốn đi chợ",
            "type": "user"
        },
        {
            "timestamp": "2024-11-20T10:30:05",
            "assistant": "Tôi gợi ý...",
            "type": "assistant"
        }
    ]
}
```

### 4. Xóa Lịch Sử
```http
DELETE /api/chatbot/history
```

### 5. Tìm Kiếm Nâng Cao
```http
POST /api/chatbot/search
Content-Type: application/json

{
    "tags": ["mua sắm", "ăn uống"],
    "min_price": 0,
    "max_price": 500000
}
```

### 6. Lấy Top Địa Điểm Đánh Giá Cao
```http
GET /api/chatbot/top-rated?limit=5
```

## 🔧 Cài Đặt

### Python Requirements
Thêm vào `backend/requirements.txt`:
```
openai>=1.0.0
unidecode
fastapi
uvicorn
pydantic
```

### Cấu Hình OpenAI API

Mở `backend/ai_recommend.py` và thêm API key:
```python
client = OpenAI(api_key = "your-api-key-here")
```

## 🎨 Tùy Chỉnh

### Thay Đổi Màu Sắc (chatbot.html)
```css
/* Thay đổi gradient chính */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Hoặc thay đổi thành màu khác */
background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
```

### Thay Đổi Số Lượng Gợi Ý Tối Đa
Trong `backend/chatbot.py`:
```python
def get_quick_suggestions(self) -> List[str]:
    # ...
    return [tag for tag, count in sorted_tags[:10]]  # Thay 10 bằng số khác
```

### Thay Đổi Số Lượng Kết Quả Gợi Ý
Trong `backend/ai_recommend.py`:
```python
def recommend(preference, destination):
    # ...
    return [d[0] for d in results[:5]]  # Thay 5 bằng số khác
```

## 🐛 Troubleshooting

### 1. Lỗi CORS
**Vấn đề**: Frontend không thể kết nối backend
**Giải pháp**: Đảm bảo CORS đã được cấu hình trong `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Lỗi AI Mode
**Vấn đề**: Chatbot không phản hồi ở AI Mode
**Giải pháp**: Kiểm tra OpenAI API key:
- Mở `backend/ai_recommend.py`
- Thêm API key hợp lệ

### 3. Lỗi Module Not Found
**Vấn đề**: Không tìm thấy module chatbot
**Giải pháp**: Đảm bảo file `chatbot.py` đã được tạo trong thư mục `backend/`

## 📊 Ví Dụ Sử Dụng

### Ví Dụ 1: Tìm Địa Điểm Mua Sắm
```
Người dùng: "Tôi muốn đi chợ"
Chatbot: "Tôi tìm thấy Chợ Bến Thành - một chợ nổi tiếng..."
```

### Ví Dụ 2: Tìm Theo Giá
```
API Call: POST /api/chatbot/search
{
    "min_price": 0,
    "max_price": 100000
}
Response: [Các địa điểm có giá dưới 100.000 VNĐ]
```

### Ví Dụ 3: Top Rated
```
API Call: GET /api/chatbot/top-rated?limit=3
Response: [3 địa điểm được đánh giá cao nhất]
```

## 📝 Lưu Ý Quan Trọng

1. **API Key**: Không nên commit API key vào repository. Sử dụng environment variables.

2. **Hiệu Năng**: Khi database lớn, cân nhắc sử dụng caching.

3. **Bảo Mật**: Thêm authentication nếu sử dụng trong production.

4. **Dữ Liệu**: Đảm bảo `database.json` tồn tại và có định dạng đúng.

## 🔮 Tính Năng Tương Lai

- [ ] Lưu lịch sử từng user
- [ ] Chatbot tìm hiểu từng user (machine learning)
- [ ] Real-time location-based recommendations
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration với booking system

---

**Được phát triển bởi Travel App Team**
