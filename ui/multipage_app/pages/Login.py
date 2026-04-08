import streamlit as st

st.title("Login")

with st.form("Login"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    st.form_submit_button("Login")