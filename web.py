import os
import streamlit as st
from main import run_agent
from db import new_client
from main import run_agent, build_config  
from tools import make_tools  
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Academia Agent")

if "client" not in st.session_state:
    st.session_state["client"] = None

if "is_guest" not in st.session_state:
    st.session_state["is_guest"] = False

if "config" not in st.session_state:
    st.session_state["config"] = None

if st.session_state["client"] is None:
    email = st.text_input("Email: ")
    password = st.text_input("Password", type = "password")
    if st.button("Log in"):
        client = new_client()
        try:
            client.auth.sign_in_with_password({"email": email, "password":password})
        except Exception:
            st.error("Login failed. Incorrect email or password. ")
        else:
            st.session_state["client"] = client #saves the client for whatever acc he is, keeps him logged in.
            st.rerun()
    if st.button("Continue as guest (YOUR INFO WONT BE SAVED) "): 
        client = new_client()
        try:
            client.auth.sign_in_anonymously()
        except Exception:
            st.error("Try again later.")
        else:
            st.session_state["client"] = client 
            st.session_state["is_guest"] = True
            st.rerun()
    st.stop()

if st.session_state["config"] is None:
    st.session_state["config"] = build_config(make_tools(st.session_state["client"]))

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
    reply = run_agent(st.session_state.messages, st.session_state["config"])
    st.session_state.messages.append({"role": "model", "parts": [{"text":reply }]})
    st.rerun()
        

