import json
import app
import streamlit as st

def launch_patient_dashboard():
    current_user = st.session_state.current_user

    st.header(f"{current_user.role} Dashboard")
    st.write("Dashboard successfully loaded")
    st.write(f"Hello {current_user.name}, welcome to the {current_user.role} Dashboard")

    # Fill this in with dashboard features and functions
    
    patient_for_view = current_user.user_id
   
    if patient_for_view:
        current_patient = app.utils.load_patient(patient_for_view, "data/patient_data.json")

        if current_patient is not None:
            st.write(f"Viewing data for patient: {current_patient.name}")
            st.write(f"Symptoms: {current_patient.symptoms}")
            st.write(f"Preferences: {current_patient.preferences}")
            
            with st.expander(f"Logs for {current_patient.name}", expanded=False):
                for log in current_patient.logs:
                    for log_title, log_content in log.items():
                        with st.expander(log_title, expanded=False):
                            st.write(log_content)




    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()