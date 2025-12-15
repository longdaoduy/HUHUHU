import base64
import io
import os
import exifread
from geopy.geocoders import Nominatim
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Sử dụng OpenAI API
print("[RECOGNIZE] Initializing OpenAI API for image recognition...")
api_key = os.getenv('OPENAI_API_KEY', '')
if not api_key:
    print("[RECOGNIZE] ERROR: OPENAI_API_KEY not found in environment variables")
    OPENAI_ENABLED = False
    USE_LOCAL_MODEL = False
else:
    try:
        client = OpenAI(api_key=api_key)
        OPENAI_ENABLED = True
        USE_LOCAL_MODEL = False
        print("[RECOGNIZE] ✅ OpenAI API initialized successfully")
    except Exception as e:
        print(f"[RECOGNIZE] Error initializing OpenAI: {e}")
        OPENAI_ENABLED = False
        USE_LOCAL_MODEL = False

def encode_image_base64(image_pil):
    """Chuyển đổi PIL Image sang base64 string."""
    buffered = BytesIO()
    image_pil.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

def load_landmarks_database():
    """Load danh sách địa danh từ database.json."""
    try:
        import json
        import unidecode
        with open("database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Tạo dictionary để tra cứu nhanh
        landmarks_dict = {}
        for item in data:
            name = item.get("name", "")
            # Normalize tên để dễ so sánh
            normalized_name = unidecode.unidecode(name.lower())
            landmarks_dict[normalized_name] = {
                "name": name,
                "lat": item.get("lat"),
                "lon": item.get("lon"),
                "location": item.get("location"),
                "province": item.get("province")
            }
        return landmarks_dict
    except Exception as e:
        print(f"[RECOGNIZE] Warning: Could not load database.json: {e}")
        return {}

def find_landmark_info(landmark_name):
    """Tìm thông tin địa danh từ database hoặc geocoding."""
    import unidecode
    
    # Load database
    landmarks_db = load_landmarks_database()
    
    # Normalize tên để tìm kiếm
    normalized_search = unidecode.unidecode(landmark_name.lower())
    
    # Tìm kiếm exact match
    if normalized_search in landmarks_db:
        info = landmarks_db[normalized_search]
        address = f"{info['location']}, {info['province']}" if info.get('location') and info.get('province') else info.get('location', 'N/A')
        return {
            "lat": info.get("lat"),
            "lon": info.get("lon"),
            "address": address
        }
    
    # Tìm kiếm partial match
    for key, info in landmarks_db.items():
        if normalized_search in key or key in normalized_search:
            address = f"{info['location']}, {info['province']}" if info.get('location') and info.get('province') else info.get('location', 'N/A')
            return {
                "lat": info.get("lat"),
                "lon": info.get("lon"),
                "address": address
            }
    
    # Nếu không tìm thấy trong database, thử geocoding
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="travel_app_recognizer", timeout=5)
        
        # Thêm "Vietnam" để tìm kiếm chính xác hơn
        search_query = f"{landmark_name}, Vietnam"
        location = geolocator.geocode(search_query, language="vi")
        
        if location:
            return {
                "lat": location.latitude,
                "lon": location.longitude,
                "address": location.address
            }
    except Exception as e:
        print(f"[RECOGNIZE] Geocoding error: {e}")
    
    # Không tìm thấy
    return {
        "lat": None,
        "lon": None,
        "address": None
    }

def get_image_analysis(image_pil, prompt):
    """Hàm chung để phân tích ảnh sử dụng OpenAI Vision API."""
    if not OPENAI_ENABLED:
        return "N/A (OpenAI API chưa khả dụng - kiểm tra API key)"
    
    try:
        # Chuyển ảnh sang base64
        base64_image = encode_image_base64(image_pil)
        
        # Gọi OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Lỗi phân tích ảnh với OpenAI: {e}")

