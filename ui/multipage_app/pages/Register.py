import streamlit as st
from api import register_user
import re

if 'check_registered' not in st.session_state:
    st.session_state['check_registered'] = False

NAME_REGEX = r"^[a-zA-Z\s\-']{2,50}$"

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

USERNAME_REGEX = r"^[a-zA-Z0-9_\-]{3,20}$"

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

PHONE_REGEX = r"^\+?[0-9]{7,15}$"

ADDRESS_REGEX = r"^[a-zA-Z0-9\s,.\-/#]{5,100}$"


st.title ("Register")

with st.form("register"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First name")
    with col2:
        last_name = st.text_input("Last name")
    age = st.number_input("Age",0,99)
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Register")

    if submitted:
        errors = []
        if not re.match(NAME_REGEX, first_name):
            errors.append("Invalid first name")
        if not re.match(NAME_REGEX, last_name):
            errors.append("Invalid last name")
        if not re.match(EMAIL_REGEX, email):
            errors.append("Invalid email")
        if not re.match(USERNAME_REGEX, username):
            errors.append("Invalid username (3-20 chars, letters/numbers/_/-)")
        if not re.match(PASSWORD_REGEX, password):
            errors.append("Password must be 8+ chars with uppercase, lowercase, number and special char (@$!%*?&)")
        if not re.match(PHONE_REGEX, phone):
            errors.append("Invalid phone number")
        if not re.match(ADDRESS_REGEX,address):
            errors.append("Invalid address (5-100 chars, e.g. '123 Main St, Apt #3')")
        if errors:
            for error in errors:
                st.error(error)
        else:
            result = register_user(first_name, last_name, age, email, phone, address,username, password)
            st.session_state['check_registered'] = True
            st.success("Registered successfully!")

# with st.sidebar:
#     col1, _, col3 = st.columns([1, 0.5, 1])
#     with col1:
#         if st.button("Login"):
#             st.title("check")
#     with col3:
#         if st.button("Logout"):
#             st.session_state['jwt_token'] = None
#             st.sidebar.success("Logged out successfully!")
