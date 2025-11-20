# ⚠️ LƯU Ý QUAN TRỌNG

## Album Feature KHÔNG hoạt động khi mở trực tiếp file!

### ❌ SAI - Không làm thế này:
- Double-click vào `album.html`
- Mở file từ File Explorer
- URL dạng: `file:///D:/Logga/Nam2/web/react-travel-app/album.html`

**Lý do:** Browser chặn CORS khi mở từ `file://` protocol

---

## ✅ ĐÚNG - Làm thế này:

### Cách 1: Dùng Batch File (Khuyến nghị)
```
Double-click: START_ALL.bat
```

### Cách 2: Thủ công
**Terminal 1:**
```powershell
cd d:\Logga\Nam2\web\react-travel-app\backend
python main.py
```

**Terminal 2:**
```powershell
cd d:\Logga\Nam2\web\react-travel-app
python -m http.server 3000
```

**Browser:**
```
http://localhost:3000/album.html
```

---

## 🧪 Kiểm Tra Đang Mở Đúng Chưa?

Xem URL trong address bar:

- ❌ `file:///D:/Logga/...` → SAI
- ✅ `http://localhost:3000/album.html` → ĐÚNG

---

## 📋 Checklist

- [ ] Backend đang chạy (port 8000)
- [ ] Frontend server đang chạy (port 3000)
- [ ] Mở qua `http://localhost:3000/album.html`
- [ ] Thử upload 1-2 ảnh
- [ ] Xem progress bar chạy
- [ ] Album được tạo thành công

---

## 🆘 Vẫn Không Được?

1. Kiểm tra Console (F12)
2. Xem có lỗi đỏ không
3. Thử file debug: `http://localhost:3000/album_debug.html`
