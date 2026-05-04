import streamlit as st

from api import get_user_favorites



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

favorites = fetch_favorites()



st.write(favorites)