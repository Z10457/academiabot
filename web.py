import os
import streamlit as st
from main import run_agent

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Academia Agent")

if "messages" not in st.session_state :
    st.session_state.messages = []
if "last_upload" not in st.session_state : 
    st.session_state.last_upload = None

uploaded = st.sidebar.file_uploader("Upload the syllabus", type =["pdf", "docx"])

for m in st.session_state.messages:
    role = "assistant" if m["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(m["parts"][0]["text"])

prompt = st.chat_input("What may I help you with today")
if prompt:
    if uploaded and uploaded.name != st.session_state.last_upload:
        path = os.path.join(UPLOAD_DIR, os.path.basename(uploaded.name))
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.session_state.last_upload = uploaded.name
        prompt += f"\n(The user uploaded the syllabus saved at {path})"

    st.session_state.messages.append({"role": "user", "parts": [{"text":prompt }]})
    reply = run_agent(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": [{"text":reply }]})
    st.rerun()
        

