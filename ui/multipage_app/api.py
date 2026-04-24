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

def logout():
    url = f"{BASE_URL}/auth/logout"
    token = st.session_state.get("access_token")
    response = httpx.post(url, cookies={"access_token":token})
    if response.status_code == 200:
        st.session_state["access_token"]=None
        st.rerun()
    return response

def get_all_products():
    url = f"{BASE_URL}/products/"
    response = httpx.get(url)
    return response

def get_items_by_name(name:str):
    url = f"{BASE_URL}/products/{name}"
    response = httpx.get(url)
    return response

