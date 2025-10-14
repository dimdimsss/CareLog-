#"utility" file for functions. we can organise classes and other function better in other files later on
import json
from app.user import User
from app.patient import Patient


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

def load_patient(user_id, data_file):
    with open(data_file, "r") as f:
        data = json.load(f)

    for patient_data in data["patient_data"]:
        if patient_data["user_id"] == user_id:
            return Patient(**patient_data)