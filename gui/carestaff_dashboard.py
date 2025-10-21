import json
import app
import streamlit as st

import os
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

def launch_carestaff_dashboard():
    current_user = st.session_state.current_user

    st.header(f"{current_user.role} Dashboard")
    st.write("Dashboard successfully loaded")
    st.write(f"Hello {current_user.name}, welcome to the {current_user.role} Dashboard")

    # Fill this in with dashboard features and functions
    # --- Nurse Call Alerts ---
    st.subheader("Nurse Call Alerts")

    colA, colB, colC = st.columns([1, 1, 2])
    with colA:
        if st.button("Refresh"):
            st.rerun()
    with colB:
        show = st.selectbox("Show", ["All", "Open", "Acknowledged", "Resolved"], index=1)
    with colC:
        st.caption("Use Acknowledge/Resolve to manage alerts.")

    status_filter = None if show.lower() == "all" else show.lower()
    alerts = app.utils.list_alerts(status=status_filter)

    if not alerts:
        st.info("No alerts to display.")
    else:
        for a in alerts:
            kind = a.get("kind", "")
            if kind == "staff_alert":
                title = f"Staff Alert — Room {a.get('room','-')}"
                subtitle = f"From: {a.get('raised_by_name','')} ({a.get('raised_by_id','')})"
            else:
                # default: nurse_call (old alerts may not have 'kind')
                title = a.get("patient_name", "Unknown")
                subtitle = f"ID: `{a.get('patient_id','?')}`"

            top = st.columns([3, 2, 2, 2, 3])
            top[0].markdown(f"**{title}**  \n{subtitle}")
            top[1].markdown(f"**Status:** {a.get('status','?').title()}")
            top[2].markdown(f"**Priority:** {a.get('priority','normal').title()}")
            top[3].markdown(f"**Time (UTC):** {a.get('timestamp','')[:19]}")
            top[4].markdown(f"**Room:** {a.get('room','-') or '-'}")
            with st.container(border=True):
                top = st.columns([3, 2, 2, 2, 2])
                top[0].markdown(f"**{a.get('patient_name','Unknown')}**  \nID: `{a.get('patient_id','?')}`")
                top[1].markdown(f"**Status:** {a.get('status','?').title()}")
                top[2].markdown(f"**Priority:** {a.get('priority','normal').title()}")
                top[3].markdown(f"**Time (UTC):** {a.get('timestamp','')[:19]}")
                top[4].markdown(f"**Room:** {a.get('room','-') or '-'}")

                c1, c2, _ = st.columns([1, 1, 6])
                ack_key = f"ack_{a['id']}"
                res_key = f"res_{a['id']}"

                if a.get("status") == "open":
                    if c1.button("Acknowledge", key=ack_key):
                        app.utils.acknowledge_alert(a["id"],
                            staff_id=str(getattr(current_user, "user_id", "")),
                            staff_name=getattr(current_user, "name", ""))
                        st.rerun()
                else:
                    c1.button("Acknowledge", key=ack_key, disabled=True)

                if a.get("status") in ("open", "acknowledged"):
                    if c2.button("Resolve", key=res_key):
                        app.utils.resolve_alert(a["id"],
                            staff_id=str(getattr(current_user, "user_id", "")),
                            staff_name=getattr(current_user, "name", ""))
                        st.rerun()
                else:
                    c2.button("Resolve", key=res_key, disabled=True)

                if a.get("status") == "acknowledged":
                    st.caption(f"Acknowledged by {a.get('ack_by','')} at {a.get('ack_time','')[:19]} UTC")
                if a.get("status") == "resolved":
                    st.caption(f"Resolved by {a.get('resolved_by','')} at {a.get('resolved_time','')[:19]} UTC")


    # --- Risk Scanner ---
    st.divider()
    st.subheader("Risk Scanner")

    if "show_risk_scanner" not in st.session_state:
        st.session_state.show_risk_scanner = False

    if st.button("Open risk scanner"):
        st.session_state.show_risk_scanner = True

    if st.session_state.show_risk_scanner:
        st.info("Select a patient to scan their logs for at-risk keywords.")
        patients = app.utils.list_patients("data/patient_data.json")

        if not patients:
            st.warning("No patients found in data/patient_data.json")
        else:
            show_cols = ["user_id", "name"]
            header_map = {"user_id": "ID", "name": "Name"}
            st.dataframe(
                [{header_map[k]: p.get(k, "") for k in show_cols} for p in patients],
                hide_index=True, use_container_width=True, height=240
            )

            selected_patient = st.selectbox(
                "Choose patient",
                patients,
                format_func=lambda p: f"{p.get('name','Unknown')} ({p.get('user_id','?')})"
            )

            # ⬇️ Full-width placeholder for results
            results_area = st.container()

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("Scan selected patient"):
                    pid = selected_patient.get("user_id")
                    rec = app.utils.get_patient_risk(pid)
                    with results_area:  # <-- render outside columns, full width
                        if not rec or rec.get("score", 0) == 0:
                            st.success("No concerning keywords found for this patient.")
                        else:
                            st.warning(f"Risk: {rec['risk_level'].upper()} • Score: {rec['score']}")
                            counts_rows = [{"Category": k, "Count": v}
                                        for k, v in rec["category_counts"].items() if v]
                            if counts_rows:
                                # use_container_width makes it stretch
                                st.dataframe(counts_rows, hide_index=True, use_container_width=True)

                            if rec.get("hits"):
                                st.write("Matched snippets:")
                                st.dataframe(
                                    [{"Category": h["category"], "Phrase": h["phrase"], "Snippet": h["snippet"]}
                                    for h in rec["hits"]],
                                    hide_index=True, use_container_width=True, height=300
                                )

            with col2:
                if st.button("Scan all patients"):
                    results = app.utils.at_risk_patients()
                    with results_area:  # <-- full width
                        if not results:
                            st.info("No hits across all patients.")
                        else:
                            # build columns dynamically
                            all_cats = sorted({c for r in results for c in r["category_counts"].keys()})
                            overview = []
                            for r in results:
                                row = {"Patient ID": r["patient_id"], "Risk": r["risk_level"], "Score": r["score"]}
                                for cat in all_cats:
                                    row[cat] = r["category_counts"].get(cat, 0)
                                overview.append(row)
                            st.dataframe(overview, hide_index=True, use_container_width=True, height=350)

            with col3:
                if st.button("Close scanner"):
                    st.session_state.show_risk_scanner = False



    # Lets the user view data and logs for a Patient of their choice
    st.subheader("View Patient Data")

    patient_for_view = st.text_input("Enter Patient user ID")
   
    if patient_for_view:
        current_patient = app.utils.load_patient(patient_for_view, "data/patient_data.json")

        if current_patient is not None:
            st.write(f"Viewing data for patient: {current_patient.name}")
            st.write(f"Symptoms: {current_patient.symptoms}")
            st.write(f"Preferences: {current_patient.preferences}")
            st.write(f"Staff Notes: {current_patient.personal_notes}")
            
            # --- Logs viewer (safe for dict | list | str) ---
            with st.expander(f"Logs for {current_patient.name}", expanded=False):
                logs = getattr(current_patient, "logs", [])  # falls back to []
                if not logs:
                    st.info("No logs found for this patient.")
                else:
                    for idx, log in enumerate(logs, start=1):

                        # Case A: each log is a dict
                        if isinstance(log, dict):
                            # Prefer {"title": "...", "content": ...} if present
                            if {"title", "content"} <= set(log.keys()):
                                title = str(log.get("title") or f"Log {idx}")
                                with st.expander(title, expanded=False):
                                    content = log.get("content")
                                    if isinstance(content, (dict, list)):
                                        st.json(content)
                                    else:
                                        st.write(content)
                            else:
                                # Generic dict: show each key/value under its own expander
                                for k, v in log.items():
                                    with st.expander(str(k), expanded=False):
                                        if isinstance(v, (dict, list)):
                                            st.json(v)
                                        else:
                                            st.write(v)

                        # Case B: each log is a list
                        elif isinstance(log, list):
                            with st.expander(f"Log {idx}", expanded=False):
                                for j, item in enumerate(log, start=1):
                                    if isinstance(item, (dict, list)):
                                        st.markdown(f"**Item {j}**")
                                        st.json(item)
                                    else:
                                        st.write(f"- {item}")

                        # Case C: plain string/number/etc.
                        else:
                            with st.expander(f"Log {idx}", expanded=False):
                                st.write(str(log))


        else:
            st.warning("No patient data for user ID")
    

        # ---------- Staff Alert (call staff to a room) ----------
    st.subheader("Staff Alert")

    with st.form("staff_alert_form", clear_on_submit=True):
        # Room to respond to
        colr1, colr2 = st.columns([2, 1])
        room = colr1.text_input("Room", placeholder="e.g., 3B / 205 / Resus")
        priority = colr2.selectbox("Priority", ["urgent", "normal"], index=0)

        # Try to load staff roster (optional file: data/staff_data.json)
        roster = app.utils.list_staff()
        on_duty = [s for s in roster if str(s.get("on_duty", True)).lower() in ("true", "1", "yes")]
        choices = on_duty or roster  # fall back to everyone if on_duty missing/falsey

        selected_staff = []
        if choices:
            # Display nice labels like "Alice (RN-123)"
            def label(s):
                uid = s.get("user_id") or s.get("id") or "?"
                role = s.get("role") or ""
                name = s.get("name") or "Unknown"
                return f"{name} ({role}) — {uid}" if role else f"{name} — {uid}"

            selected = st.multiselect(
                "Notify specific on-duty staff (leave empty to alert all on-duty)",
                choices,
                format_func=label
            )
            selected_staff = [str(s.get("user_id") or s.get("id") or "") for s in selected if (s.get("user_id") or s.get("id"))]
        else:
            st.caption("No staff roster file found (data/staff_data.json). "
                    "You can still send a broadcast to all on-duty staff.")
            selected_raw = st.text_input("Target staff IDs (optional, comma-separated)", placeholder="e.g., 101, 204, 309")
            if selected_raw.strip():
                selected_staff = [x.strip() for x in selected_raw.split(",") if x.strip()]

        message = st.text_area("Message (optional)", placeholder="Brief context, e.g., 'assist with lift'")

        send = st.form_submit_button("Send Staff Alert")
        if send:
            if not room.strip():
                st.error("Please enter a room.")
            else:
                alert = app.utils.create_staff_alert(
                    raised_by_id=str(getattr(current_user, "user_id", "")),
                    raised_by_name=str(getattr(current_user, "name", "")),
                    room=room.strip(),
                    message=message.strip(),
                    priority=priority,
                    target_staff_ids=selected_staff or None
                )
                st.success(f"Alert sent to staff for Room {room}.")
                with st.expander("Alert details"):
                    st.json(alert)  

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
    
    
    #Updates Symptoms notes 
    st.subheader("Update patient symptoms.")
    pid_symptoms = st.text_input("Please enter the patient ID.",key = "pid_symptoms")
    psymptoms = st.text_input("Please enter the patient symptoms.")
    if st.button("Update symptoms"):
        symptoms_success = app.utils.update_patient_symptoms(pid_symptoms,psymptoms)

        if symptoms_success:
            st.success("Symptoms successfully Updated.")
        else:
            st.error("Invalid user ID.")

    #Update personal notes
    st.subheader("New Patient Note?")
    pid_note = st.text_input("Please enter the patient ID.", key = "pid_note")
    pnote = st.text_input("What are they feeling today?", key = "pnote")  
    if st.button("Submit new note"):
        note_success = app.utils.update_patient_personal_note(pid_note,pnote)
        if note_success:
            st.success("Note successfully added")
        else:
            st.error("Invalid user ID.")


    
    # Quit function to return to login page. Leave this at the bottom
    if st.button("Quit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
        st.rerun()
