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

# # Initialize session state
# if "current_user" not in st.session_state:
#     st.session_state.current_user = None
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # Only show login page if not logged in
# if not st.session_state.logged_in:
#     with login_page.container():
#         st.header("Welcome to Carelog!")
#         st.subheader("Login")

#         user_name = st.text_input("Enter your user ID:")

#         if user_name:
#             current_user = app.utils.load_user(user_name)
#             if current_user is not None:
#                 password = st.text_input("Enter your password:", type="password")

#                 if password:
#                     if password == current_user.password:
#                         # Save login state and current user in session
#                         st.session_state.current_user = current_user
#                         st.session_state.logged_in = True
#                     else:
#                         st.error("Incorrect password")
#             else:
#                 st.warning("User ID does not exist")

# # If logged in, show the dashboard based on user_id
# if st.session_state.logged_in:
#     login_page.empty()  # clear login page
#     with dashboard_page.container():
#         if st.session_state.current_user.user_id == "cs001":
#             gui.carestaff_dashboard.test_launch()
#         else:
#             st.write(f"Dashboard for {st.session_state.current_user.name} (user_id: {st.session_state.current_user.user_id}) not implemented yet")

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Only show login page if not logged in
if not st.session_state.logged_in:
    with login_page.container():
        st.header("Welcome to Carelog!")
        st.subheader("Login")

        user_name = st.text_input("Enter your user ID:")

        if user_name:
            current_user = app.utils.load_user(user_name)
            if current_user is not None:
                password = st.text_input("Enter your password:", type="password")

                if password:
                    if password == current_user.password:
                        # Save login state and current user in session
                        st.session_state.current_user = current_user
                        st.session_state.logged_in = True
                    else:
                        st.error("Incorrect password")
            else:
                st.warning("User ID does not exist")

# If logged in, show the dashboard based on role
if st.session_state.logged_in:
    login_page.empty()  # clear login page
    with dashboard_page.container():
        if st.session_state.current_user.role == "CareStaff":
            gui.carestaff_dashboard.test_launch()
        else:
            st.write(
                f"Dashboard for {st.session_state.current_user.name} "
                f"(role: {st.session_state.current_user.role}) not implemented yet"
            )