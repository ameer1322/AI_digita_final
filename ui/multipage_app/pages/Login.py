import streamlit as st


from api import login_user


st.title("Login")

with st.form("Login"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        response = login_user(username, password)

        if response.status_code == 200:
            st.success("Logged in successfully")
        else:
            try:
                error_details= response.json().get("detail")
                st.error(error_details)
            except Exception:

                st.error(f"{response.status_code}:{response.text}")