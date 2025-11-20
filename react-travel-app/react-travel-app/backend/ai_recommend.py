import json
import unidecode
from openai import OpenAI
#Đọc file Destination
client = OpenAI(api_key = "")
def loadDestination():
    """
    Hàm này được SỬA LẠI.
    Bây giờ nó sẽ xử lý trước (pre-process) cả TÊN và TAGS
    để việc tìm kiếm nhanh và chính xác 100%.
    """
    destinations = []
    with open("database.json", "r", encoding = "utf-8") as f:
        data = json.load(f)
    
    for destination in data:
        raw_tags = destination.get("tags", [])
        dest_name = destination.get("name", "") # Lấy tên

        # 1. Giữ tag gốc để hiển thị
        display_tags = [tag.strip().lower() for tag in raw_tags]
        
        # 2. Tạo set (tập hợp) chứa tất cả TỪ ĐƠN LẺ (để tìm từ)
        #    Đây là chìa khóa để sửa lỗi "chợ" vs "chơi"
        search_words = set()
        
        # 3. Tạo list (danh sách) chứa các CỤM ĐẦY ĐỦ (để tìm cụm)
        search_phrases = []

        # --- Xử lý TÊN ---
        # Ví dụ: "Chợ Bến Thành" -> "cho ben thanh"
        norm_name = unidecode.unidecode(dest_name.lower())
        # Thêm cụm từ "cho ben thanh" vào danh sách
        search_phrases.append(norm_name)
        # Tách "cho ben thanh" thành {"cho", "ben", "thanh"}
        search_words.update(norm_name.split())
        
        # --- Xử lý TAGS ---
        for tag in raw_tags:
            # Ví dụ: "vui chơi" -> "vui choi"
            norm_tag_phrase = unidecode.unidecode(tag.lower())
            
            # Thêm cụm từ "vui choi" vào danh sách
            search_phrases.append(norm_tag_phrase)
            
            # Tách "vui choi" thành {"vui", "choi"}
            search_words.update(norm_tag_phrase.split())
        
        # Thêm các trường đã xử lý vào dictionary
        destinations.append({
            "name" : dest_name, # Tên gốc
            "location" : destination.get("location"),
            "tags" : display_tags, # Tag gốc
            
            # 2 trường mới dùng cho tìm kiếm SIÊU CHÍNH XÁC
            "search_words": search_words,   # Set: {"vui", "choi", "thao", "cam", "vien"...}
            "search_phrases": search_phrases, # List: ["vui choi", "thao cam vien"...]
            
            "introduction" : destination.get("introduction"),
            "price" : destination.get("price (VNĐ)"),
            "rating" : destination.get("rating"),
            "lat" : destination.get("lat"),
            "lon" : destination.get("lon"),
            "review" : destination.get("review"),
            "province" : destination.get("province"),
            "images": destination.get("images", [])
        })

    return destinations

#Tính độ tương thích địa điểm
def compatibality_rate(preference, destination):
    """
    Hàm này được SỬA LẠI (LOGIC MỚI).
    Chỉ trả về kết quả nếu TẤT CẢ các từ bạn gõ
    đều có trong Tên hoặc Tags của địa điểm.
    """
    score = 0
    
    # 1. Chuẩn bị sở thích (preference)
    # Ví dụ: "bến thành" -> {"ben", "thanh"}
    pref_words = set(unidecode.unidecode(preference.lower()).split())
    
    # Nếu người dùng không gõ gì, không làm gì cả
    if not pref_words:
        return 0

    # 2. Lấy TẬP HỢP TỪ KHÓA của địa điểm (đã xử lý ở loadDestination)
    # Ví dụ: {"cho", "ben", "thanh", "mua", "sam", ...}
    dest_words = destination.get("search_words", set())

    # 3. Tính điểm (Logic "Tất cả phải khớp")
    # Kiểm tra xem TẤT CẢ các từ người dùng gõ
    # có phải là TẬP CON (subset) của các từ khóa địa điểm không.
    #
    # Ví dụ: pref_words = {"ben", "thanh"}
    #        dest_words = {"cho", "ben", "thanh"}
    #        Hàm issubset() trả về TRUE.
    #
    # Ví dụ: pref_words = {"ben", "thanh"}
    #        dest_words = {"ben", "nha", "rong"}
    #        Hàm issubset() trả về FALSE (vì thiếu "thanh").
    #
    if pref_words.issubset(dest_words):
        # Cho điểm cao để nó được chọn
        # Cộng thêm số lượng từ để ưu tiên khớp nhiều từ hơn
        # (ví dụ: "chợ bến thành" (3 từ) sẽ thắng "chợ bến" (2 từ))
        score = 10 + len(pref_words)
        
    return score

#Recommend theo tags
def recommend(preference, destination):
    preference = preference.lower()

    results = []
    for dest in destination:
        score = compatibality_rate(preference, dest)
        if score > 0:
            results.append((dest, score))
    #Sắp xếp giảm dần theo điểm số tương thích
    results.sort(key = lambda x : x[1], reverse = True)

    return [d[0] for d in results[:5]]

#Recommend bằng AI
def ai_recommend(user_input, places_data):
    if not user_input.strip():
        return "Vui long nhập sở thích của bạn."
    
    prompt = f"""
    Bạn là AI gợi ý du lịch. 
    Người dùng nói: "{user_input}".
    Dưới đây là danh sách địa điểm:
    {places_data}
    Hãy chọn ra 3 địa điểm phù hợp nhất và giải thích ngắn gọn lý do.
    """
    try:
        response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
                {"role": "system", "content": "Bạn là AI chuyên gia tư vấn du lịch thông minh."},
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        return f"Lỗi khi gọi API: {str(e)}"

    return response.choices[0].message.content


    
