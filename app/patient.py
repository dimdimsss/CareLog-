from app.user import User

class patient(User):
    def __init__(self, user_id, name, symptoms="None", preferences="None", logs=None): # Shoudn't need role or password on object creation, so they are removed and assigned default values in super()
        super().__init__(user_id, name, password="Default", role="Patient") 

        self.symptoms = symptoms
        self.preferences = preferences
        self.logs = logs if logs is not None else [] # You normally create a list with a log as a dictionary element inside of it for this attribute on object creation. if you don't it will just make an empty list for you to add stuff to later
