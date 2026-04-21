import httpx
import streamlit as st
BASE_URL = "http://localhost:8000"



def register_user( first_name, last_name, age, email, phone, address, username, password):
    url = f"{BASE_URL}/auth/signup"
    payload = {
        "first_name":first_name,
        "last_name":last_name,
        "age":age,
        "email":email,
        "phone":phone,
        "address":address,
        "username": username,
        "password":password
    }
    response = httpx.post(url, json=payload)
    if response.status_code == 201:
        token = response.cookies.get("access_token")
        st.session_state["access_token"] = token
        st.rerun()
    return response

def login_user(username, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"username": username, "password": password}
    response = httpx.post(url, json=payload)
    if response.status_code == 200:
        token = response.cookies.get("access_token")
        st.session_state["access_token"] = token
        st.rerun()
    return response