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

            with st.expander(f"Staff notes for {current_patient.name}", expanded=False):
                for note in current_patient.personal_notes:
                    for note_title, note_content in note.items():
                        with st.expander(note_title, expanded=False):
                            st.write(note_content)
            
            with st.expander(f"Logs from {current_patient.name}", expanded=False):
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


    # Add new staff member
    st.subheader("Create new staff member")

    with st.form("create_staff_form", clear_on_submit=True):
        staff_id = st.text_input("Staff user ID", placeholder="e.g., c002")
        staff_name = st.text_input("Full name")
        staff_password = st.text_input("Password", value="carestaff")
        staff_role = st.selectbox("Role", ["CareStaff", "Admin"])
        create_staff = st.form_submit_button("Create staff")

        if create_staff:
            if not staff_id.strip() or not staff_name.strip():
                st.error("Please provide at least user ID and name.")
            else:
                try:
                    new_staff = app.utils.add_staff(
                        user_id=staff_id.strip(),
                        password=staff_password,
                        name=staff_name.strip(),
                        role=staff_role,
                        users_path="users.json" 
                    )
                    st.success(f"Created {new_staff['role']} {new_staff['name']} ({new_staff['user_id']})")
                    with st.expander("Created record"):
                        st.json(new_staff)
                except Exception as e:
                    st.error(str(e))



    
    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()
