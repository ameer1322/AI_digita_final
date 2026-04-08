import streamlit as st


with st.form("search_function"):
    searched_products = st.text_input("Search Amazshop")
    submit_btn = st.form_submit_button("Search")


st.divider()

st.write("Available items")
