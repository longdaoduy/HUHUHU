"""
Vietnam Travel App - API Integration Test
Tệp này để kiểm tra các endpoint authentication
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Test data
test_user = {
    "fullname": "Nguyễn Văn Test",
    "email": "test@example.com",
    "phone": "0123456789",
    "password": "Test123456"
}

login_data = {
    "email": "test@example.com",
    "password": "Test123456"
}

def test_register():
    """Test đăng ký."""
    print("=== Testing Register ===")
    response = requests.post(f"{BASE_URL}/api/register", json=test_user)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def test_login():
    """Test đăng nhập."""
    print("\n=== Testing Login ===")
    response = requests.post(f"{BASE_URL}/api/login", json=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def test_get_profile(token):
    """Test lấy profile."""
    print("\n=== Testing Get Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/user/profile", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_logout(token):
    """Test đăng xuất."""
    print("\n=== Testing Logout ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/logout", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("Starting API tests...\n")
    
    # Register
    reg_result = test_register()
    
    # Login
    login_result = test_login()
    
    if login_result.get("success"):
        token = login_result.get("token")
        
        # Get profile
        test_get_profile(token)
        
        # Logout
        test_logout(token)
    
    print("\n✅ Tests completed!")
