class User:
    """Class that represents the users of CareLog"""
    def __init__(self, user_id, password, name, role):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.role = role

    # This is just for testing
    def __repr__(self):
        return f"User(user_id='{self.user_id}', name='{self.name}', role='{self.role}')"