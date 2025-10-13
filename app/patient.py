from app.user import User

class patient(User):
    def __init__(self, user_id, password, name, role, symptoms="None", preferences="None", logs=None):
        super().__init__(user_id, password, name, role)

        self.symptoms = symptoms
        self.preferences = preferences
        self.logs = logs if logs is not None else [] # You normally create a list with a log as a dictionary element inside of it for this attribute on object creation. if you don't it will just make an empty list for you to add stuff to later
