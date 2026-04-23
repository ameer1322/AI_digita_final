import streamlit as st


from api import logout


if st.button("Logout"):
    logout()
