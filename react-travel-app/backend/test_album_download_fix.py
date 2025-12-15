"""
Test script to verify album download functionality
"""
import requests
import base64
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("TEST ALBUM DOWNLOAD FUNCTIONALITY")
print("=" * 70)

# Step 1: Create test album
album_name = "test_download_album"
print(f"\n1. Creating test album: {album_name}")

response = requests.post(f"{BASE_URL}/api/albums", json={"name": album_name})
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✅ Album created")
else:
    print(f"   Response: {response.text}")

# Step 2: Create test image
print(f"\n2. Creating test image...")
img = Image.new('RGB', (400, 300), color='blue')
img_buffer = BytesIO()
img.save(img_buffer, format='JPEG')
img_bytes = img_buffer.getvalue()
print(f"   ✅ Test image created: {len(img_bytes)} bytes")

# Step 3: Upload image to album
print(f"\n3. Uploading image to album...")
files = {
    'files': ('test_image.jpg', img_bytes, 'image/jpeg')
}
data = {
    'auto_recognize': 'false'
}

response = requests.post(
    f"{BASE_URL}/api/albums/{album_name}/images",
    files=files,
    data=data
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"   ✅ Upload result: {result.get('message', '')}")
    print(f"   Added: {result.get('added_count', 0)}/{result.get('total_count', 0)}")
else:
    print(f"   ❌ Upload failed: {response.text}")
    exit(1)

# Step 4: Check album contents
print(f"\n4. Checking album contents...")
response = requests.get(f"{BASE_URL}/api/albums/{album_name}/images")
if response.status_code == 200:
    result = response.json()
    image_count = result.get('total', 0)
    print(f"   ✅ Album has {image_count} image(s)")
    
    if image_count > 0:
        first_image = result.get('images', [])[0]
        print(f"   Image info (from API):")
        print(f"      - Filename: {first_image.get('filename')}")
        print(f"      - Has image_data: {'image_data' in first_image}")
        print(f"      - Has bytes: {'bytes' in first_image}")
        if 'image_data' in first_image:
            img_data_len = len(first_image['image_data']) if first_image['image_data'] else 0
            print(f"      - image_data length: {img_data_len} chars")
else:
    print(f"   ❌ Failed to get album contents: {response.text}")

# Step 4.5: Debug album storage directly
print(f"\n4.5. Checking album storage directly (DEBUG)...")
response = requests.get(f"{BASE_URL}/api/albums/debug/{album_name}")
if response.status_code == 200:
    debug_info = response.json()
    print(f"   ✅ Debug info:")
    print(f"      - Total items in storage: {debug_info.get('total_items')}")
    if debug_info.get('items_info'):
        first_item_debug = debug_info['items_info'][0]
        print(f"      - First item keys: {first_item_debug.get('keys')}")
        print(f"      - Has image_data in storage: {first_item_debug.get('has_image_data')}")
        print(f"      - image_data length: {first_item_debug.get('image_data_length', 0)}")
else:
    print(f"   ❌ Debug failed: {response.text}")

# Step 5: Test download
print(f"\n5. Testing album download...")
response = requests.get(f"{BASE_URL}/api/albums/{album_name}/download")
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    zip_data = response.content
    print(f"   ✅ Downloaded ZIP: {len(zip_data)} bytes")
    
    # Verify it's a valid ZIP
    if zip_data[:2] == b'PK':
        print(f"   ✅ Valid ZIP file (magic number OK)")
        
        # Try to extract and verify
        from zipfile import ZipFile
        try:
            with ZipFile(BytesIO(zip_data), 'r') as zf:
                files_in_zip = zf.namelist()
                print(f"   ✅ ZIP contains {len(files_in_zip)} file(s):")
                for fname in files_in_zip:
                    file_info = zf.getinfo(fname)
                    print(f"      - {fname}: {file_info.file_size} bytes")
        except Exception as e:
            print(f"   ❌ Failed to read ZIP: {e}")
    else:
        print(f"   ❌ Not a valid ZIP file")
        print(f"   First 100 bytes: {zip_data[:100]}")
else:
    print(f"   ❌ Download failed")
    print(f"   Response: {response.text}")

# Step 6: Cleanup
print(f"\n6. Cleaning up test album...")
response = requests.delete(f"{BASE_URL}/api/albums/{album_name}")
if response.status_code == 200:
    print(f"   ✅ Test album deleted")
else:
    print(f"   ⚠️  Failed to delete: {response.text}")

print("\n" + "=" * 70)
print("TEST COMPLETED")
print("=" * 70)
