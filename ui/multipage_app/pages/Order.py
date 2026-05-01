import pandas as pd
import streamlit as st

from api import get_user_unconfirmed_order, get_user_confirmed_orders, remove_from_order, confirm_order



@st.cache_data(ttl=60)
def fetch_unconfirmed_order():
    response = get_user_unconfirmed_order()
    if response.status_code==200:
        items = response.json()
        return items
    return None

@st.cache_data(ttl=60)
def fetch_confirmed_orders():
    response = get_user_confirmed_orders()
    if response.status_code == 200:
        items = response.json()
        return items
    return None

if st.session_state.get("refresh_orders"):
    st.session_state["refresh_orders"] = False
    fetch_unconfirmed_order.clear()

st.session_state["unconfirmed_order"] = pd.DataFrame(fetch_unconfirmed_order())

st.session_state["confirmed_orders"] = pd.DataFrame(fetch_confirmed_orders())

if not st.session_state["unconfirmed_order"].empty:
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        st.write("Product")
    with col2:
        st.write("Quantity")
    with col3:
        st.write("Total price")

    for _, row in st.session_state["unconfirmed_order"].iterrows():

        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

        with col1:
            st.write(row["name"])
        with col2:
            st.write(str(row["quantity"]))
        with col3:
            st.write(str(row["price"]*row["quantity"])+"$")
        with col4:
            remove_quantity = st.number_input(
                "Amount", min_value=1, value=1, step=1, max_value=row["quantity"],
                key=f"qty_{row['name']}"
            )
        with col5:
            if st.button("Remove", key = f"remove {row['name']}"):
                response = remove_from_order(row["name"],remove_quantity)
                if response.status_code == 200:
                    st.success(f"Removed {row['name']}!")
                else:
                    st.error(f"Failed to Remove {row['name']}!")
                fetch_unconfirmed_order.clear()
                st.rerun()
    if st.button("Place order"):
        confirm_order()
        fetch_unconfirmed_order.clear()
        fetch_confirmed_orders.clear()
        st.rerun()
else:
    st.subheader("No order yet!")

st.divider()
st.subheader("Past orders")

if not st.session_state["confirmed_orders"].empty:

    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        st.write("Product")
    with col2:
        st.write("Quantity")
    with col3:
        st.write("Total price")
    prev_order_id = None
    for _, row in st.session_state["confirmed_orders"].iterrows():
        if prev_order_id is not None and row["order_id"] != prev_order_id:
            st.divider()

        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.write(row["name"])
        with col2:
            st.write(str(row["quantity"]))
        with col3:
            st.write(str(row["price"]*row["quantity"])+"$")

        prev_order_id=row["order_id"]