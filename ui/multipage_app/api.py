import httpx

BASE_URL = "http://localhost:8000"



def register_user( first_name, last_name, age, email, phone, address, username, password):
    url = f"{BASE_URL}/users/"
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
    return response

