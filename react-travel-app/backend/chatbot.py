import json
from datetime import datetime
from typing import List, Optional
from ai_recommend import ai_recommend, recommend, loadDestination

class TravelChatbot:
    """
    Chatbot du lịch thông minh sử dụng AI để gợi ý địa điểm.
    """
    
    def __init__(self):
        self.destinations = loadDestination()
        self.conversation_history = []
        self.chat_sessions = {}
    
    def format_destinations_for_ai(self, destinations: List[dict]) -> str:
        """
        Chuyển danh sách địa điểm thành chuỗi để gửi cho AI.
        """
        formatted = "Danh sách địa điểm du lịch:\n"
        for i, dest in enumerate(destinations, 1):
            formatted += f"\n{i}. {dest.get('name', 'N/A')}\n"
            formatted += f"   - Vị trí: {dest.get('location', 'N/A')}\n"
            formatted += f"   - Mô tả: {dest.get('introduction', 'N/A')}\n"
            formatted += f"   - Giá vé: {dest.get('price', 'N/A')} VNĐ\n"
            formatted += f"   - Đánh giá: {dest.get('rating', 'N/A')}/5\n"
        return formatted
    
    def chat(self, user_message: str, use_ai: bool = True) -> dict:
        """
        Xử lý tin nhắn từ người dùng và trả về gợi ý.
        
        Args:
            user_message: Tin nhắn từ người dùng
            use_ai: Sử dụng AI để gợi ý (True) hay sử dụng regex matching (False)
        
        Returns:
            dict: Chứa response và recommended destinations
        """
        if not user_message.strip():
            return {
                "status": "error",
                "message": "Vui lòng nhập sở thích của bạn."
            }
        
        # Lưu lịch sử cuộc trò chuyện
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "type": "user"
        })
        
        try:
            if use_ai:
                # Sử dụng AI để gợi ý
                ai_response = ai_recommend(user_message, self.format_destinations_for_ai(self.destinations))
                
                # Cũng lấy kết quả matching cho tham khảo
                matching_results = recommend(user_message, self.destinations)
                
                response_text = ai_response
            else:
                # Sử dụng regex matching thuần
                matching_results = recommend(user_message, self.destinations)
                
                if not matching_results:
                    response_text = f"Xin lỗi, không tìm thấy địa điểm nào phù hợp với '{user_message}'.\nVui lòng thử với các từ khóa khác như: du lịch, mua sắm, ăn uống, thể thao, v.v."
                else:
                    response_text = f"Tôi đã tìm thấy {len(matching_results)} địa điểm phù hợp với sở thích '{user_message}' của bạn."
            
            # Lưu response
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "assistant": response_text,
                "type": "assistant"
            })
            
            result = {
                "status": "success",
                "message": response_text,
                "use_ai": use_ai,
                "recommendations": []
            }
            
            # Thêm thông tin chi tiết về các địa điểm gợi ý
            if use_ai and 'matching_results' in locals():
                result["recommendations"] = [
                    {
                        "name": dest.get("name"),
                        "location": dest.get("location"),
                        "introduction": dest.get("introduction"),
                        "price": dest.get("price"),
                        "rating": dest.get("rating"),
                        "images": dest.get("images", [])
                    }
                    for dest in matching_results[:5]
                ]
            elif not use_ai and matching_results:
                result["recommendations"] = [
                    {
                        "name": dest.get("name"),
                        "location": dest.get("location"),
                        "introduction": dest.get("introduction"),
                        "price": dest.get("price"),
                        "rating": dest.get("rating"),
                        "images": dest.get("images", [])
                    }
                    for dest in matching_results[:5]
                ]
            
            return result
        
        except Exception as e:
            error_msg = f"Lỗi xảy ra: {str(e)}"
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "assistant": error_msg,
                "type": "error"
            })
            return {
                "status": "error",
                "message": error_msg
            }
    
    def get_conversation_history(self) -> List[dict]:
        """
        Lấy lịch sử cuộc trò chuyện.
        """
        return self.conversation_history
    
    def clear_history(self):
        """
        Xóa lịch sử cuộc trò chuyện.
        """
        self.conversation_history = []
    
    def get_quick_suggestions(self) -> List[str]:
        """
        Lấy danh sách gợi ý nhanh dựa trên các tags phổ biến.
        """
        tags_count = {}
        for dest in self.destinations:
            for tag in dest.get("tags", []):
                tags_count[tag] = tags_count.get(tag, 0) + 1
        
        # Sắp xếp theo số lần xuất hiện
        sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, count in sorted_tags[:10]]
    
    def search_by_tags(self, tags: List[str]) -> List[dict]:
        """
        Tìm kiếm địa điểm theo danh sách tags.
        """
        results = []
        for dest in self.destinations:
            dest_tags = [tag.lower() for tag in dest.get("tags", [])]
            for search_tag in tags:
                if search_tag.lower() in dest_tags:
                    results.append(dest)
                    break
        return results
    
    def search_by_price_range(self, min_price: int, max_price: int) -> List[dict]:
        """
        Tìm kiếm địa điểm theo khoảng giá.
        """
        results = []
        for dest in self.destinations:
            price = dest.get("price", 0)
            if isinstance(price, str):
                # Loại bỏ các ký tự không phải số
                price_str = ''.join(c for c in price if c.isdigit())
                price = int(price_str) if price_str else 0
            
            if min_price <= price <= max_price:
                results.append(dest)
        return results
    
    def get_top_rated(self, limit: int = 5) -> List[dict]:
        """
        Lấy các địa điểm được đánh giá cao nhất.
        """
        sorted_dests = sorted(
            self.destinations,
            key=lambda x: float(x.get("rating", 0)),
            reverse=True
        )
        return sorted_dests[:limit]


# Khởi tạo chatbot global
chatbot_instance = TravelChatbot()
