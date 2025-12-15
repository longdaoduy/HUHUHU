"""
Quick script to check current album storage state
"""
import requests

BASE_URL = "http://localhost:8000"

print("Checking current albums...")
response = requests.get(f"{BASE_URL}/api/albums")

if response.status_code == 200:
    data = response.json()
    albums = data.get('albums', {})
    print(f"\nFound {len(albums)} album(s):\n")
    
    for album_name, info in albums.items():
        print(f"📁 {album_name}")
        print(f"   - Images: {info.get('image_count', 0)}")
        print(f"   - Last modified: {info.get('last_modified', 'N/A')}")
        print()
        
        # Get detailed info
        detail_response = requests.get(f"{BASE_URL}/api/albums/{album_name}/images?include_images=false")
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            images = detail_data.get('images', [])
            if images:
                print(f"   First image info:")
                first_img = images[0]
                print(f"      - Filename: {first_img.get('filename')}")
                print(f"      - Landmark: {first_img.get('landmark')}")
                print(f"      - Has image_data in response: {'image_data' in first_img}")
                print()
else:
    print(f"Failed to get albums: {response.status_code}")
    print(response.text)
