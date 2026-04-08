import httpx

BASE_URL = "http://localhost:8000"



def register_user(username, first_name, last_name, password, email):
    url = f"{BASE_URL}/users/"
    payload = {
        "first_name":first_name,
        "last_name":last_name,
        "username": username,
        "password":password,
        "email":email
    }
    response = httpx.post(url, json=payload)
    return response

