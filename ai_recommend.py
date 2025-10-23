import csv
from openai import OpenAI
#Đọc file Destination
client = OpenAI(api_key = " ")
def loadDestination():
    destinations = []
    with open("destination.csv", "r", encoding = "utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            #Chia tags bằng dấu phẩy
            tags = [tag.strip().lower() for tag in row["tags"].split(',')]
            destinations.append({
                "name": row["name"],
                "location" : row["location"],
                "tags" : tags
            })
    return destinations

#Tính độ tương thích địa điểm
def compatibality_rate(preference, destination):
    score = 0
    tags = " ".join(destination.get("tags", [])).lower()
    for word in preference.split():
        if word in tags:
            score += 1

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


    
