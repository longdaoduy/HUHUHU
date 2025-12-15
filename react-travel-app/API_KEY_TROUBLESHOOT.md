# 🔧 Hướng Dẫn Fix Lỗi Chatbot

## ❌ Lỗi: API key không hợp lệ (401)

### Vấn đề
Khi sử dụng AI Mode, nhận được lỗi:
```
Lỗi xác thực API: API key không hợp lệ hoặc đã hết hạn
```

### Nguyên nhân
1. API key không đúng
2. API key đã hết hạn
3. Tài khoản OpenAI bị disable
4. Không có credit trong tài khoản

### Cách Fix

#### Bước 1: Kiểm tra API key
1. Truy cập https://platform.openai.com/api-keys
2. Đăng nhập bằng tài khoản OpenAI
3. Kiểm tra API key của bạn
4. Nếu không tìm thấy, tạo API key mới

#### Bước 2: Cập nhật API key
Mở file `backend/ai_recommend.py` và tìm dòng:
```python
client = OpenAI(api_key = "sk-proj-...")
```

Thay thế bằng API key của bạn:
```python
client = OpenAI(api_key = "your-new-api-key-here")
```

⚠️ **LƯU Ý AN TOÀN**: 
- Không chia sẻ API key này với ai
- Không commit vào git nếu là project public
- Xem xét sử dụng environment variables thay vì hardcode

#### Bước 3: Sử dụng Environment Variables (Tùy chọn)

**Cách an toàn hơn:**

1. Tạo file `.env` trong thư mục `backend/`:
```
OPENAI_API_KEY=your-api-key-here
```

2. Cập nhật `ai_recommend.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

3. Cài đặt dependency:
```bash
pip install python-dotenv
```

#### Bước 4: Test API key
Chạy test script:
```bash
python debug_chatbot.py
```

Nếu thành công, sẽ thấy:
```
✅ AI Response received!
```

## ✅ Giải pháp thay thế: Sử dụng Quick Mode

Nếu không muốn/không thể sử dụng OpenAI API, có thể sử dụng **Quick Mode**:

1. Mở `chatbot.html`
2. Click vào nút "⚡ Quick Mode"
3. Chatbot sẽ sử dụng tìm kiếm từ khóa thông thường (không cần API)

### So sánh:

| Feature | AI Mode | Quick Mode |
|---------|---------|-----------|
| Cần API? | ✅ Có | ❌ Không |
| Độ chính xác | Cao | Trung bình |
| Tốc độ | Chậm (1-3s) | Nhanh (<100ms) |
| Chi phí | ✅ Có | Miễn phí |

## 🔍 Debug Logs

Để xem chi tiết lỗi, chạy:
```bash
python debug_chatbot.py
```

Output sẽ cho thấy:
- ✅ Dữ liệu được load
- ✅ Chatbot khởi tạo
- ✅ Quick Mode test
- ⚠️ AI Mode errors (nếu có)

## 📞 Hỗ trợ thêm

Nếu vẫn có vấn đề:

1. **Kiểm tra lại API key**: https://platform.openai.com/api-keys
2. **Kiểm tra billing**: https://platform.openai.com/account/billing/overview
3. **Kiểm tra status**: https://status.openai.com/

## 💡 Tips

1. Quick Mode hoạt động tốt để demo
2. AI Mode cần API key nhưng kết quả tốt hơn
3. Có thể kết hợp cả hai mode

---

**Nếu lỗi vẫn tiếp tục, thử Quick Mode để tận dụng chatbot!**
