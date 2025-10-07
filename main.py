class CareLog:
    def __init__(self, patients_name, log, date_and_time):
        self.patients_name = patients_name
        self.log = log
        self.date_and_time = date_and_time


class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

class Patient:
    def __init__(self, mrn): # what does mrn mean?(UML diagram)
        self.mrn = mrn
        pass

class CareStaff:
    def __init__(self, speciality):
        self.speciality = speciality


# test commit