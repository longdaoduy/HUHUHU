import streamlit as st
from math import radians, sin, cos, asin, sqrt
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image
from openai import OpenAI
import base64
import io
import exifread
from geopy.geocoders import Nominatim
st.set_page_config(page_title="Du lịch demo ", page_icon="🧭", layout="wide")

# Khởi tạo state
if "albums" not in st.session_state:
    # {album_name: [{"filename": str, "bytes": b, "uploaded_at": str}]}
    st.session_state.albums = {}

PROVINCE_COORDS = {
    "TP.HCM": (10.776889, 106.700806),
    "Hà Nội": (21.027763, 105.834160),
    "Quảng Nam": (15.573606, 108.474044),  # Tam Kỳ
}

ATTRACTIONS = [
    {"name": "Hồ Gươm (Hoàn Kiếm)", "city": "Hà Nội", "lat": 21.028511, "lon": 105.848097,
     "rating": 4.6, "reviews": ["Không khí dễ chịu, đi dạo tối rất thích.", "Gần phố cổ, nhiều quán ăn ngon."]},
    {"name": "Văn Miếu - Quốc Tử Giám", "city": "Hà Nội", "lat": 21.0278, "lon": 105.8354,
     "rating": 4.5, "reviews": ["Kiến trúc đẹp, nhiều góc chụp ảnh.", "Nên đi buổi sáng để vắng người."]},
    {"name": "Nhà thờ Đức Bà", "city": "TP.HCM", "lat": 10.7797838, "lon": 106.6990184,
     "rating": 4.4, "reviews": ["Địa điểm mang tính biểu tượng.", "Khu vực xung quanh nhiều quán cà phê."]},
    {"name": "Bưu điện Trung tâm Sài Gòn", "city": "TP.HCM", "lat": 10.7802, "lon": 106.6997,
     "rating": 4.6, "reviews": ["Kiến trúc Pháp cổ rất ấn tượng.", "Gần nhà thờ Đức Bà, đi bộ qua là tới."]},
    {"name": "Chợ Bến Thành", "city": "TP.HCM", "lat": 10.772, "lon": 106.698,
     "rating": 4.1, "reviews": ["Đông vui, nhiều đặc sản.", "Mặc cả trước khi mua sẽ tốt hơn."]},
    {"name": "Phố cổ Hội An", "city": "Quảng Nam", "lat": 15.880058, "lon": 108.338047,
     "rating": 4.8, "reviews": ["Đèn lồng buổi tối rất đẹp.", "Ẩm thực phong phú, dễ đi bộ."]},
]

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

    c1, c2, c3 = st.columns(3)

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
        st.markdown("###  Album sau chuyến đi")
        st.write("- Tạo album\n- Thêm nhiều ảnh\n- Tải toàn bộ dưới dạng .zip")
        if st.button("Vào tính năng này", key="go_album"):
            st.session_state.nav = "Album ảnh"

    st.divider()
    st.info("Dùng menu trái để chuyển nhanh giữa các tính năng.")

#client = OpenAI(api_key = "key")
def get_landmark_from_image(image):
    
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    img_str = base64.b64encode(buf.getvalue()).decode()

    prompt = "What is the landmark in this photo? Give a short answer."

    resp = client.responses.create(
        model="gpt-5-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{img_str}"}
            ]
        }],
        max_output_tokens=256
    )
    return resp.output_text.strip()

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
                 with st.spinner("Đang nhận dạng..."):
                    try:
                        result = get_landmark_from_image(img)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Lỗi API: {e}")
            else:
                st.warning("Hãy tải một ảnh trước.")

