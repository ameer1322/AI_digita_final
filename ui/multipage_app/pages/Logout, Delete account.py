import streamlit as st


from api import logout, delete_account


if st.button("Logout"):
    logout()
if "delete_check" not in st.session_state:
    st.session_state["delete_check"] = False

if st.button("Delete account"):
    st.session_state["delete_check"] = True

if st.session_state["delete_check"]:
    st.write("Are you sure?")
    if st.button("Yes!"):
        delete_account()
        logout()
        st.session_state["delete_check"] = False
        st.rerun()
    if st.button("No!"):
        st.session_state["delete_check"] = False
        st.rerun()


