import os
import streamlit as st
import requests

BACKEND_BASE_URL = os.getenv("BACKEND_URL")
API_URL = "http://backend:8000/run-query" 

st.set_page_config(page_title="Linux Agent Bot", page_icon="💻", layout="centered")

st.title("💻 Linux Agent Assistant")
st.markdown("Ask me to run tasks on your EC2 server!")

# Chat history stored in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your query here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend API
    try:
        response = requests.post(API_URL, json={"query": prompt})
        if response.status_code == 200:
            answer = response.json().get("answer", "No response")
        else:
            answer = f"Error: {response.text}"
    except Exception as e:
        answer = f"⚠️ Could not connect to backend: {e}"

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
