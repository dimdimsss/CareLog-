from app import User

class patient(User):
    def __init__(self, user_id, password, name, role, symptoms="None", preferences="None", logs=None):
        super().__init__(user_id, password, name, role)

        self.symptoms = symptoms
        self.preferences = preferences
        self.logs = logs if logs is not None else []
