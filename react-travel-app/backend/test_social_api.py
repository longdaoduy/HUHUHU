"""
Test script để kiểm tra Social Feed API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test với token thật từ login
def test_with_real_token():
    print("=== Testing Social Feed API ===\n")
    
    # Bước 1: Login để lấy token
    print("1. Testing login...")
    login_data = {
        "email": "test@gmail.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                token = result.get("token")
                print(f"✅ Login successful! Token: {token[:20]}...")
                
                # Bước 2: Test tạo post
                print("\n2. Testing create post...")
                headers = {"Authorization": f"Bearer {token}"}
                post_data = {
                    "content": "Test post from API script",
                    "location": "Ho Chi Minh City"
                }
                
                response = requests.post(
                    f"{BASE_URL}/api/social/posts",
                    headers=headers,
                    data=post_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Post created! ID: {result.get('post', {}).get('post_id')}")
                else:
                    print(f"❌ Failed to create post: {response.status_code}")
                    print(f"Response: {response.text}")
                
                # Bước 3: Test lấy danh sách posts
                print("\n3. Testing get posts...")
                response = requests.get(
                    f"{BASE_URL}/api/social/posts",
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    posts = result.get('posts', [])
                    print(f"✅ Found {len(posts)} posts")
                    for post in posts[:3]:
                        print(f"   - {post.get('user_email')}: {post.get('content')[:50]}...")
                else:
                    print(f"❌ Failed to get posts: {response.status_code}")
                    print(f"Response: {response.text}")
                
            else:
                print(f"❌ Login failed: {result.get('message')}")
        else:
            print(f"❌ Login request failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_with_real_token()
