#"utility" file for functions. we can organise classes and other function better in other files later on
import json

def testfunction():
    print("function is working!")

class User:
    """placeholder docstring"""
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

class Patient:
    """placeholder docstring"""
    def __init__(self, mrn): # what does mrn mean?(UML diagram)
        self.mrn = mrn

class CareStaff:
    """placeholder docstring"""
    def __init__(self, speciality):
        self.speciality = speciality