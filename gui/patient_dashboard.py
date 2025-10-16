import json
import app
import streamlit as st

def launch_patient_dashboard():
    current_user = st.session_state.current_user

    st.header(f"{current_user.role} Dashboard")
    st.write("Dashboard successfully loaded")
    st.write(f"Hello {current_user.name}, welcome to the {current_user.role} Dashboard")

    # ----- Patient's own data -----
    st.subheader(f"Data for {current_user.name}")

    patient_for_view = current_user.user_id
    if patient_for_view:
        current_patient = app.utils.load_patient(patient_for_view, "data/patient_data.json")

        if current_patient is not None:
            st.write(f"Symptoms: {current_patient.symptoms}")
            st.write(f"Preferences: {current_patient.preferences}")

            # SAFE logs viewer (handles dict | list | str)
            with st.expander(f"Logs for {current_patient.name}", expanded=False):
                logs = getattr(current_patient, "logs", [])
                if not logs:
                    st.info("No logs found for this patient.")
                else:
                    for idx, log in enumerate(logs, start=1):
                        if isinstance(log, dict):
                            # Prefer {'title':..., 'content':...} shape if present
                            if {"title", "content"} <= set(log.keys()):
                                title = str(log.get("title") or f"Log {idx}")
                                with st.expander(title, expanded=False):
                                    content = log.get("content")
                                    if isinstance(content, (dict, list)):
                                        st.json(content)
                                    else:
                                        st.write(content)
                            else:
                                for k, v in log.items():
                                    with st.expander(str(k), expanded=False):
                                        if isinstance(v, (dict, list)):
                                            st.json(v)
                                        else:
                                            st.write(v)
                        elif isinstance(log, list):
                            with st.expander(f"Log {idx}", expanded=False):
                                for j, item in enumerate(log, start=1):
                                    if isinstance(item, (dict, list)):
                                        st.markdown(f"**Item {j}**")
                                        st.json(item)
                                    else:
                                        st.write(f"- {item}")
                        else:
                            with st.expander(f"Log {idx}", expanded=False):
                                st.write(str(log))

    # ---------- Nurse Call button ----------
    st.subheader("Need assistance?")
    if st.button("Call Nurse / Request Help", type="primary", use_container_width=True):
        pid = str(getattr(current_user, "user_id", getattr(current_user, "id", "")))
        pname = str(getattr(current_user, "name", "Unknown Patient"))
        # FIX: call through app.utils (you did not import `utils` directly)
        alert = app.utils.create_help_alert(patient_id=pid, patient_name=pname)
        st.success("Nurse has been alerted. Please stay where you are — help is on the way.")
        with st.expander("Alert details"):
            st.json(alert)




    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()
