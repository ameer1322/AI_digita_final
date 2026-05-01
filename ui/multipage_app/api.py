from datetime import datetime, timezone

import httpx
import jwt
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

def is_token_expired(token: str)-> bool:
    try:
        payload = jwt.decode(token, options={"verify_signature":False})
        exp = payload.get("exp")
        if exp is None:
            return True
        return datetime.now(timezone.utc).timestamp() > exp
    except jwt.PyJWTError:
        return True

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

def get_products_by_name(name:str):
    url = f"{BASE_URL}/products/{name}"
    response = httpx.get(url)
    return response

def add_to_cart(product_name: str, quantity:int):
    url = f"{BASE_URL}/order/"
    token = st.session_state.get("access_token")
    response = httpx.put(
        url,
        json={"product_name":product_name,"quantity":quantity},
        headers={"Authorization":f"Bearer: {token}"}
    )
    return response

def add_to_favorites(product_name:str):
    url = f"{BASE_URL}/products/add_to_favorites"
    token = st.session_state.get("access_token")
    response = httpx.put(
        url,
        json={"product_name":product_name},
        headers = {"Authorization":f"Bearer: {token}"}
    )
    return response

def get_user_unconfirmed_order():
    url = f"{BASE_URL}/order/get_user_unconfirmed_order"
    token = st.session_state.get("access_token")
    response = httpx.get(
        url,
        headers = {"Authorization":f"Bearer: {token}"}
    )
    return response


def get_user_confirmed_orders():
    url = f"{BASE_URL}/order/get_user_confirmed_orders"
    token = st.session_state.get("access_token")
    response = httpx.get(
        url,
        headers = {"Authorization" : f"Bearer: {token}"}
    )
    return response


def remove_from_order(product_name:str, amount:int):
    url = f"{BASE_URL}/order/remove_from_order"
    token = st.session_state.get("access_token")
    response = httpx.put(
        url,
        json={"product_name":product_name,"amount":amount},
        headers = {"Authorization": f"Bearer: {token}"}
    )
    return response

def confirm_order():
    url = f"{BASE_URL}/order/confirm_order"
    token = st.session_state.get("access_token")
    response = httpx.put(
        url,
        headers = {"Authorization": f"Bearer: {token}"}
    )
    print(response)
    return response

