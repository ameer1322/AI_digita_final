import streamlit as st
import httpx
from api import BASE_URL

st.title("Shopping Assistant")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "prompt_count" not in st.session_state:
    st.session_state["prompt_count"] = 0

if st.button("Restart session"):
    st.session_state["chat_history"] = []
    st.session_state["prompt_count"] = 0
    st.rerun()

for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
print(st.session_state["prompt_count"])
if st.session_state["prompt_count"]< 5:
    if prompt := st.chat_input("Ask me anything about our products..."):
        with st.chat_message("user"):
            st.write(prompt)

        response = httpx.post(
            f"{BASE_URL}/chat/",
            json={"message": prompt, "history": st.session_state["chat_history"]},
            timeout=30.0
        )

        if response.status_code == 200:
            reply = response.json()["response"]
            with st.chat_message("assistant"):
                st.write(reply)
            st.session_state["chat_history"].append({"role": "user", "content": prompt})
            st.session_state["chat_history"].append({"role": "assistant", "content": reply})
            st.session_state["prompt_count"] += 1
            st.rerun()
        else:
            st.error("Something went wrong, please try again.")
else:
    st.write("Out of prompts for this session, please start a new session!")