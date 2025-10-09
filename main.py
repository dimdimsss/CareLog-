import streamlit as st
import json #might not be necessary but just in case

#so we can use stuff from them (folder.file.function/class)
import app 
import gui

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

st.header("Welcome to Carelog!") # im testing to see if streamlit is imported correctly can you guys check to see if this is showing on your end. works for me but i have path issues so it might be different - Aidan
st.subheader("Login")

#choosing a user type and then showing a different dashboard for each type (get from other folders/modules). what do you guys think about this approach?
option = st.selectbox(
    'Choose a User type:',
    ['CareStaff', 'Patient', 'Clerk', 'Admin']
)