def get_landmark_from_image(image_pil):
    """Yêu cầu: Nhận dạng địa danh - sử dụng OpenAI Vision API."""
    if not OPENAI_ENABLED:
        return "Không thể nhận diện (OpenAI API chưa sẵn sàng)"
    
    # Load danh sách địa danh từ database để tham khảo
    landmark_names = []
    try:
        import json
        with open("database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            landmark_names = [item.get("name", "") for item in data if item.get("name")]
    except:
        pass
    
    landmarks_list = ", ".join(landmark_names[:34]) if landmark_names else "Landmark 81, Nhà thờ Đức Bà, Bưu điện Trung tâm Sài Gòn, Chợ Bến Thành, Bitexco Tower, AEON Mall Tân Phú, Vincom Center Đồng Khởi, Bến Nhà Rồng, Crescent Mall, Công viên Suối Tiên"
    prompt = f"""Phân tích ảnh này và nhận dạng địa danh cụ thể ở TP. Hồ Chí Minh.

HƯỚNG DẪN QUAN TRỌNG:
1. Tìm kiếm TÊN CỤ THỂ trên biển hiệu, logo, bảng tên, hoặc đặc điểm kiến trúc của các địa điểm ở Thành Phố Hồ Chí Minh
2. Nếu thấy logo/tên thương hiệu (ví dụ: AEON, Vincom, Landmark 81...), trả về TÊN ĐẦY ĐỦ CHÍNH XÁC
3. Tránh trả lời chung chung như "khu mua sắm", "trung tâm thương mại", "toà nhà"
4. Nếu nhìn thấy chữ tiếng Việt hoặc tiếng Anh trên ảnh, đọc và sử dụng để xác định tên

Một số địa danh tham khảo ở TP.HCM:
{landmarks_list}

HÃY TRẢ VỀ:
- Nếu nhận diện được: TÊN ĐẦY ĐỦ VÀ CHÍNH XÁC (ví dụ: "AEON Mall Tân Phú", "Vincom Center Đồng Khởi")
- Nếu KHÔNG chắc chắn: "Không rõ địa danh"

Chỉ trả về TÊN, không giải thích thêm."""
    
    try:
        result = get_image_analysis(image_pil, prompt)
        return result.strip()
    except Exception as e:
        return f"Lỗi nhận dạng: {str(e)[:50]}"

def get_landmark_with_confidence(image_pil):
    """Nhận dạng địa danh với thông tin chi tiết hơn - sử dụng OpenAI Vision API."""
    if not OPENAI_ENABLED:
        return {
            "landmark": "Không rõ địa danh",
            "description": "OpenAI API chưa khả dụng",
            "confidence": "low"
        }
    
    # Load danh sách địa danh từ database
    landmark_names = []
    try:
        import json
        with open("database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            landmark_names = [item.get("name", "") for item in data if item.get("name")]
    except:
        pass
    
    landmarks_list = "\n- ".join(landmark_names[:30]) if landmark_names else "Landmark 81\n- Nhà Thờ Đức Bà\n- Chợ Bến Thành\n- AEON Mall Tân Phú\n- Bitexco Tower"
    
    prompt = f"""Phân tích ảnh này và trả về ONLY valid JSON (không có text khác):
{{
  "landmark": "Tên chính xác của địa danh (tiếng Việt)",
  "description": "Mô tả ngắn gọn về địa danh này",
  "confidence": "high/medium/low"
}}

HƯỚNG DẪN QUAN TRỌNG:
1. Tìm kiếm BIỂN HIỆU, LOGO, TÊN THƯƠNG HIỆU trên ảnh
2. Đọc chữ trên ảnh (tiếng Việt/Anh) để xác định tên chính xác
3. Tránh trả lời chung chung như "trung tâm thương mại", "khu mua sắm"
4. Nếu thấy logo AEON → "AEON Mall Tân Phú" hoặc tên cụ thể khác
5. Nếu thấy logo Vincom → "Vincom Center Đồng Khởi" hoặc tên cụ thể

Địa danh tham khảo ở TP.HCM:
- {landmarks_list}

QUY TẮC:
- Nếu nhận diện được TÊN CỤ THỂ từ biển hiệu/logo: confidence = "high"
- Nếu chỉ đoán dựa vào kiến trúc: confidence = "medium" 
- Nếu không chắc chắn: landmark = "Không rõ địa danh", confidence = "low"

CHỈ TRẢ VỀ JSON HỢP LỆ, KHÔNG CÓ TEXT NÀO KHÁC."""
    
    try:
        result = get_image_analysis(image_pil, prompt)
        # Parse JSON response
        import json
        import re
        
        # Try to extract JSON from response if it contains extra text
        # Look for JSON pattern with support for nested objects
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            data = json.loads(json_str)
        else:
            # If no JSON found, try to parse the whole response
            data = json.loads(result)
        
        # Tra cứu thông tin địa danh từ database hoặc geocoding
        landmark_name = data.get("landmark", "")
        if landmark_name and landmark_name.lower() != "không rõ địa danh":
            print(f"[RECOGNIZE] Looking up info for: {landmark_name}")
            location_info = find_landmark_info(landmark_name)
            data["lat"] = location_info.get("lat")
            data["lon"] = location_info.get("lon")
            data["address"] = location_info.get("address")
            print(f"[RECOGNIZE] Found: lat={data['lat']}, lon={data['lon']}, address={data['address']}")
        else:
            data["lat"] = None
            data["lon"] = None
            data["address"] = None
        
        return data
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return the text as description
        return {
            "landmark": "Không rõ địa danh",
            "description": result[:200] if result else "Không có mô tả",
            "confidence": "low",
            "lat": None,
            "lon": None,
            "address": None
        }
    except Exception as e:
        return {
            "landmark": "Không rõ địa danh",
            "description": f"Lỗi: {str(e)[:50]}",
            "confidence": "low",
            "lat": None,
            "lon": None,
            "address": None
        }


def detect_landmark_strict(pil_img, retries=3):
    """Nhận dạng địa danh với độ chính xác cao - thử nhiều lần với các biến thể ảnh."""
    from PIL import ImageEnhance, ImageFilter
    
    if not OPENAI_ENABLED:
        raise ValueError("OpenAI API chưa khả dụng")
    
    def ask(img):
        """Gọi API nhận dạng địa danh."""
        try:
            prompt = """Nhận dạng địa danh trong ảnh này.
Chỉ trả về TÊN ĐẦY ĐỦ của địa danh bằng tiếng Việt nếu bạn CHẮC CHẮN nhận ra.
Nếu không chắc chắn, trả về 'Không rõ địa danh'.
Chỉ trả về TÊN, không giải thích thêm."""
            result = get_image_analysis(img, prompt)
            return result.strip() if result else ""
        except Exception:
            return ""
    
    def is_valid_result(name):
        """Kiểm tra kết quả có hợp lệ không."""
        if not name:
            return False
        name_lower = name.lower()
        invalid_responses = [
            "không rõ địa danh", 
            "không rõ", 
            "không xác định",
            "không có địa danh",
            "không chắc chắn",
            "n/a",
            "unknown"
        ]
        return not any(invalid in name_lower for invalid in invalid_responses)
    
    # 1. Thử với ảnh gốc (retries lần)
    print(f"[RECOGNIZE] Trying original image ({retries} attempts)...")
    for _ in range(retries):
        name = ask(pil_img)
        if is_valid_result(name):
            print(f"[RECOGNIZE] ✅ Found with original: {name}")
            return name
    
    # 2. Thử resize với nhiều tỷ lệ khác nhau
    w, h = pil_img.size
    for scale in [1.5, 0.75, 2.0, 0.5]:
        print(f"[RECOGNIZE] Trying scale {scale}x...")
        resized = pil_img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        for _ in range(retries):
            name = ask(resized)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with scale {scale}x: {name}")
                return name
    
    # 3. Tăng độ sắc nét (sharpness)
    try:
        print(f"[RECOGNIZE] Trying sharpness enhancement...")
        enhancer = ImageEnhance.Sharpness(pil_img)
        sharpened = enhancer.enhance(2.0)
        for _ in range(retries):
            name = ask(sharpened)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with sharpness: {name}")
                return name
    except Exception:
        pass
    
    # 4. Tăng độ tương phản (contrast)
    try:
        print(f"[RECOGNIZE] Trying contrast enhancement...")
        enhancer = ImageEnhance.Contrast(pil_img)
        contrasted = enhancer.enhance(1.5)
        for _ in range(retries):
            name = ask(contrasted)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with contrast: {name}")
                return name
    except Exception:
        pass
    
    # 5. Tăng độ sáng (brightness) - hữu ích cho ảnh tối
    try:
        print(f"[RECOGNIZE] Trying brightness enhancement...")
        enhancer = ImageEnhance.Brightness(pil_img)
        brightened = enhancer.enhance(1.3)
        for _ in range(retries):
            name = ask(brightened)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with brightness: {name}")
                return name
    except Exception:
        pass
    
    # 6. Áp dụng bộ lọc làm sắc nét (SHARPEN filter)
    try:
        print(f"[RECOGNIZE] Trying SHARPEN filter...")
        filtered = pil_img.filter(ImageFilter.SHARPEN)
        for _ in range(retries):
            name = ask(filtered)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with SHARPEN filter: {name}")
                return name
    except Exception:
        pass
    
    # 7. Tăng chất lượng ảnh qua nén JPEG cao
    try:
        print(f"[RECOGNIZE] Trying high-quality JPEG compression...")
        buf = BytesIO()
        pil_img.convert("RGB").save(buf, format="JPEG", quality=95, optimize=True)
        buf.seek(0)
        img_enhanced = Image.open(buf)
        for _ in range(retries):
            name = ask(img_enhanced)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with JPEG optimization: {name}")
                return name
    except Exception:
        pass
    
    # 8. Kết hợp nhiều kỹ thuật: Sharpness + Contrast
    try:
        print(f"[RECOGNIZE] Trying combined enhancement (Sharpness + Contrast)...")
        img_combo = pil_img.copy()
        img_combo = ImageEnhance.Sharpness(img_combo).enhance(1.8)
        img_combo = ImageEnhance.Contrast(img_combo).enhance(1.3)
        for _ in range(retries):
            name = ask(img_combo)
            if is_valid_result(name):
                print(f"[RECOGNIZE] ✅ Found with combined enhancement: {name}")
                return name
    except Exception:
        pass
    
    print(f"[RECOGNIZE] ❌ Failed to recognize landmark after all attempts")
    raise ValueError("Không nhận diện được địa danh sau nhiều lần thử với các kỹ thuật khác nhau")

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
    """Phát hiện vị trí từ ảnh (GPS hoặc OpenAI Vision API)."""
    # Thử lấy GPS từ EXIF
    gps = get_gps_from_image(image_file)
    if gps:
        lat, lon = gps
        place = reverse_geocode(lat, lon)
        if place:
            return place
   
    # Nếu không có GPS, dùng OpenAI Vision API
    try:
        if OPENAI_ENABLED:
            result = get_landmark_from_image(image_pil)
            return result if result else "Không xác định"
        else:
            return "Không thể nhận diện (OpenAI API chưa khả dụng)"
    except Exception:
        return None

def analyze_image(image_file_or_pil, analysis_type="landmark"):
    """
    Hàm chính để phân tích ảnh sử dụng OpenAI Vision API.
    
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