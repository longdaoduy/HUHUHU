# Hướng Dẫn Chuyển Đổi Sang OpenAI API

## ✅ Đã Hoàn Thành

Backend đã được chỉnh sửa để sử dụng **OpenAI API** thay vì local model.

## 📋 Các Thay Đổi

### 1. **ai_recommend.py**
- ✅ Import `OpenAI` client từ thư viện `openai`
- ✅ Khởi tạo OpenAI client với API key từ `.env`
- ✅ Hàm `ai_recommend()` giờ sử dụng `gpt-3.5-turbo` để gợi ý địa điểm

### 2. **recognize.py**
- ✅ Import `OpenAI` client
- ✅ Hàm `get_image_analysis()` sử dụng OpenAI Vision API (`gpt-4o-mini`)
- ✅ Hàm `get_landmark_from_image()` nhận dạng địa danh qua OpenAI
- ✅ Hàm `get_landmark_with_confidence()` trả về JSON với thông tin chi tiết
- ✅ Hàm `detect_landmark_strict()` thử nhiều lần với OpenAI API
- ✅ Hàm `detect_location()` sử dụng OpenAI khi không có GPS

### 3. **Các File Phụ Trợ**
- ✅ Tạo file `.env.example` làm mẫu cho cấu hình API key

## 🔧 Cách Cài Đặt

### Bước 1: Lấy OpenAI API Key

1. Truy cập: https://platform.openai.com/api-keys
2. Đăng nhập hoặc tạo tài khoản
3. Tạo API key mới
4. Copy API key

### Bước 2: Cấu Hình API Key

Tạo file `.env` trong thư mục `backend/`:

```bash
cd backend
copy .env.example .env
```

Mở file `.env` và thêm API key:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install openai>=1.0.0
```

Hoặc cài đặt tất cả:

```bash
pip install -r requirements.txt
```

### Bước 4: Kiểm Tra

Chạy test để kiểm tra kết nối:

```python
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Test API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

## 📊 So Sánh Local Model vs OpenAI API

| Tính Năng | Local Model | OpenAI API |
|-----------|-------------|------------|
| **Chi Phí** | Miễn phí | Tính phí theo token |
| **Độ Chính Xác** | Trung bình | Rất cao |
| **Tốc Độ** | Nhanh (local) | Phụ thuộc mạng |
| **Yêu Cầu** | TensorFlow, EasyOCR | API key |
| **Ngôn Ngữ** | Tiếng Anh chủ yếu | Đa ngôn ngữ tốt |
| **Nhận Dạng Ảnh** | ImageNet classes | Vision AI |

## 💰 Chi Phí OpenAI API

### Giá GPT-3.5-turbo (cho chatbot):
- Input: $0.50 / 1M tokens
- Output: $1.50 / 1M tokens

### Giá GPT-4o-mini (cho nhận dạng ảnh):
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens
- **Ảnh**: $0.001225 / ảnh (1024×1024)

### Ví dụ Chi Phí:
- 100 lần chatbot: ~$0.05
- 100 lần nhận dạng ảnh: ~$0.15

## ⚠️ Lưu Ý

1. **Bảo Mật API Key**: Không commit file `.env` lên Git
2. **Rate Limits**: OpenAI có giới hạn requests/phút
3. **Error Handling**: Code đã xử lý lỗi khi API không khả dụng
4. **Fallback**: Nếu OpenAI lỗi, hệ thống sẽ trả về thông báo lỗi rõ ràng

## 🐛 Troubleshooting

### Lỗi: "OPENAI_API_KEY not found"
- Kiểm tra file `.env` có tồn tại trong thư mục `backend/`
- Kiểm tra API key đã được thêm đúng format

### Lỗi: "Rate limit exceeded"
- Đợi 1 phút rồi thử lại
- Xem xét nâng cấp plan OpenAI

### Lỗi: "Invalid API key"
- API key đã hết hạn hoặc không hợp lệ
- Tạo API key mới tại https://platform.openai.com/api-keys

## 🔄 Quay Lại Local Model

Nếu muốn quay lại sử dụng local model, chỉnh sửa:

1. Trong `ai_recommend.py`: Đổi `USE_LOCAL_AI = False` thành `True`
2. Trong `recognize.py`: Import lại các hàm từ `local_ai.py`

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra console output để xem log chi tiết
2. Kiểm tra file `.env` đã được load đúng
3. Test kết nối OpenAI API trước khi chạy app

---

**Cập nhật**: November 26, 2025
