import pandas as pd
import streamlit as st

from api import get_user_orders, remove_from_order

@st.cache_data(ttl=60)
def fetch_orders():
    response = get_user_orders()
    if response.status_code==200:
        items = response.json()
        return items
    return None

st.session_state["orders"] = pd.DataFrame(fetch_orders())

if not st.session_state["orders"].empty:
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.write("Product")
    with col2:
        st.write("Quantity")
    with col3:
        st.write("Total price")

    for _, row in st.session_state["orders"].iterrows():

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
                fetch_orders.clear()
                st.rerun()
else:
    st.subheader("No order yet!")

st.divider()
st.subheader("Past orders")

