import streamlit as st

if 'check_registered' not in st.session_state:
    st.session_state['check_registered'] = False


st.title ("Register")

with st.form("register"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First name")
    with col2:
        last_name = st.text_input("Last name")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    st.form_submit_button("Register")

# with st.sidebar:
#     col1, _, col3 = st.columns([1, 0.5, 1])
#     with col1:
#         if st.button("Login"):
#             st.title("check")
#     with col3:
#         if st.button("Logout"):
#             st.session_state['jwt_token'] = None
#             st.sidebar.success("Logged out successfully!")
