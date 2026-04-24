from statistics import quantiles

import streamlit as st
from api import get_all_items
import pandas as pd

with st.form("search_function"):
    searched_products = st.text_input("Search Amazshop")
    submit_btn = st.form_submit_button("Search")


st.divider()

st.write("Available items")

# @st.cache_data
def fetch_items():
    response = get_all_items()
    if response.status_code==200:
        items = response.json()
        return pd.DataFrame(items, columns=["name","price", "quantity"])
    return None

df = fetch_items()
if df is not None:
    st.dataframe(df, use_container_width=True)
else:
    st.error("Failed to fetch items")