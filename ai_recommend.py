import csv
import unidecode
from openai import OpenAI

#client = OpenAI(api_key="")

def loadDestination():
    destinations = []
<<<<<<< HEAD
    with open("Data.csv", "r", encoding = "utf-8") as f:
=======
    with open("Data.csv", "r", encoding="utf-8") as f:
>>>>>>> 133891d (update ai_recommend.py)
        reader = csv.DictReader(f)
        for row in reader:
            tags = [tag.strip().lower() for tag in row["tags"].split(',')]
            destinations.append({
                "name": row["name"],
                "location": row["location"],
                "tags": tags
            })
    return destinations


def compatibality_rate(preference, destination):
    score = 0
    pref = unidecode.unidecode(preference.lower())
    tags = " ".join(destination.get("tags", [])).lower()
<<<<<<< HEAD
    tags = unidecode.unidecode(tags)

    for word in pref.split():
        if word in tags:
            score += 2
            
    #Nếu cụm từ có trong tags
    if pref in tags:
        score += 5
        
=======
    for word in preference.split():
        if word in tags:
            score += 1
>>>>>>> 133891d (update ai_recommend.py)
    return score


def recommend(preference, destination):
    preference = preference.lower()
    results = []
    for dest in destination:
        score = compatibality_rate(preference, dest)
        if score > 0:
            results.append((dest, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return [d[0] for d in results[:5]]


def ai_recommend(user_input, places_data):
    if not user_input.strip():
        return "Vui lòng nhập sở thích của bạn."

    prompt = f"""
    Bạn là AI gợi ý du lịch.
    Người dùng nói: "{user_input}".
    Dưới đây là danh sách địa điểm:
    {places_data}
    Hãy chọn ra 3 địa điểm phù hợp nhất và giải thích ngắn gọn lý do.
    """

    try:
        response = client.chat.completions.create(
<<<<<<< HEAD
        model = "gpt-5-mini",
        messages=[
=======
            model="gpt-5-mini",
            messages=[
>>>>>>> 133891d (update ai_recommend.py)
                {"role": "system", "content": "Bạn là AI chuyên gia tư vấn du lịch thông minh."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Lỗi khi gọi API: {str(e)}"


    
