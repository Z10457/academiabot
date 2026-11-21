import streamlit as st

if "count" not in st.session_state:
    st.session_state["count"] = 0

if st.button("Add one"):
    st.session_state["count"] += 1

st.write(st.session_state["count"])