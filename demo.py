import ai_recommend
import streamlit as st
import pandas as pd
from math import radians, sin, cos, asin, sqrt
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import base64
import io
import exifread
from geopy.geocoders import Nominatim
import textwrap 

st.set_page_config(page_title="Du lịch demo ", page_icon="🧭", layout="wide")

# Khởi tạo state
if "albums" not in st.session_state:
    # Cấu trúc mới cho album items (sẽ được thêm trong screen_album)
    # {
    #   "filename": str,
    #   "bytes": b,
    #   "uploaded_at": str (ISO format),
    #   "album_name": str,
    #   "landmark": str,
    #   "description": str
    # }
    st.session_state.albums = {}

# Thêm state cho album đang hoạt động
if "active_album" not in st.session_state:
    st.session_state.active_album = None



def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def zip_album(album_name, items):
    buf = BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
        for item in items:
            zf.writestr(item["filename"], item["bytes"])
    buf.seek(0)
    return buf

def screen_home():
    st.title("🧭 Demo UI du lịch")
    st.markdown("#### Trang chủ")
    st.caption("Chọn một tính năng bên dưới để bắt đầu.")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("###  Nhận dạng ảnh (UI)")
        st.write("- Tải 1 ảnh lên\n- Xem trước ảnh\n- Hiển thị kết quả")
        if st.button("Vào tính năng này", key="go_upload"):
            st.session_state.nav = "Nhận dạng ảnh"

    with c2:
        st.markdown("###  Gợi ý điểm tham quan")
        st.write("- Nhập vị trí hiện tại\n- Chọn bán kính tìm kiếm\n- Xem gợi ý và đánh giá")
        if st.button("Vào tính năng này", key="go_suggest"):
            st.session_state.nav = "Gợi ý điểm tham quan"

    with c3:
        st.markdown("###  Gợi ý địa điểm theo sở thích")
        st.write("- Nhập sở thích\n- Hiển thị kết quả theo sở thích")
        if st.button("Vào tính năng này", key="go_suggest_interest"):
            st.session_state.nav = "Gợi ý theo sở thích"
            
    with c4:
        st.markdown("###  Album sau chuyến đi")
        st.write("- Tạo album\n- Thêm nhiều ảnh\n- Tải toàn bộ dưới dạng .zip")
        if st.button("Vào tính năng này", key="go_album"):
            st.session_state.nav = "Album ảnh"

    st.divider()
    st.info("Dùng menu trái để chuyển nhanh giữa các tính năng.")

# --- PHẦN AI (CẬP NHẬT) ---

#client = OpenAI(api_key="")
OPENAI_ENABLED = True

def get_image_analysis(image_pil, prompt):
    """Hàm chung để gọi OpenAI Vision API."""
    if not OPENAI_ENABLED:
        return "N/A (Chưa cấu hình API)"
    
    try:
        buf = io.BytesIO()
        image_pil.save(buf, format="JPEG")
        img_str = base64.b64encode(buf.getvalue()).decode()

        response = client.responses.create(

            model="gpt-5-mini", 
            input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": prompt},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{img_str}"}
        ]
    }],
    max_output_tokens=300
)
        return response.output_text.strip()
    except Exception as e:
        st.error(f"Lỗi gọi OpenAI API: {e}")
        return f"Lỗi: {e}"


def get_landmark_from_image(image_pil):
    """Yêu cầu: Nhận dạng địa danh."""
    prompt = "What is the landmark in this photo? If no specific landmark, say 'Không có'. Answer in Vietnamese. Keep it short (e.g., 'Nhà thờ Đức Bà' or 'Tháp Rùa')."
    return get_image_analysis(image_pil, prompt)

def detect_landmark_strict(pil_img, retries=3):
    def ask(img):
        return (get_landmark_from_image(img) or "").strip()

    w, h = pil_img.size
    for scale in (1.0, 1.5, 0.75):
        img = pil_img if scale == 1.0 else pil_img.resize((int(w*scale), int(h*scale)))
        for _ in range(retries):
            name = ask(img)
            if name:
                return name

    buf = BytesIO()
    pil_img.convert("RGB").save(buf, format="JPEG", quality=95, optimize=True)
    buf.seek(0)
    img2 = Image.open(buf)
    for _ in range(retries):
        name = ask(img2)
        if name:
            return name

    raise ValueError("Không nhận diện được địa danh sau nhiều lần quét")

