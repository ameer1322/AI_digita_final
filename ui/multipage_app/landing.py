import streamlit as st


if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

st.title("Amazshop")


if st.session_state["access_token"]:
    pages = [
        st.Page("pages/Home.py", title="Home"),
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


