from datetime import datetime

import jwt
import streamlit as st
from api import is_token_expired

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

token = st.session_state["access_token"]

st.title("Amazshop")


if token and not is_token_expired(token):
    pages = [
        st.Page("pages/Home.py", title="Home"),
        st.Page("pages/Order.py",title = "Order"),
        st.Page("pages/Favorite items.py",title="Favorite items"),
        st.Page("pages/Chat assistant.py", title="Chat assistant"),
        st.Page("pages/Logout.py",title = "Logout")
    ]
else:
    pages = [
        st.Page("pages/Home.py",title="home"),
        st.Page("pages/Register.py",title = "Register"),
        st.Page("pages/Login.py", title="Login")
    ]

pg = st.navigation(pages)
pg.run()