def get_gps_from_image(image_file):
    try:
        image_file.seek(0)
        tags = exifread.process_file(image_file, details=False)
        lat_ref = tags.get("GPS GPSLatitudeRef")
        lon_ref = tags.get("GPS GPSLongitudeRef")
        lat = tags.get("GPS GPSLatitude")
        lon = tags.get("GPS GPSLongitude")
        if not (lat and lon and lat_ref and lon_ref):
            return None

        def convert_to_degrees(value):
            d, m, s = [float(x.num) / float(x.den) for x in value.values]
            return d + (m / 60.0) + (s / 3600.0)

        lat_val = convert_to_degrees(lat)
        lon_val = convert_to_degrees(lon)
        if lat_ref.values[0] != "N":
            lat_val = -lat_val
        if lon_ref.values[0] != "E":
            lon_val = -lon_val
        return (lat_val, lon_val)
    except Exception:
        return None


def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="album_locator")
        location = geolocator.reverse((lat, lon), language="vi")
        return location.address if location else None
    except Exception:
        return None


def detect_location(image_file, image_pil):
    gps = get_gps_from_image(image_file)
    if gps:
        lat, lon = gps
        place = reverse_geocode(lat, lon)
        if place:
            return place
   
    try:
        place = get_landmark_from_image(image_pil)
        return place
    except Exception:
        return None

