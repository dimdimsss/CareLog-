#"utility" file for functions. we can organise classes and other function better in other files later on
import json
from app.user import User


def testfunction():
    print("function is working!")

def load_user(user_id):
    """Loads a user by ID from the JSON file and returns a User object."""
    print("yeah")
    with open("data/users.json", "r") as f:
        data = json.load(f)

    for user_data in data["users"]:
        if user_data["user_id"] == user_id:
            return User(**user_data)




class TestClass:
    """If you are seeing this message in streamlit, it means class imports are working"""
    def __init__(self, field):
        self.field = field



class Patient:
    """placeholder docstring"""
    def __init__(self, mrn): # what does mrn mean?(UML diagram)
        self.mrn = mrn

class CareStaff:
    """placeholder docstring"""
    def __init__(self, speciality):
        self.speciality = speciality