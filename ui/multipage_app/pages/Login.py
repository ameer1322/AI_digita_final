import streamlit as st


from api import login_user


st.title("Login")

with st.form("Login"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        result = login_user(username, password)
