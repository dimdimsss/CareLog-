#"utility" file for functions. we can organise classes and other function better in other files later on
import json
from app.user import User


def test_function():
    print("function is working!")


class TestClass:
    """If you are seeing this message in streamlit, it means class imports are working"""
    def __init__(self, field):
        self.field = field


def load_user(user_id, data_file):
    """Loads a user by user_id from the json file and returns a User object using the corresponding data"""
    with open(data_file, "r") as f:
        data = json.load(f)

    for user_data in data["users"]:
        if user_data["user_id"] == user_id:
            return User(**user_data)

def get_patient_logs(user_id, data_file):
    """Returns a Patient's list of logs from the logs attribute in the json file"""
    with open(data_file, "r") as f:
        data = json.load(f)

    for patient_data in data["patient_data"]:
        if patient_data["user_id"] == user_id:
            return patient_data["logs"]



# I've included these classes but i'm not sure if they are actually necassary. Will move to their own file if needed.
class Patient:
    """placeholder docstring"""
    def __init__(self, mrn): # what does mrn mean?(UML diagram)
        self.mrn = mrn

class CareStaff:
    """placeholder docstring"""
    def __init__(self, speciality):
        self.speciality = speciality