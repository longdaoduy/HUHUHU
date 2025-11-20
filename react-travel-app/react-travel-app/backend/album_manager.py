import json
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont
import textwrap
import streamlit as st

def zip_album(album_name, items):
    """Tạo file ZIP chứa tất cả ảnh trong album."""
    buf = BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
        for item in items:
            zf.writestr(item["filename"], item["bytes"])
    buf.seek(0)
    return buf

def create_pdf_album(album_items):
    """Tạo file PDF từ album ảnh với thông tin chi tiết."""
    if not album_items:
        return None

    try:
        # Thử tải font hỗ trợ Unicode.
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
        font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except IOError:
        # Fallback nếu không tìm thấy font
        if 'st' in globals():
            st.warning("Không tìm thấy font 'DejaVuSans', sử dụng font mặc định (có thể lỗi tiếng Việt).")
        font = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    pages = []
    A4_SIZE = (595, 842) # Kích thước A4 theo pixel (72 dpi)
    MARGIN = 40

    for item in album_items:
        # Tạo trang A4 trắng
        page = Image.new('RGB', A4_SIZE, 'white')
        draw = ImageDraw.Draw(page)

        # Tải ảnh
        img = Image.open(BytesIO(item["bytes"]))
        
        # Resize ảnh để vừa trang, giữ tỷ lệ
        img_width, img_height = img.size
        max_width = A4_SIZE[0] - 2 * MARGIN
        max_height = A4_SIZE[1] // 2 # Dành nửa trên cho ảnh
        
        ratio = min(max_width / img_width, max_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Canh giữa ảnh
        img_x = (A4_SIZE[0] - new_size[0]) // 2
        img_y = MARGIN
        page.paste(img, (img_x, img_y))

        # Thêm metadata
        current_y = img_y + new_size[1] + 30 # Vị trí bắt đầu viết text

        # Địa danh
        draw.text((MARGIN, current_y), "Địa danh:", font=font_bold, fill="black")
        current_y += 30
        landmark_lines = textwrap.wrap(item.get('landmark', 'N/A'), width=80)
        for line in landmark_lines:
            draw.text((MARGIN, current_y), line, font=font, fill="black")
            current_y += 20
        
        current_y += 20 # Khoảng cách
        
        # Tên file và ngày
        footer_text = f"{item['filename']} | {datetime.fromisoformat(item['uploaded_at']).strftime('%Y-%m-%d %H:%M')}"
        draw.text((MARGIN, A4_SIZE[1] - MARGIN), footer_text, font=font, fill="gray")

        pages.append(page)

    if not pages:
        return None

    # Lưu PDF vào bộ nhớ
    pdf_buf = BytesIO()
    pages[0].save(pdf_buf, "PDF", resolution=100.0, save_all=True, append_images=pages[1:])
    pdf_buf.seek(0)
    return pdf_buf

def create_album_item(filename, file_bytes, album_name, landmark=None, description=None):
    """Tạo một item album với metadata đầy đủ."""
    return {
        "filename": filename,
        "bytes": file_bytes,
        "uploaded_at": datetime.now().isoformat(),
        "album_name": album_name,
        "landmark": landmark or "N/A",
        "description": description or ""
    }

def add_images_to_album(album_storage, album_name, files, recognize_function=None):
    """
    Thêm nhiều ảnh vào album với tự động nhận dạng.
    
    Args:
        album_storage: Dictionary chứa các album
        album_name: Tên album
        files: Danh sách file ảnh
        recognize_function: Hàm nhận dạng ảnh (từ recognize.py)
    
    Returns:
        Tuple (success_count, total_count, errors)
    """
    if album_name not in album_storage:
        album_storage[album_name] = []
    
    bucket = album_storage[album_name]
    errors = []
    success_count = 0
    
    for i, f in enumerate(files):
        try:
            # Kiểm tra file ảnh
            img_pil = Image.open(f)
            img_pil.verify()

            # Đọc bytes
            f.seek(0)
            file_bytes = f.read()

            # Gọi AI lấy địa danh nếu có function
            landmark = "N/A"
            if recognize_function:
                try:
                    img_for_ai = Image.open(BytesIO(file_bytes))
                    landmark = recognize_function(img_for_ai, "strict_landmark")
                except Exception as e:
                    errors.append(f"Ảnh {f.name}: Lỗi nhận dạng - {e}")
                    continue

            # Tạo item và thêm vào bucket
            item = create_album_item(f.name, file_bytes, album_name, landmark)
            bucket.append(item)
            success_count += 1

        except Exception as e:
            errors.append(f"File không hợp lệ: {f.name} ({e})")
            continue
    
    album_storage[album_name] = bucket
    return success_count, len(files), errors

def filter_album_items(items, search_landmark=None, search_date=None):
    """Lọc các item trong album theo tiêu chí."""
    filtered_items = items
    
    if search_landmark:
        filtered_items = [i for i in filtered_items 
                         if search_landmark.lower() in i.get('landmark', '').lower()]
    
    if search_date:
        filtered_items = [i for i in filtered_items 
                         if datetime.fromisoformat(i['uploaded_at']).date() == search_date]
    
    return filtered_items

def group_items_by_landmark(items):
    """Nhóm các item theo địa danh."""
    groups = {}
    for item in items:
        landmark = item.get('landmark', 'Chưa nhận dạng')
        if landmark not in groups:
            groups[landmark] = []
        groups[landmark].append(item)
    return groups

def sort_items_by_date(items, reverse=True):
    """Sắp xếp các item theo ngày tải lên."""
    return sorted(items, key=lambda x: x['uploaded_at'], reverse=reverse)

def get_album_stats(album_storage):
    """Lấy thống kê tổng quan về các album."""
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
    
    return stats

def save_albums_to_file(album_storage, filename="albums_backup.json"):
    """Lưu tất cả album vào file JSON (không bao gồm bytes ảnh)."""
    backup_data = {}
    for album_name, items in album_storage.items():
        backup_data[album_name] = []
        for item in items:
            # Lưu metadata, không lưu bytes
            backup_item = {k: v for k, v in item.items() if k != "bytes"}
            backup_data[album_name].append(backup_item)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    return filename

def load_albums_metadata_from_file(filename="albums_backup.json"):
    """Tải metadata của album từ file JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Lỗi khi tải file: {e}")
        return {}