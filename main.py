import streamlit as st


class CareLog:
    def __init__(self, patients_name, log, date_and_time):
        self.patients_name = patients_name
        self.log = log
        self.date_and_time = date_and_time


#just throwing in some of the main classes, we can move them accordingly once we've decided on a folder/file structure
class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

class Patient:
    def __init__(self, mrn): # what does mrn mean?(UML diagram)
        self.mrn = mrn

class CareStaff:
    def __init__(self, speciality):
        self.speciality = speciality




#____Main program start goes below here____

st.header("test header") # im testing to see if streamlit is important correctly can you guys check to see if this is showing on your end.

