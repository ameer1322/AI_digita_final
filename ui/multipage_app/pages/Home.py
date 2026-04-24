import streamlit as st
from api import get_all_products, get_items_by_name
import pandas as pd
from sqlalchemy.orm import sessionmaker

if "items" not in st.session_state:
    st.session_state["items"] = None
if "refresh_items" not in st.session_state:
    st.session_state["refresh_items"] = False


with st.form("search_function"):
    searched_text = st.text_input("Search Amazshop")
    submit_btn = st.form_submit_button("Search")

    if submit_btn:
        if searched_text != "":
            searched_items = []
            searched_items.append(get_items_by_name(searched_text).json())

            if searched_items[0] is not None:
                items_df = pd.DataFrame(searched_items,columns=["name","price","quantity"])
                st.session_state["items"] = items_df
                st.session_state["refresh_items"] = True
            else:
                st.error("Items not found")
st.divider()

st.write("Available items")

def fetch_items():
    response = get_all_products()
    if response.status_code==200:
        items = response.json()
        return pd.DataFrame(items, columns=["name","price", "quantity"])
    return None

if not st.session_state["refresh_items"]:
    st.session_state["items"] = fetch_items()

if st.session_state["items"] is not None:
    st.dataframe(st.session_state["items"], width='stretch')
else:
    st.error("Failed to fetch items")

if st.button("toggle"):
    # st.session_state["items"] = pd.DataFrame()
    st.session_state["refresh_items"] = not st.session_state["refresh_items"]
    st.rerun()
st.write(st.session_state["refresh_items"])