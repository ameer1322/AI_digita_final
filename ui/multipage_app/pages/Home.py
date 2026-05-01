import streamlit as st
from api import get_all_products, get_products_by_name, add_to_cart,is_token_expired, add_to_favorites
import pandas as pd




if "products_df" not in st.session_state:
    st.session_state["products_df"] = None

if "refresh_items" not in st.session_state:
    st.session_state["refresh_items"] = False

token = st.session_state["access_token"]


@st.cache_data(ttl=60)
def fetch_products():
    response = get_all_products()
    if response.status_code==200:
        items = response.json()
        return items
    return None

st.session_state["products"] = fetch_products()

if not st.session_state["refresh_items"]:
    st.session_state["products_df"] = pd.DataFrame(fetch_products(),columns=["name","price", "inventory"])

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
                    if product["inventory"] > value:
                        filtered_products.append(product)
            elif operator == "<":
                for product in st.session_state["products"]:
                    if product["inventory"] < value:
                        filtered_products.append(product)
            elif operator == "=":
                for product in st.session_state["products"]:
                    if product["inventory"] == value:
                        filtered_products.append(product)
        st.session_state["products_df"] = pd.DataFrame(filtered_products,columns=["name","price","inventory"])


def fetch_items_by_name_post_cache(searched_text:str):
    if searched_text != "":
        st.session_state["products"] = fetch_products_by_name(searched_text)
        st.session_state["products_df"] = pd.DataFrame(st.session_state["products"],columns=["name","price","inventory"])
        st.session_state["refresh_items"]=True
    else:
        st.session_state["products_df"] = pd.DataFrame(fetch_products(), columns=["name", "price", "inventory"])


with st.form("search_function"):
    searched_text = st.text_input("Search Amazshop")
    submit_btn = st.form_submit_button("Search")
    col1, col2, col3 = st.columns(3)
    with col1:
        field = st.selectbox("Field", ["price", "inventory"])
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
    st.session_state["products_df"]=pd.DataFrame(fetch_products(),columns=["name","price","inventory"])

if token and not is_token_expired(token):
    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 2, 2, 2])
    with col1:
        st.write("Product")
    with col2:
        st.write("Price")
    with col3:
        st.write("Inventory")
    for _, row in st.session_state["products_df"].iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3,2,1,2,2,2])

        with col1:
            st.write(row["name"])
        with col2:
            st.write(f"${row['price']}")
        with col3:
            st.write(str(row["inventory"]))
        with col4:
            order_quantity= st.number_input(
                "Amount", min_value=1, value=1, step=1,
                key=f"qty_{row['name']}"
            )
        with col5:
            if st.button("Order", key=f"order_{row['name']}"):
                response = add_to_cart(row["name"],order_quantity)
                if response.status_code == 201:
                    st.success(f"Ordered {row['name']}!")
                else:
                    st.error(f"Failed to order {row['name']}!")
        with col6:
            if st.button("Favorite", key = f"favorite_{row['name']}"):
                response = add_to_favorites(row['name'])
                if response.status_code == 200:
                    st.success(f"Order added to favorites")
                else:
                    st.error(f"Failed to add to favorites")
else:
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.write("Product")
    with col2:
        st.write("Price")
    with col3:
        st.write("Inventory")
    for _, row in st.session_state["products_df"].iterrows():

        col1,col2,col3 = st.columns([3,2,1])
        with col1:
            st.write(row["name"])
        with col2:
            st.write(f"${row['price']}")
        with col3:
            st.write(str(row["inventory"]))

