import base64
import io
import exifread
from geopy.geocoders import Nominatim
from openai import OpenAI
from PIL import Image
from io import BytesIO

# Khởi tạo OpenAI client
client = OpenAI(api_key="")
OPENAI_ENABLED = True

def get_image_analysis(image_pil, prompt):
    """Hàm chung để gọi OpenAI Vision API."""
    if not OPENAI_ENABLED:
        return "N/A (Chưa cấu hình API)"
    
    try:
        buf = io.BytesIO()
        image_pil.save(buf, format="JPEG")
        img_str = base64.b64encode(buf.getvalue()).decode()

        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                ]
            }],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Lỗi gọi OpenAI API: {e}")

def get_landmark_from_image(image_pil):
    """Yêu cầu: Nhận dạng địa danh."""
    prompt = "What is the landmark in this photo? If no specific landmark, say 'Không có'. Answer in Vietnamese. Keep it short (e.g., 'Nhà thờ Đức Bà' or 'Tháp Rùa')."
    return get_image_analysis(image_pil, prompt)

def get_landmark_with_confidence(image_pil):
    """Nhận dạng địa danh với thông tin chi tiết hơn."""
    prompt = """Identify the landmark in this photo. 
    - If it's a famous landmark, provide the name in Vietnamese
    - If it's not a landmark or unclear, say 'Không rõ địa danh'
    - Keep the landmark name short (e.g., 'Chùa Một Cột', 'Hồ Gươm')
    
    Return ONLY the landmark name, nothing else."""
    
    try:
        landmark = get_image_analysis(image_pil, prompt).strip()
        
        # Determine confidence based on response
        if not landmark or landmark.lower() in ['không có', 'không rõ', 'không rõ địa danh', 'n/a']:
            return {
                "landmark": "Không rõ địa danh",
                "description": "Không thể nhận diện địa danh trong ảnh này",
                "confidence": "low"
            }
        elif len(landmark) < 50 and 'không' not in landmark.lower():
            return {
                "landmark": landmark,
                "description": f"Địa danh được nhận dạng: {landmark}",
                "confidence": "high"
            }
        else:
            return {
                "landmark": landmark[:50],
                "description": f"Có thể là: {landmark[:100]}",
                "confidence": "medium"
            }
    except Exception as e:
        return {
            "landmark": "Không rõ địa danh",
            "description": f"Lỗi khi nhận dạng: {str(e)[:50]}",
            "confidence": "low"
        }


def detect_landmark_strict(pil_img, retries=3):
    """Nhận dạng địa danh với nhiều lần thử và xử lý ảnh khác nhau."""
    def ask(img):
        return (get_landmark_from_image(img) or "").strip()

    w, h = pil_img.size
    # Thử với các tỷ lệ khác nhau
    for scale in (1.0, 1.5, 0.75):
        img = pil_img if scale == 1.0 else pil_img.resize((int(w*scale), int(h*scale)))
        for _ in range(retries):
            name = ask(img)
            if name and name.lower() != "không có":
                return name

    # Thử với ảnh được tối ưu hóa
    buf = BytesIO()
    pil_img.convert("RGB").save(buf, format="JPEG", quality=95, optimize=True)
    buf.seek(0)
    img2 = Image.open(buf)
    for _ in range(retries):
        name = ask(img2)
        if name and name.lower() != "không có":
            return name

    raise ValueError("Không nhận diện được địa danh sau nhiều lần quét")

def get_gps_from_image(image_file):
    """Trích xuất tọa độ GPS từ EXIF data của ảnh."""
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
    """Chuyển đổi tọa độ thành địa chỉ."""
    try:
        geolocator = Nominatim(user_agent="album_locator")
        location = geolocator.reverse((lat, lon), language="vi")
        return location.address if location else None
    except Exception:
        return None

def detect_location(image_file, image_pil):
    """Phát hiện vị trí từ ảnh (GPS hoặc AI)."""
    # Thử lấy GPS từ EXIF
    gps = get_gps_from_image(image_file)
    if gps:
        lat, lon = gps
        place = reverse_geocode(lat, lon)
        if place:
            return place
   
    # Nếu không có GPS, dùng AI
    try:
        place = get_landmark_from_image(image_pil)
        return place
    except Exception:
        return None

def analyze_image(image_file_or_pil, analysis_type="landmark"):
    """
    Hàm chính để phân tích ảnh.
    
    Args:
        image_file_or_pil: File ảnh hoặc PIL Image
        analysis_type: "landmark", "location", hoặc "strict_landmark"
    
    Returns:
        Kết quả phân tích tùy theo loại
    """
    if isinstance(image_file_or_pil, Image.Image):
        # Nếu là PIL Image
        pil_img = image_file_or_pil
        if analysis_type == "landmark":
            return get_landmark_from_image(pil_img)
        elif analysis_type == "strict_landmark":
            return detect_landmark_strict(pil_img)
        else:
            return "Cần file gốc để phân tích GPS"
    else:
        # Nếu là file
        image_file = image_file_or_pil
        pil_img = Image.open(image_file)
        
        if analysis_type == "landmark":
            return get_landmark_from_image(pil_img)
        elif analysis_type == "location":
            return detect_location(image_file, pil_img)
        elif analysis_type == "strict_landmark":
            return detect_landmark_strict(pil_img)
        else:
            return get_landmark_from_image(pil_img)