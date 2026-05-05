import pandas as pd
import streamlit as st

from api import get_user_favorites, handle_favorites



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
    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        st.write("Product name")
    with col2:
        st.write("Price")

    for _, row in st.session_state["favorites"].iterrows():
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            st.write(row["name"])
        with col2:
            st.write(f'{row["price"]}$')
        with col3:
            if st.button("Remove from favorites", key=f"remove {row['product_id']}"):
                handle_favorites(row["name"])
                fetch_favorites.clear()
                st.rerun()
else:
    st.subheader("No items in favorites")

