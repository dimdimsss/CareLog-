# Test file for functions and classes throughout the program
import pytest
import app

def test_test():
    test = "test"

    assert test == "test"

def test_load_user():
    user_object = app.utils.load_user("p001", "data/users.json")

    assert user_object.name == "Jacob Johnson"
    assert user_object.password == "patient"
    assert user_object.role == "Patient"



#------------- Load all patients tests --------------
def test_load_all_patients():#Tests to see if all data is loaded correctly, tests for 2 user to ensure that it's loading multiple users infomations
    patient_list = app.utils.load_all_patients()

    assert patient_list[0].user_id == "p001"
    assert patient_list[0].password == "patient"
    assert patient_list[0].name == "Jacob Johnson"
    assert patient_list[0].role == "Patient"

    assert patient_list[1].user_id == "p002"
    assert patient_list[1].password == "patient"
    assert patient_list[1].name == "Joe Jackson"
    assert patient_list[1].role == "Patient"


#------------- Submit Patient log tests --------------
def test1_submit_patient_log():#Postive test case (How the function is submitted through streamlit).
    outcome = app.utils.submit_patient_log("test","test log1")

    assert outcome == True
    
    user = app.utils.load_patient("test","data/patient_data.json") # Testing to make sure it was submitted

    assert user.logs[-1][f"Log {len(user.logs)}"] == "test log1"

def test2_submit_patient_log():#Negitive test case when patient forgets to submit log info.
    outcome = app.utils.submit_patient_log("test","")

    assert outcome == False

def test3_submit_patient_log():#If system malfunctions and no patient_id is recorded.
    outcome = app.utils.submit_patient_log("","test log1")

    assert outcome == False

def test4_submit_patient_log(): #If system malfunctions and patient ID dosent exist.
    outcome = app.utils.submit_patient_log("N/A","test log1")

    assert outcome == False


#------------- Submit Patient Preferences --------------
def test1_update_patient_preferences():#Postive test case (How the function is submitted through streamlit)
    outcome = app.utils.update_patient_preferences("test","test pref")

    assert outcome == True

    user = app.utils.load_patient("test","data/patient_data.json") #Testing to make sure preference is submitted correctly 
    preferences_list = [s.strip() for s in user.preferences.split(",")]

    assert preferences_list[-1] == "test pref"

def test2_update_patient_preferences():#Negitive test case when function is submiited with no entry
    outcome = app.utils.update_patient_preferences("test","")

    assert outcome == False 

def test3_update_patient_preferences():#Negitive test case when if system malfunctions and no user id is submitted
    outcome = app.utils.update_patient_preferences("","test pref")

    assert outcome == False

def test4_update_patient_preferences():#Negitive test case when the user id dosent exist
    outcome = app.utils.update_patient_preferences("N/A","test pref")

    assert outcome == False


#------------- Remove Patient Preferences --------------
def test1_remove_patient_preferences():#Postive test case (How the function is submitted through streamlit)
    app.utils.update_patient_preferences("test","remove pref")

    outcome = app.utils.remove_patient_preferences("test","remove pref")

    assert outcome == True

    user = app.utils.load_patient("test","data/patient_data.json") #Testing to make sure preference is removed correctly 
    preferences_list = [s.strip() for s in user.preferences.split(",")]

    assert "remove pref"  not in preferences_list

def test2_remove_patient_preferences():#Testing of no input
    outcome = app.utils.remove_patient_preferences("test","")

    assert outcome == False

def test3_remove_patient_preferences():#Testing for no user ID 
    outcome = app.utils.remove_patient_preferences("","remove pref")

    assert outcome == False

def test4_remove_patient_preferences():#Testing for invalid user ID
    app.utils.update_patient_preferences("N/A","remove pref")

    outcome = app.utils.remove_patient_preferences("test","remove pref")

    assert outcome == False

#------------- Update patient synmptoms --------------
def test1_update_patient_symptoms():#Testing for a successful update
    outcome = app.utils.update_patient_symptoms("test","test symptoms")

    assert outcome == True

    user = app.utils.load_patient("test","data/patient_data.json") # checking function updated

    assert user.symptoms == "test symptoms"

def test2_update_patient_symptoms():# testing for no input
    outcome = app.utils.update_patient_symptoms("test","")

    assert outcome == False

def test3_update_patient_symptoms():#testing for no user id 
    outcome = app.utils.update_patient_symptoms("","test symptoms")

    assert outcome == False

def test4_update_patient_symptoms():#Testing for invalid user id
    outcome = app.utils.update_patient_symptoms("N/A","test symptoms")

    assert outcome == False

#------------- Update personal note --------------
def test1_update_personal_note():
    outcome = app.utils.update_patient_personal_note("test","test note")

    assert outcome == True

    user = app.utils.load_patient("test","data/patient_data.json") # Testing to make sure it was submitted

    assert user.personal_notes[-1][f"Note {len(user.personal_notes)}"] == "test note"

def test2_update_personal_note():#Testing for no input
    outcome = app.utils.update_patient_personal_note("test","")

    assert outcome == False

def test3_update_personal_note():#testing for no user id
    outcome = app.utils.update_patient_personal_note("","test note")

    assert outcome == False

def test4_update_personal_note():#Testing for invalid user id
    outcome = app.utils.update_patient_personal_note("N/A","test note")

    assert outcome == False


