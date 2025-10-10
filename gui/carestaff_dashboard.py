import json
import app
import streamlit as st

def launch_carestaff_dashboard():
    current_user = st.session_state.current_user

    st.header(f"{current_user.role} Dashboard")
    st.write("Dashboard successfully loaded")
    st.write(f"Hello {current_user.name}, welcome to the {current_user.role} Dashboard")



    if st.button("Quit"):
        st.rerun()