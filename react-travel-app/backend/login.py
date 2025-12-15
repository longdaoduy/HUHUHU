import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import base64
import json
import os
ALBUM_FILE = "Users_album.json"
def loadUserAlbum(username):
    if not os.path.exists(ALBUM_FILE):
        return {}
    with open(ALBUM_FILE, 'r',encoding='utf-8') as f:
        try:
            all_album = json.load(f)
        except json.JSONDecodeError:
            return {}
    #Lấy album của người
    user_album = all_album.get(username ,{})
    loaded_albums = {}
    for album_name, items in user_album.items():
        loaded_albums[album_name] = []
        for item in items:
            #Tạo bản sao item
            new_item = item.copy()
            if 'bytes' in new_item and isinstance(new_item['bytes'], str):
                try:
                    # Giải mã chuỗi Base64 trở lại thành dữ liệu bytes
                    decoded_bytes = base64.b64decode(new_item['bytes'])
                    new_item['bytes'] = decoded_bytes
                except:
                    # Nếu giải mã lỗi, gán None để báo lỗi dữ liệu
                    new_item['bytes'] = None
            loaded_albums[album_name].append(new_item)
    
    return loaded_albums

def saveUserAlbums(username, user_albums):
    """
    Lưu dữ liệu album của người dùng vào file JSON.
    Mã hóa bytes ảnh thành chuỗi Base64.
    """
    
    # Tải tất cả dữ liệu hiện có để tránh ghi đè người dùng khác
    if os.path.exists(ALBUM_FILE):
        with open(ALBUM_FILE, 'r', encoding='utf-8') as f:
            try:
                all_albums_data = json.load(f)
            except json.JSONDecodeError:
                all_albums_data = {}
    else:
        all_albums_data = {}

    #Mã hóa (Base64) dữ liệu của người dùng hiện tại
    albums_to_save = {}
    for album_name, items in user_albums.items():
        albums_to_save[album_name] = []
    
        for item in items:
            # Tạo bản sao để không làm thay đổi item trong session_state
            new_item = item.copy() 
            
            # Mã hóa bytes ảnh sang chuỗi Base64 để lưu vào JSON
            if 'bytes' in new_item and isinstance(new_item['bytes'], bytes):
                encoded_bytes = base64.b64encode(new_item['bytes']).decode('utf-8')
                new_item['bytes'] = encoded_bytes
    
            albums_to_save[album_name].append(new_item)

    # Cập nhật và ghi lại toàn bộ file
    all_albums_data[username] = albums_to_save
    
    with open(ALBUM_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_albums_data, f, indent=4, ensure_ascii=False)


def loadUser():
    if not os.path.exists("Users.json"):
        return {"users" : []}
    with open("Users.json", "r", encoding = "utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users" : []}
    
#Lưu thông tin người dùng
def saveUser(data):
    with open("Users.json", "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
#Giao diên phần đăng nhập
def screen_signupform():
    st.title("Đăng kí tài khoản mới")
    new_name = st.text_input("Tên hiển thị")
    new_username = st.text_input("Tên người dùng")
    new_password = st.text_input("Mật khẩu", type = "password")
    if st.button("Đăng ký"):
        data = loadUser()
        users = data["users"]

        if any(u["username"] == new_username for u in users):
            st.error("⚠️ Tên đăng nhập đã tồn tại!")
        elif not new_name or not new_username or not new_password:
            st.warning("Vui lòng nhập đầy đủ thông tin.")
        else:
            users.append({
                "name": new_name,
                "username": new_username,
                "password": new_password
            })
            saveUser(data)
            st.success("✅ Đăng ký thành công! Vui lòng đăng nhập.")
            st.session_state.show_signup = False  # Quay lại login
        
#Giao diễn phần login
def screen_login_page(data):
    
    credentials = {"usernames": {}}
    for user in data["users"]:
        credentials["usernames"][user["username"]] = {
            "email": "",
            "name": user["name"],
            "password": user["password"]
        }

    authenticator = stauth.Authenticate(
        credentials,
        "urbanquest_cookie",
        "abcdef123456",
        30
    )

    result = authenticator.login(fields="Đăng nhập", location = "main")

    if result is not None:
        name, auth_status, username = result
        if auth_status is True:
            st.session_state.name = name # LƯU TÊN HIỂN THỊ
            st.session_state.username = username
        elif auth_status is False:
            st.error("❌ Sai tài khoản hoặc mật khẩu.")

    return authenticator

    
    
            
