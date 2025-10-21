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

        else:
            st.warning("No patient data for user ID")
    

    # Add new patient
    st.subheader("Create new patient")

    with st.form("create_patient_form", clear_on_submit=True):
        new_id = st.text_input("Patient user ID", placeholder="e.g., p003")
        new_name = st.text_input("Full name")
        new_password = st.text_input("Password", value="patient")
        new_symptoms = st.text_input("Symptoms", "")
        new_prefs = st.text_input("Preferences", "")
        create = st.form_submit_button("Create patient")

        if create:
            if not new_id.strip() or not new_name.strip():
                st.error("Please provide at least user ID and name.")
            else:
                try:
                    res = app.utils.add_patient(
                        user_id=new_id.strip(),
                        password=new_password,
                        name=new_name.strip(),
                        symptoms=new_symptoms.strip(),
                        preferences=new_prefs.strip(),
                        users_path="users.json",
                        patient_path="patient_data.json"
                    )
                    st.success(f"Created patient {res['patient']['name']} ({res['patient']['user_id']})")
                    with st.expander("Created records"):
                        st.json(res)
                except Exception as e:
                    st.error(str(e))

    
        #Updates Patient logs
    st.subheader("New Patient Log?")
    pid = st.text_input("Please enter the patient ID.")
    plog = st.text_input("What are they feeling today?")  
    if st.button("next"):
        log_success = app.utils.submit_patient_log(pid,plog)
        if log_success:
            st.success("Log successfully added")

        else:
            st.error("Invalid user ID")


     #Updates patient preferences
    st.subheader("Update patient preferences")
    pid_pref = st.text_input("Please enter patient ID.")
    ppreference = st.text_input("Please enter the patient preferences.")
    if st.button("Update preferences"):
        preference_success = app.utils.update_patient_preferences(pid_pref,ppreference)

        if preference_success:
            st.success("Prefernce successfully added.")
        else:
            st.error("Invalid user ID.")


    #Updates Clinical notes 
    st.subheader("Update patient symptoms.")
    pid_pref = st.text_input("Please enter patient ID.")
    psymptoms = st.text_input("Please enter the patient symptoms.")
    if st.button("Update symptoms"):
        preference_success = app.utils.update_patient_symptoms(pid_pref,psymptoms)

        if preference_success:
            st.success("Symptoms successfully Updated.")
        else:
            st.error("Invalid user ID.")

    
    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()
