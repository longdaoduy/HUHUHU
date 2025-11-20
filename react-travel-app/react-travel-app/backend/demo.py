import ai_recommend
import recognize
import album_manager
import streamlit as st
import pandas as pd
from math import radians, sin, cos, asin, sqrt
from datetime import datetime
from io import BytesIO
from PIL import Image
try:
    from streamlit_geolocation import streamlit_geolocation as geoloc
    _GEO_OK = True
except Exception as e:
    _GEO_OK = False
    _GEO_ERR = repr(e)
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
                if recognize.OPENAI_ENABLED:
                    with st.spinner("Đang nhận dạng..."):
                        try:
                            # img đã được định nghĩa ở 'with col1'
                            result = recognize.get_landmark_from_image(img)
                            st.success(result)
                        except Exception as e:
                            st.error(f"Lỗi API: {e}")
                else:
                    st.error("Tính năng AI chưa được bật. Vui lòng thêm OPENAI_API_KEY.")
            else:
                st.warning("Hãy tải một ảnh trước.")

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

    # Hiển thị toạ độ đã lưu gần nhất 
    if "last_coords" in st.session_state:
        lc = st.session_state["last_coords"]
        st.caption(f"Toạ độ đã lưu: lat={lc['lat']:.6f}, lon={lc['lon']:.6f} · nguồn: {lc['source']}")

    mode = st.radio(
        "Chọn cách lấy vị trí",
        ("Chọn tỉnh/thành (thủ công)", "Dùng GPS từ trình duyệt"),
        horizontal=True,
    )

    col_left, col_right = st.columns([2, 1])

    # Thiết lập bán kính chung
    with col_right:
        radius = st.slider("Bán kính (km)", min_value=1, max_value=100, value=5)

    # Xác định lat/lon theo mode
    lat = lon = None
    with col_left:
        if mode.startswith("Chọn tỉnh/thành"):
            province = st.selectbox(
                "Chọn tỉnh/thành",
                options=list(PROVINCE_COORDS.keys()),
                index=0,
            )
            lat, lon = PROVINCE_COORDS[province]
            src = "manual"
        else:
            if not _GEO_OK:
                st.error("Thiếu component GPS. Cài: pip install streamlit-geolocation")
                st.info("Tạm thời nhập tay nếu cần:")
                lat = st.number_input("Lat", value=float(st.session_state.get("last_coords", {}).get("lat", 10.762622)))
                lon = st.number_input("Lon", value=float(st.session_state.get("last_coords", {}).get("lon", 106.660172)))
                src = "manual-fallback"
            else:
                st.caption("Bấm 'Cho phép' khi trình duyệt hỏi quyền vị trí.")
                loc = geoloc()
                if loc and loc.get("latitude") and loc.get("longitude"):
                    lat = float(loc["latitude"])
                    lon = float(loc["longitude"])
                    src = "gps"
                    st.success(f"Đã lấy GPS: lat={lat:.6f}, lon={lon:.6f}")
                else:
                    st.warning("Chưa nhận được toạ độ từ GPS. Bạn có thể thử lại hoặc chuyển sang chọn thủ công.")

    st.caption("Dữ liệu lấy từ database nội bộ. Không gọi mạng.")

    # Nút tìm kiếm
    if st.button("Tìm điểm tham quan gần tôi"):
        if lat is None or lon is None:
            st.error("Chưa có toạ độ hợp lệ.")
            return

        # Lưu tĩnh toạ độ đã dùng
        st.session_state["last_coords"] = {"lat": lat, "lon": lon, "source": src}

        destinations = ai_recommend.loadDestination()

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
                    st.markdown(
                        f"**{item.get('name','(Không tên)')}**"
                        + (f" · {item.get('location')}" if item.get('location') else "")
                    )
                    st.markdown(f"Khoảng cách: **{item['distance_km']:.2f} km**")
                    if item.get("introduction"):
                        st.write(item["introduction"])
                    if item.get("price") is not None:
                        try:
                            st.caption(f"Giá tham khảo: {int(item['price']):,} VNĐ")
                        except Exception:
                            st.caption(f"Giá tham khảo: {item['price']} VNĐ")
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

def render_thumbnail(item):
    """Hàm con để hiển thị 1 ảnh thumbnail và popover chi tiết."""
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

        with st.expander("Thêm ảnh vào album (Tự động nhận dạng)"):
            files = st.file_uploader("Tải nhiều ảnh", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"uploader_{album_name}")

            if st.button(f"Thêm {len(files)} ảnh vào '{album_name}'"):
                if not files:
                    st.warning("Chọn ít nhất một ảnh.")
                elif not recognize.OPENAI_ENABLED:
                    st.error("Không thể thêm ảnh. Tính năng AI (OpenAI Key) chưa được cấu hình.")
                else:
                    progress_bar = st.progress(0, text="Đang xử lý ảnh...")
                    
                    success_count, total_count, errors = album_manager.add_images_to_album(
                        st.session_state.albums,
                        album_name,
                        files,
                        recognize.analyze_image
                    )
                    
                    progress_bar.empty()
                    
                    if errors:
                        st.error(f"Có lỗi khi xử lý {len(errors)} ảnh:")
                        for error in errors:
                            st.error(f"- {error}")
                    
                    if success_count > 0:
                        st.success(f"Đã thêm {success_count}/{total_count} ảnh vào album '{album_name}'.")
                        st.rerun()

        if not items:
            st.info("Album này chưa có ảnh. Hãy thêm ảnh ở trên.")
            return

        st.subheader("Tìm kiếm và Lọc")
        c_filter1, c_filter2 = st.columns(2)
        with c_filter1:
            search_landmark = st.text_input("Tìm theo địa danh")
        with c_filter2:
            search_date = st.date_input("Tìm theo ngày tải lên", None)

        # Áp dụng bộ lọc
        filtered_items = album_manager.filter_album_items(items, search_landmark, search_date)

        st.caption(f"Hiển thị {len(filtered_items)} / {len(items)} ảnh.")
        st.divider()

        st.subheader("Bộ sưu tập")
        group_by = st.radio("Sắp xếp/Nhóm theo:", ("Không nhóm (mới nhất trước)", "Địa danh"), horizontal=True)

        if group_by == "Địa danh":
            groups = album_manager.group_items_by_landmark(filtered_items)
            
            for landmark, group_items in sorted(groups.items()):
                st.markdown(f"#### {landmark} ({len(group_items)} ảnh)")
                cols = st.columns(4) # Giữ layout 4 cột như file gốc
                for idx, item in enumerate(group_items):
                    with cols[idx % 4]:
                        render_thumbnail(item) # Yêu cầu 2
                st.divider()
        
        else: # "Không nhóm"
            # Sắp xếp mới nhất trước
            sorted_items = album_manager.sort_items_by_date(filtered_items, reverse=True)
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
            zip_buf = album_manager.zip_album(album_name, filtered_items)
            st.download_button(
                f"Tải {len(filtered_items)} ảnh (.zip)",
                data=zip_buf,
                file_name=f"{album_name}.zip",
                mime="application/zip",
                use_container_width=True
            )
        with dl_c2:
            if st.button(f"Chuẩn bị file PDF ({len(filtered_items)} ảnh)", use_container_width=True):
                with st.spinner("Đang tạo file PDF..."):
                    pdf_buf = album_manager.create_pdf_album(filtered_items)
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