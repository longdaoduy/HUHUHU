"""
Social Feed Module - Quản lý posts, comments, likes cho chức năng mạng xã hội
"""

from datetime import datetime
from typing import List, Dict, Optional
import json
import os

# File lưu trữ posts và comments
POSTS_FILE = "social_posts.json"
COMMENTS_FILE = "social_comments.json"
LIKES_FILE = "social_likes.json"

class SocialFeedManager:
    def __init__(self):
        self.posts = self.load_posts()
        self.comments = self.load_comments()
        self.likes = self.load_likes()
    
    def load_posts(self) -> Dict:
        """Load posts từ file"""
        if os.path.exists(POSTS_FILE):
            try:
                with open(POSTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def load_comments(self) -> Dict:
        """Load comments từ file"""
        if os.path.exists(COMMENTS_FILE):
            try:
                with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def load_likes(self) -> Dict:
        """Load likes từ file"""
        if os.path.exists(LIKES_FILE):
            try:
                with open(LIKES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_posts(self):
        """Lưu posts vào file"""
        with open(POSTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.posts, f, ensure_ascii=False, indent=2)
    
    def save_comments(self):
        """Lưu comments vào file"""
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.comments, f, ensure_ascii=False, indent=2)
    
    def save_likes(self):
        """Lưu likes vào file"""
        with open(LIKES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.likes, f, ensure_ascii=False, indent=2)
    
    def create_post(self, user_email: str, content: str, image_data: Optional[str] = None, 
                   location: Optional[str] = None, user_avatar: Optional[str] = None,
                   user_fullname: Optional[str] = None) -> Dict:
        """Tạo post mới"""
        post_id = f"post_{datetime.now().timestamp()}"
        
        post = {
            "post_id": post_id,
            "user_email": user_email,
            "user_avatar": user_avatar,
            "user_fullname": user_fullname,
            "content": content,
            "image_data": image_data,
            "location": location,
            "created_at": datetime.now().isoformat(),
            "likes_count": 0,
            "comments_count": 0
        }
        
        self.posts[post_id] = post
        self.save_posts()
        
        return post
    
    def get_posts(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Lấy danh sách posts (newest first)"""
        posts_list = list(self.posts.values())
        # Sort by created_at descending
        posts_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        # Apply pagination
        return posts_list[offset:offset + limit]
    
    def get_post_by_id(self, post_id: str) -> Optional[Dict]:
        """Lấy post theo ID"""
        return self.posts.get(post_id)
    
    def get_user_posts(self, user_email: str, limit: int = 20) -> List[Dict]:
        """Lấy posts của một user"""
        user_posts = [p for p in self.posts.values() if p.get('user_email') == user_email]
        user_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return user_posts[:limit]
    
    def delete_post(self, post_id: str, user_email: str) -> bool:
        """Xóa post (chỉ user tạo post mới được xóa)"""
        post = self.posts.get(post_id)
        if not post:
            return False
        
        if post.get('user_email') != user_email:
            return False
        
        # Xóa post
        del self.posts[post_id]
        
        # Xóa comments của post
        if post_id in self.comments:
            del self.comments[post_id]
        
        # Xóa likes của post
        if post_id in self.likes:
            del self.likes[post_id]
        
        self.save_posts()
        self.save_comments()
        self.save_likes()
        
        return True
    
    def add_comment(self, post_id: str, user_email: str, content: str, user_avatar: str = None, user_fullname: str = None) -> Optional[Dict]:
        """Thêm comment vào post"""
        if post_id not in self.posts:
            return None
        
        comment_id = f"comment_{datetime.now().timestamp()}"
        
        comment = {
            "comment_id": comment_id,
            "post_id": post_id,
            "user_email": user_email,
            "user_avatar": user_avatar,
            "user_fullname": user_fullname,
            "content": content,
            "created_at": datetime.now().isoformat()
        }
        
        # Khởi tạo list comments cho post nếu chưa có
        if post_id not in self.comments:
            self.comments[post_id] = []
        
        self.comments[post_id].append(comment)
        
        # Cập nhật comment count
        self.posts[post_id]['comments_count'] = len(self.comments[post_id])
        
        self.save_comments()
        self.save_posts()
        
        return comment
    
    def get_comments(self, post_id: str) -> List[Dict]:
        """Lấy comments của một post"""
        comments = self.comments.get(post_id, [])
        # Sort by created_at ascending (oldest first)
        comments.sort(key=lambda x: x.get('created_at', ''))
        return comments
    
    def delete_comment(self, post_id: str, comment_id: str, user_email: str) -> bool:
        """Xóa comment"""
        if post_id not in self.comments:
            return False
        
        comments = self.comments[post_id]
        
        for i, comment in enumerate(comments):
            if comment.get('comment_id') == comment_id:
                # Chỉ user tạo comment hoặc user tạo post mới được xóa
                post = self.posts.get(post_id)
                if comment.get('user_email') == user_email or (post and post.get('user_email') == user_email):
                    comments.pop(i)
                    
                    # Cập nhật comment count
                    self.posts[post_id]['comments_count'] = len(comments)
                    
                    self.save_comments()
                    self.save_posts()
                    return True
        
        return False
    
    def toggle_like(self, post_id: str, user_email: str) -> Dict:
        """Toggle like/unlike post"""
        if post_id not in self.posts:
            return {"success": False, "message": "Post not found"}
        
        # Khởi tạo set likes cho post nếu chưa có
        if post_id not in self.likes:
            self.likes[post_id] = []
        
        likes_list = self.likes[post_id]
        
        if user_email in likes_list:
            # Unlike
            likes_list.remove(user_email)
            self.posts[post_id]['likes_count'] = len(likes_list)
            self.save_likes()
            self.save_posts()
            return {"success": True, "action": "unliked", "likes_count": len(likes_list)}
        else:
            # Like
            likes_list.append(user_email)
            self.posts[post_id]['likes_count'] = len(likes_list)
            self.save_likes()
            self.save_posts()
            return {"success": True, "action": "liked", "likes_count": len(likes_list)}
    
    def get_likes(self, post_id: str) -> List[str]:
        """Lấy danh sách users đã like post"""
        return self.likes.get(post_id, [])
    
    def is_liked_by_user(self, post_id: str, user_email: str) -> bool:
        """Kiểm tra user đã like post chưa"""
        return user_email in self.likes.get(post_id, [])

# Global instance
social_feed_manager = SocialFeedManager()
