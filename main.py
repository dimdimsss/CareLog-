import streamlit as st
import json #might not be necessary but just in case

#so we can use stuff from them (folder.file.function/class)
import app 
import gui

class CareLog: # dims do we still need this here?
    def __init__(self, patients_name, log, date_and_time):
        self.patients_name = patients_name
        self.log = log
        self.date_and_time = date_and_time


#___testing things___
app.utils.testfunction() # testing imports

current_user = app.utils.load_user("cs001")
print(current_user)

app.utils.TestClass




#____Main program start goes below here____

login_page = st.empty()

login_page.header("Welcome to Carelog!") # im testing to see if streamlit is imported correctly can you guys check to see if this is showing on your end. works for me but i have path issues so it might be different - Aidan
login_page.subheader("Login")



#choosing a user type and then showing a different dashboard for each type (get from other folders/modules). what do you guys think about this approach?
option = login_page.selectbox(
    'Choose a User type (this does nothing right now):',
    ['CareStaff', 'Patient', 'Clerk', 'Admin']
)

login_page.write("you chose", option)
login_page.write("[streamlit and logic stuff happening and then respective dashboard loaded from gui]")

if login_page.button("access CareStaff dahsboard (will add authentication)"):
    login_page.empty()
    gui.carestaff_dashboard.test_launch() #testing to see if dashboard can be imported from gui and then launched from main.py