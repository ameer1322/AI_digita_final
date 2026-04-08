import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

st.title("Amazshop")


if st.session_state.logged_in:
    pages = [
        st.Page("pages/Chat assistant.py", title="Chat assistant"),
        st.Page("pages/Favorite items.py",title="Favorite items"),
        st.Page("pages/Orders.py",title = "orders")
    ]
else:
    pages = [
        st.Page("pages/Home.py",title="home"),
        st.Page("pages/Register.py",title = "Register"),
        st.Page("pages/Login.py", title="Login")
    ]

pg = st.navigation(pages)
pg.run()


