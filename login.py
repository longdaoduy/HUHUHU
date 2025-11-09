import streamlit as st
import streamlit_authenticator as stauth
import json
import os
def loadUser():
    if not os.path.exists("Users.json"):
        return {"users" : []}
    with open("Users.json", "r", encoding = "utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users" : []}
    
#Lưu thông tin ngwoif dùng
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

    
    
            
