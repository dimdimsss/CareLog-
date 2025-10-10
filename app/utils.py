#"utility" file for functions. we can organise classes and other function better in other files later on
import json


def testfunction():
    print("function is working!")


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