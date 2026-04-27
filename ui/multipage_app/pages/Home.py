import streamlit as st
from api import get_all_products, get_products_by_name
import pandas as pd
from sqlalchemy.orm import sessionmaker


if "products_df" not in st.session_state:
    st.session_state["products_df"] = None

if "refresh_items" not in st.session_state:
    st.session_state["refresh_items"] = False



@st.cache_data(ttl=60)
def fetch_products():
    response = get_all_products()
    if response.status_code==200:
        items = response.json()
        return items
    return None

st.session_state["products"] = fetch_products()

if not st.session_state["refresh_items"]:
    st.session_state["products_df"] = pd.DataFrame(fetch_products(),columns=["name","price", "quantity"])

@st.cache_data(ttl=60)
def fetch_products_by_name(searched_text:str):
    if searched_text != "":
        searched_items = get_products_by_name(searched_text).json()
        if searched_items:
            return searched_items
        return None

def filter_items_by_range(field,operator,value):
    filtered_products = []
    if st.session_state["products"] is not None:
        if field == "price":
            if operator == ">":
                for product in st.session_state["products"]:
                    if product["price"] > value:
                        filtered_products.append(product)
            elif operator == "<":
                for product in st.session_state["products"]:
                    if product["price"] < value:
                        filtered_products.append(product)
            elif operator == "=":
                for product in st.session_state["products"]:
                    if product["price"] == value:
                        filtered_products.append(product)

        else:
            if operator == ">":
                for product in st.session_state["products"]:
                    if product["quantity"] > value:
                        filtered_products.append(product)
            elif operator == "<":
                for product in st.session_state["products"]:
                    if product["quantity"] < value:
                        filtered_products.append(product)
            elif operator == "=":
                for product in st.session_state["products"]:
                    if product["quantity"] == value:
                        filtered_products.append(product)
        st.session_state["products_df"] = pd.DataFrame(filtered_products,columns=["name","price","quantity"])


def fetch_items_by_name_post_cache(searched_text:str):
    if searched_text != "":
        st.session_state["products"] = fetch_products_by_name(searched_text)
        st.session_state["products_df"] = pd.DataFrame(st.session_state["products"],columns=["name","price","quantity"])
        st.session_state["refresh_items"]=True
    else:
        st.session_state["products_df"] = pd.DataFrame(fetch_products(), columns=["name", "price", "quantity"])


with st.form("search_function"):
    searched_text = st.text_input("Search Amazshop")
    submit_btn = st.form_submit_button("Search")
    col1, col2, col3 = st.columns(3)
    with col1:
        field = st.selectbox("Field", ["price", "quantity"])
    with col2:
        operator = st.selectbox("Operator", [">", "<", "="])
    with col3:
        value = st.number_input("Value", min_value=0)


    fetch_items_by_name_post_cache(searched_text)

    filter_items_by_range(field, operator, value)


st.divider()

st.write("Available items")



if st.session_state["products_df"].empty:
    st.error("Products not found")
    st.session_state["products_df"]=pd.DataFrame(fetch_products(),columns=["name","price","quantity"])

st.write(st.session_state["products_df"])