def screen_upload():
    st.title("Tải ảnh để nhận dạng (UI)")
    st.subheader("Tải ảnh lên")

    up = st.file_uploader("Chọn ảnh (png/jpg/jpeg)", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    col1, col2 = st.columns([1, 1])

    with col1:
        if up:
            img = Image.open(up)
            st.image(img, caption=f"Xem nhanh: {up.name}", use_container_width=True)
        else:
            st.info("Chưa có ảnh. Hãy chọn file ở trên.")

    with col2:
        st.markdown("**Kết quả nhận dạng:**")
        if st.button("Nhận dạng ảnh"):
            if up:
                 if OPENAI_ENABLED:
                    with st.spinner("Đang nhận dạng..."):
                        try:
                            # img đã được định nghĩa ở 'with col1'
                            result = get_landmark_from_image(img)
                            st.success(result)
                        except Exception as e:
                            st.error(f"Lỗi API: {e}")
                 else:
                    st.error("Tính năng AI chưa được bật. Vui lòng thêm OPENAI_API_KEY.")
            else:
                st.warning("Hãy tải một ảnh trước.")

# screen_suggest_interest (Giữ nguyên)
def screen_suggest_interest():
    st.title("Gợi ý địa điểm theo sở thích")
    st.markdown("Nhập sở thích hoặc địa điểm bạn muốn tham quan")
    interest = st.text_input("Nhập sở thích tham quan của bạn (ví dụ: đồi núi, biển cả, ...)")

    if st.button("Gợi ý ngay"):
        if interest.strip() == "":
            st.warning("Vui lòng nhập sở thích")
            return
        try:
            destination_list = ai_recommend.loadDestination()
            results = ai_recommend.recommend(interest, destination_list)

            if not results:
                st.error("Không tìm thấy địa điểm phù hợp")
                return

            st.success(f"Tìm thấy {len(results)} địa điểm phù hợp")

            for dest in results:
                with st.container(border=True):
                    left, right = st.columns([3, 1])
                    with left:
                        # Tên + địa bàn
                        st.markdown(
                            f"**{dest.get('name', '(Không tên)')}**"
                            + (f" · {dest.get('location')}" if dest.get('location') else "")
                        )

                        # Giới thiệu
                        if dest.get("introduction"):
                            st.write(dest["introduction"])                      
                        # Giá
                        if dest.get("price") is not None:
                            try:
                                st.caption(f"Giá tham khảo: {int(dest['price']):,} VNĐ")
                            except Exception:
                                st.caption(f"Giá tham khảo: {dest['price']} VNĐ")
                        # Review trong expander, tách câu
                        if dest.get("review"):
                            with st.expander("Xem review chi tiết"):
                                sentences = [s.strip() for s in str(dest["review"]).split(".") if s.strip()]
                                for s in sentences:
                                    st.write(f"- {s}.")
                    with right:
                        # Rating
                        rating = dest.get("rating")
                        if rating is not None:
                            st.metric("Đánh giá", f"{float(rating):.1f} ⭐")
                        else:
                            st.metric("Đánh giá", "N/A")

                        if dest.get("score") is not None:
                            try:
                                st.caption(f"Phù hợp: {float(dest['score']):.0%}")
                            except Exception:
                                st.caption(f"Phù hợp: {dest['score']}")
        except Exception as e:
            st.error(f"Lỗi khi gợi ý: {e}")

def load_province_coords(csv_path: str) -> dict:
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{csv_path}'. Tính năng gợi ý theo vị trí sẽ không hoạt động.")
        return {}, pd.DataFrame()
        
    df["display"] = df["province"].fillna(df["capital"])
    # dict: display -> (lat, lon)
    return dict(zip(df["display"], zip(df["lat"], df["lon"]))), df

def screen_suggest():
    st.title("Gợi ý điểm tham quan trong bán kính")

    PROVINCE_COORDS, df = load_province_coords("vn_provinces_coords.csv")
    if not PROVINCE_COORDS:
        return

    colA, colB = st.columns([2, 1])
    with colA:
        province = st.selectbox(
            "Chọn tỉnh/thành",
            options=list(PROVINCE_COORDS.keys()),
            index=0,
        )
    with colB:
        radius = st.slider("Bán kính (km)", min_value=1, max_value=100, value=5)

    lat, lon = PROVINCE_COORDS[province]

    st.caption("Dữ liệu lấy từ database nội bộ. Không gọi mạng.")
    if st.button("Tìm điểm tham quan gần tôi"):
        destinations = ai_recommend.loadDestination()  # dùng hàm đã sửa

        results = []
        for d in destinations:
            if d.get("lat") is None or d.get("lon") is None:
                continue
            dist = haversine_km(lat, lon, d["lat"], d["lon"])
            if dist <= radius:
                results.append({**d, "distance_km": dist})

        if not results:
            st.warning("Không tìm thấy điểm nào trong bán kính đã chọn.")
            return

        results.sort(key=lambda x: (x["distance_km"], -float(x["rating"] or 0)))
        st.success(f"Tìm thấy {len(results)} điểm phù hợp.")

        for item in results:
            with st.container(border=True):
                left, right = st.columns([3, 1])
                with left:
                    # Tên
                    st.markdown(f"**{item.get('name','(Không tên)')}**"
                                + (f" · {item.get('location')}" if item.get('location') else ""))
                    # Khoảng cách
                    st.markdown(f"Khoảng cách: **{item['distance_km']:.2f} km**")
                    # Giới thiệu ngắn
                    if item.get("introduction"):
                        st.write(item["introduction"])
                    # Tags (nếu có)
                    # Giá
                    if item.get("price") is not None:
                        try:
                            st.caption(f"Giá tham khảo: {int(item['price']):,} VNĐ")
                        except Exception:
                            st.caption(f"Giá tham khảo: {item['price']} VNĐ")
                    # Review trong expander
                if item.get("review"):
                    with st.expander("Xem review chi tiết"):
                        sentences = [s.strip() for s in item["review"].split(".") if s.strip()]
                        for s in sentences:
                            st.write(f"- {s}.")
                with right:
                    rating = item.get("rating")
                    if rating is not None:
                        st.metric("Đánh giá", f"{float(rating):.1f} ⭐")
                    else:
                        st.metric("Đánh giá", "N/A")



def create_pdf_album(album_items):
    """Yêu cầu 4: Xuất album ra PDF."""
    if not album_items:
        return None

    try:
        # Thử tải font hỗ trợ Unicode.
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
        font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except IOError:
        # Fallback nếu không tìm thấy font
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

def render_thumbnail(item):
    """Yêu cầu 2: Hàm con để hiển thị 1 ảnh thumbnail và popover chi tiết."""
    img = Image.open(BytesIO(item["bytes"]))
    st.image(img, use_container_width=True, caption=item['filename'][:20] + "...")
    
    with st.popover("Xem chi tiết"):
        st.image(img, use_container_width=True)
        st.markdown(f"**Tên file:** {item['filename']}")
        dt = datetime.fromisoformat(item['uploaded_at'])
        st.markdown(f"**Tải lên:** {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Album:** {item.get('album_name', 'N/A')}")
        st.divider()
        st.markdown(f"**Địa danh (AI):**")
        st.info(item.get('landmark', 'N/A'))
        

# --- PHẦN ALBUM (NÂNG CẤP HOÀN TOÀN) ---

def screen_album():
    st.title("🖼️ Album ảnh sau chuyến đi")
    
    # Sử dụng layout cột của file gốc
    left, right = st.columns([2,1])

    # --- Cột phải: Quản lý Album (Cải tiến từ file gốc) ---
    with right:
        st.markdown("### Quản lý Album")
        
        # Chọn album đang hoạt động
        album_names = list(st.session_state.albums.keys())
        
        # Nếu album đang active bị xóa, reset nó
        if st.session_state.active_album not in album_names:
            st.session_state.active_album = None

        # Chọn album để xem (thay cho text input của file gốc)
        default_index = 0
        if st.session_state.active_album in album_names:
            default_index = album_names.index(st.session_state.active_album)
        
        selected_album = st.radio(
            "Chọn album để xem/thêm ảnh:",
            album_names,
            index=default_index if album_names else 0,
            key="album_selector",
            label_visibility="collapsed"
        )
        if album_names:
            st.session_state.active_album = selected_album
        
        st.divider()
        new_album_name = st.text_input("Tên album mới")
        if st.button("Tạo album mới"):
            if new_album_name.strip():
                if new_album_name not in st.session_state.albums:
                    st.session_state.albums[new_album_name] = []
                    st.session_state.active_album = new_album_name
                    st.rerun()
                else:
                    st.warning("Album đã tồn tại.")
            else:
                st.warning("Tên album không được để trống.")
        
        if st.session_state.active_album and st.button(f"Xóa album '{st.session_state.active_album}'", type="primary"):
            del st.session_state.albums[st.session_state.active_album]
            st.session_state.active_album = None
            st.rerun()

    # --- Cột trái: Hiển thị Album chi tiết ---
    with left:
        if not st.session_state.active_album:
            st.info("Hãy tạo hoặc chọn một album từ cột bên phải để bắt đầu.")
            return

        # Lấy thông tin album hiện tại
        album_name = st.session_state.active_album
        items = st.session_state.albums.get(album_name, [])
        st.header(f"Album: {album_name} ({len(items)} ảnh)")

        # --- Yêu cầu 1: Khu vực tải ảnh VÀ xử lý metadata ---
        with st.expander("Thêm ảnh vào album (Tự động nhận dạng)"):
            files = st.file_uploader("Tải nhiều ảnh", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"uploader_{album_name}")

            if st.button(f"Thêm {len(files)} ảnh vào '{album_name}'"):
                if not files:
                    st.warning("Chọn ít nhất một ảnh.")
                elif not OPENAI_ENABLED:
                    st.error("Không thể thêm ảnh. Tính năng AI (OpenAI Key) chưa được cấu hình.")
                else:
                    progress_bar = st.progress(0, text="Đang xử lý ảnh...")
                    bucket = st.session_state.albums.get(album_name, [])
                    
                    for i, f in enumerate(files):
                        try:
                            progress_text = f"Đang xử lý ảnh: {f.name} ({i+1}/{len(files)})..."
                            progress_bar.progress((i+1) / len(files), text=progress_text)

                            # Kiểm tra file ảnh
                            img_pil = Image.open(f)
                            img_pil.verify()

                            # Đọc bytes
                            f.seek(0)
                            file_bytes = f.read()

                            # Gọi AI lấy địa danh
                            img_for_ai = Image.open(BytesIO(file_bytes))
                            try:
                                landmark = detect_landmark_strict(img_for_ai, retries=3)
                            except Exception as e:
                                st.error(f"Ảnh {f.name}: {e}. Dừng lại để tránh bỏ sót.")
                                progress_bar.empty()
                                st.stop()  # dừng hẳn, không lưu ảnh nào thiếu địa danh

                            # Lưu trữ metadata (chỉ chạy khi landmark hợp lệ)
                            bucket.append({
                                "filename": f.name,
                                "bytes": file_bytes,
                                "uploaded_at": datetime.now().isoformat(),
                                "album_name": album_name,
                                "landmark": landmark.strip(),
                            })

                        except Exception as e:
                            st.error(f"File không hợp lệ hoặc lỗi AI: {f.name} ({e})")
                            continue

                    st.session_state.albums[album_name] = bucket
                    progress_bar.empty()
                    st.success(f"Đã thêm {len(files)} ảnh vào album '{album_name}'.")
                    st.rerun()

        if not items:
            st.info("Album này chưa có ảnh. Hãy thêm ảnh ở trên.")
            return

        # --- Yêu cầu 3: Tìm kiếm và Lọc ---
        st.subheader("Tìm kiếm và Lọc")
        c_filter1, c_filter2 = st.columns(2)
        with c_filter1:
            search_landmark = st.text_input("Tìm theo địa danh")
        with c_filter2:
            search_date = st.date_input("Tìm theo ngày tải lên", None)

        # Áp dụng bộ lọc
        filtered_items = items
        if search_landmark:
            filtered_items = [i for i in filtered_items if search_landmark.lower() in i.get('landmark', '').lower()]
        if search_date:
            filtered_items = [i for i in filtered_items if datetime.fromisoformat(i['uploaded_at']).date() == search_date]

        st.caption(f"Hiển thị {len(filtered_items)} / {len(items)} ảnh.")
        st.divider()

        # --- Yêu cầu 2 & 5: Hiển thị Gallery & Nhóm ---
        st.subheader("Bộ sưu tập")
        group_by = st.radio("Sắp xếp/Nhóm theo:", ("Không nhóm (mới nhất trước)", "Địa danh"), horizontal=True)

        if group_by == "Địa danh":
            groups = {}
            for item in filtered_items:
                landmark = item.get('landmark', 'Chưa nhận dạng')
                if landmark not in groups:
                    groups[landmark] = []
                groups[landmark].append(item)
            
            for landmark, group_items in sorted(groups.items()):
                st.markdown(f"#### {landmark} ({len(group_items)} ảnh)")
                cols = st.columns(4) # Giữ layout 4 cột như file gốc
                for idx, item in enumerate(group_items):
                    with cols[idx % 4]:
                        render_thumbnail(item) # Yêu cầu 2
                st.divider()
        
        else: # "Không nhóm"
            # Sắp xếp mới nhất trước
            sorted_items = sorted(filtered_items, key=lambda x: x['uploaded_at'], reverse=True)
            cols = st.columns(4) # Giữ layout 4 cột như file gốc
            for idx, item in enumerate(sorted_items):
                with cols[idx % 4]:
                    render_thumbnail(item) # Yêu cầu 2

        # --- Nút tải xuống (Giữ Zip, Thêm PDF) ---
        st.divider()
        st.subheader("Tải xuống Album (đã lọc)")
        
        if not filtered_items:
            st.warning("Không có ảnh nào trong bộ lọc để tải xuống.")
            return

        dl_c1, dl_c2 = st.columns(2)
        with dl_c1:
            # Giữ nút Zip gốc
            zip_buf = zip_album(album_name, filtered_items)
            st.download_button(
                f"Tải {len(filtered_items)} ảnh (.zip)",
                data=zip_buf,
                file_name=f"{album_name}.zip",
                mime="application/zip",
                use_container_width=True
            )
        with dl_c2:
            # Yêu cầu 4: Nút tải PDF
            if st.button(f"Chuẩn bị file PDF ({len(filtered_items)} ảnh)", use_container_width=True):
                with st.spinner("Đang tạo file PDF..."):
                    pdf_buf = create_pdf_album(filtered_items)
                    if pdf_buf:
                        # Lưu vào session state để download button bên dưới có thể truy cập
                        st.session_state.pdf_buffer = pdf_buf
                    else:
                        st.error("Không có ảnh để tạo PDF.")
            
            if "pdf_buffer" in st.session_state:
                st.download_button(
                    "Tải file PDF",
                    data=st.session_state.pdf_buffer,
                    file_name=f"{album_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    on_click=lambda: st.session_state.pop("pdf_buffer", None) # Xóa buffer sau khi click
                )


# --- PHẦN ĐIỀU HƯỚNG GỐC (GIỮ NGUYÊN) ---

PAGES = {
    "Trang chủ": screen_home,
    "Nhận dạng ảnh": screen_upload,
    "Gợi ý điểm tham quan": screen_suggest,
    "Gợi ý theo sở thích": screen_suggest_interest,
    "Album ảnh": screen_album,
}

if "nav" not in st.session_state:
    st.session_state.nav = "Trang chủ"

with st.sidebar:
    st.header("Điều hướng")
    nav_selection = st.selectbox(
        "Chọn màn hình",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(st.session_state.nav),
        label_visibility="collapsed"
    )
    # Cập nhật state nếu lựa chọn thay đổi (tránh lỗi st.rerun)
    if nav_selection != st.session_state.nav:
        st.session_state.nav = nav_selection
        st.rerun()


PAGES[st.session_state.nav]()