def screen_suggest():
    st.title("Gợi ý điểm tham quan trong bán kính")

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

    st.caption("Gợi ý dựa trên dữ liệu mẫu nội bộ. Không gọi mạng.")
    if st.button("Tìm điểm tham quan gần tôi"):
        results = []
        for a in ATTRACTIONS:
            d = haversine_km(lat, lon, a["lat"], a["lon"])
            if d <= radius:
                results.append({**a, "distance_km": d})

        if not results:
            st.warning("Không tìm thấy điểm nào trong bán kính đã chọn.")
            return

        results.sort(key=lambda x: (x["distance_km"], -x["rating"]))
        st.success(f"Tìm thấy {len(results)} điểm phù hợp.")
        for item in results:
            with st.container(border=True):
                left, right = st.columns([3, 1])
                with left:
                    st.markdown(f"**{item['name']}** · {item['city']}")
                    st.markdown(f"Khoảng cách: **{item['distance_km']:.2f} km**")
                with right:
                    st.metric("Đánh giá", f"{item['rating']:.1f} ⭐")

                with st.expander("Xem đánh giá mẫu"):
                    for r in item.get("reviews", []):
                        st.write(f"• {r}")


def screen_album():
    st.title(" Album ảnh sau chuyến đi")
    left, right = st.columns([2,1])

    with left:
        album_name = st.text_input("Tên album", value="Chuyến đi của tôi")
        files = st.file_uploader("Tải nhiều ảnh", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="album_uploader")

        add_col1, add_col2 = st.columns(2)
        with add_col1:
            if st.button("Thêm vào album"):
                 if not files:
                    st.warning("Chọn ít nhất một ảnh.")
                 else:
                    for f in files:
                        try:
                            img = Image.open(f)
                            img.verify()
                            f.seek(0)
                            img = Image.open(f)  # reopen để đọc dữ liệu
                        except Exception:
                            st.error(f"File không phải ảnh hợp lệ: {f.name}")
                            continue

                # 🔹 Tự phát hiện địa điểm từ ảnh
                        location = detect_location(f, img)
                        album_key = location if location else "Không xác định"

                        bucket = st.session_state.albums.get(album_key, [])
                        f.seek(0)
                        bucket.append({
                            "filename": f.name,
                            "bytes": f.read(),
                            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.session_state.albums[album_key] = bucket

            st.success("Đã thêm ảnh và tự động nhóm theo địa điểm.")
        with add_col2:
            if st.button("Xóa album hiện tại"):
                if album_name in st.session_state.albums:
                    del st.session_state.albums[album_name]
                    st.warning(f"Đã xóa album '{album_name}'.")
                else:
                    st.info("Album chưa tồn tại.")

        if album_name in st.session_state.albums and st.session_state.albums[album_name]:
            st.markdown(f"### Ảnh trong album: {album_name}")
            items = st.session_state.albums[album_name]
            cols = st.columns(4)
            for idx, item in enumerate(items):
                with cols[idx % 4]:
                    try:
                        img = Image.open(BytesIO(item["bytes"]))
                        st.image(img, use_container_width=True)
                        st.caption(f"{item['filename']} · {item['uploaded_at']}")
                    except Exception:
                        st.error(f"Lỗi hiển thị: {item['filename']}")

            zip_buf = zip_album(album_name, items)
            st.download_button(
                "Tải toàn bộ album (.zip)",
                data=zip_buf,
                file_name=f"{album_name}.zip",
                mime="application/zip"
            )
        else:
            st.info("Album trống hoặc chưa tồn tại. Hãy thêm ảnh.")

    with right:
        st.markdown("### Danh sách album")
        if not st.session_state.albums:
            st.caption("Chưa có album nào.")
        else:
            for name, items in st.session_state.albums.items():
                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    st.caption(f"{len(items)} ảnh trong album")
                    if items:
                        try:
                            thumb = Image.open(BytesIO(items[-1]["bytes"]))
                            st.image(thumb, caption="Ảnh gần nhất", use_container_width=True)
                        except Exception:
                            st.caption("Không tạo được thumbnail.")


PAGES = {
    "Trang chủ": screen_home,
    "Nhận dạng ảnh": screen_upload,
    "Gợi ý điểm tham quan": screen_suggest,
    "Album ảnh": screen_album,
}

if "nav" not in st.session_state:
    st.session_state.nav = "Trang chủ"

with st.sidebar:
    st.header("Điều hướng")
    st.session_state.nav = st.selectbox(
        "Chọn màn hình",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(st.session_state.nav),
        label_visibility="collapsed"
    )


PAGES[st.session_state.nav]()
