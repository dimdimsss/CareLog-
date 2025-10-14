import json
import app
import streamlit as st

def launch_admin_dashboard():
    current_user = st.session_state.current_user

    st.header(f"{current_user.role} Dashboard")
    st.write("Dashboard successfully loaded")
    st.write(f"Hello {current_user.name}, welcome to the {current_user.role} Dashboard")

    # Fill this in with dashboard features and functions

    # Lets the user view data and logs for a Patient of their choice
    st.subheader("View Patient Data")
    
    patient_for_view = st.text_input("Enter Patient user ID")
    current_patient = app.utils.load_patient(patient_for_view, "data/patient_data.json")


    if patient_for_view:
        #loaded_log = current_patient.logs

        #if loaded_log:

        st.write(f"Viewing data for patient: {current_patient.name}")
        st.write(f"Symptoms: {current_patient.symptoms}")
        st.write(f"Preferences: {current_patient.preferences}")

        with st.expander(f"Logs for {current_patient.name}"):
            st.write(current_patient.logs)

    else:
        st.warning("No patient data for user ID")
    



    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()