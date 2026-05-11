import pandas as pd
import streamlit as st

from api import get_user_favorites, add_to_cart, handle_favorites



@st.cache_data(ttl=60)
def fetch_favorites():
    response = get_user_favorites()
    if response.status_code==200:
        items = response.json()
        return items
    return None

if st.session_state.get("refresh_favorites"):
    st.session_state["refresh_favorites"] = False
    fetch_favorites.clear()

st.session_state["favorites"] = pd.DataFrame(fetch_favorites())

if not st.session_state["favorites"].empty:
    col1,col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,1])
    with col1:
        st.write("Product name")
    with col2:
        st.write("Price")
    with col6:
        st.write("inventory")

    for _, row in st.session_state["favorites"].iterrows():
        col1,col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,1])
        with col1:
            st.write(row["name"])
        with col2:
            st.write(f'{row["price"]}$')
        with col3:
            if st.button("Remove from favorites", key=f"remove {row['product_id']}"):
                handle_favorites(row["name"])
                fetch_favorites.clear()
                st.rerun()
        with col4:
            order_quantity= st.number_input(
            "Amount", min_value=1, value=1, step=1,
                key=f"qty_{row['name']}"
            )
        with col5:
            if st.button("Order", key=f"order_{row['name']}"):
                if row["inventory"]<order_quantity:
                    st.error("Not enough products in inventory!")
                else:
                    response = add_to_cart(row["name"],order_quantity)
                    if response.status_code == 201:
                        st.success(f"Ordered {row['name']}!")
                        st.session_state["refresh_orders"] = True
                    elif response.status_code == 400:
                        st.error(response.json()["detail"])
        with col6:
            st.write(str(row["inventory"]))
else:
    st.subheader("No items in favorites")

