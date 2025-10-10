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

# current_user = app.utils.load_user("cs001")
# print(current_user)

app.utils.TestClass




#____Main program start goes below here____

login_page = st.empty()

dashboard_page = st.empty()

with login_page.container():
    st.header("Welcome to Carelog!") # im testing to see if streamlit is imported correctly can you guys check to see if this is showing on your end. works for me but i have path issues so it might be different - Aidan
    st.subheader("Login")

    option = st.selectbox('Choose a User type (this does nothing right now):', ['CareStaff', 'Patient', 'Clerk', 'Admin']) #choosing a user type and then showing a different dashboard for each type (get from other folders/modules). what do you guys think about this approach?
    st.write("You chose", option)

    user_name = st.text_input("Enter your user ID:")

    current_user = app.utils.load_user(user_name)

    if current_user is not None:
        password = st.text_input("Enter your password:")

    if password == current_user.password:
        login_page.empty()
        with dashboard_page.container():
            gui.carestaff_dashboard.test_launch()

    # if "current_user" not in st.session_state:
    #     st.session_state.current_user = app.utils.load_user(user_name)

    # password = st.text_input("Enter your password:")

    # if password == current_user.password:
    #     login_page.empty()  # clears everything
    #     with dashboard_page.container():
    #         gui.carestaff_dashboard.test_launch()

        



    if st.button("Access CareStaff dashboard (will add authentication later)"):
        login_page.empty()  # clears everything
        with dashboard_page.container():
            gui.carestaff_dashboard.test_launch() #testing to see if dashboard can be imported from gui and then launched from main.py