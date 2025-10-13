import json
import app
import streamlit as st

def launch_admin_dashboard():
    current_user = st.session_state.current_user

    st.header(f"{current_user.role} Dashboard")
    st.write("Dashboard successfully loaded")
    st.write(f"Hello {current_user.name}, welcome to the {current_user.role} Dashboard")

    # Fill this in with dashboard features and functions

    # Lets the user view a Patient log of their choice
    st.subheader("View Patient Logs")
    patient_for_view = st.text_input("Enter Patient user ID")

    if patient_for_view:
        loaded_log = app.utils.get_patient_logs(patient_for_view, "data/patient_data.json")

        if loaded_log:
            #st.write(loaded_log)
            with st.expander("Logs for", app.utils.get_patient_name(patient_for_view, "data/patient_data.json")): 
                st.write(loaded_log)

        else:
            st.warning("No patient data for user ID")



    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()