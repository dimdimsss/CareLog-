from app.user import User

class Patient(User):
    def __init__(self, user_id, password, name, role, symptoms, preferences, logs=None): # Im not sure if we need role or password on object creation, might be removeable and assigned default values in super
        super().__init__(user_id, password, name, role) # Base attributes from User

        # Attributes for data
        self.symptoms = symptoms
        self.preferences = preferences
        self.logs = logs if logs is not None else [] # Loading a patient normally assigns a list with logs as dictionary elements inside of it for this attribute on object creation. If it doesn't it will just make an empty list for you to append to later. This is because sometimes a user might, or might not have existing logs
