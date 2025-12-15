import json
import unidecode
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load biến môi trường từ file .env
load_dotenv()

# Sử dụng OpenAI API
print("[AI_RECOMMEND] Using OpenAI API")

# Lấy API key từ environment variable
api_key = os.getenv('OPENAI_API_KEY', '')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please add it to your .env file.")

client = OpenAI(api_key=api_key)
print("[AI_RECOMMEND] OpenAI client initialized successfully")
def loadDestination():
   
    destinations = []
    with open("database.json", "r", encoding = "utf-8") as f:
        data = json.load(f)
    
    for destination in data:
        raw_tags = destination.get("tags", [])
        dest_name = destination.get("name", "") # Lấy tên
        display_tags = [tag.strip().lower() for tag in raw_tags]
        search_words = set()

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
    pref_words = set(unidecode.unidecode(preference.lower()).split())
    
    # Nếu người dùng không gõ gì, không làm gì cả
    if not pref_words:
        return 0

    # 2. Lấy TẬP HỢP TỪ KHÓA của địa điểm (đã xử lý ở loadDestination)
    # Ví dụ: {"cho", "ben", "thanh", "mua", "sam", ...}
    dest_words = destination.get("search_words", set())
    if pref_words.issubset(dest_words):
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

#Recommend bằng AI (sử dụng OpenAI API)
def ai_recommend(user_input, places_data):
    """
    Gợi ý địa điểm sử dụng OpenAI GPT API.
    Cần OPENAI_API_KEY trong file .env
    """
    if not user_input.strip():
        return "Vui lòng nhập sở thích của bạn."
    
    print(f"[AI_RECOMMEND] Processing with OpenAI: {user_input}")
    
    try:
        # Tạo prompt cho OpenAI
        system_prompt = """Bạn là trợ lý du lịch thông minh. Nhiệm vụ của bạn là gợi ý địa điểm du lịch phù hợp nhất dựa trên sở thích của người dùng.
        
Hãy phân tích danh sách địa điểm được cung cấp và chọn ra 3 địa điểm phù hợp nhất.
Trả lời bằng tiếng Việt, ngắn gọn và hữu ích."""
        
        user_prompt = f"""Sở thích của tôi: {user_input}

{places_data}

Hãy gợi ý 3 địa điểm phù hợp nhất và giải thích ngắn gọn tại sao."""
        
        # Gọi OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        print(f"[AI_RECOMMEND] OpenAI response received")
        return ai_response
        
    except Exception as e:
        print(f"[AI_RECOMMEND] OpenAI Error: {e}")
        return f"⚠️ Lỗi khi gọi OpenAI API: {str(e)[:100]}\n\nVui lòng kiểm tra API key trong file .env"


    
