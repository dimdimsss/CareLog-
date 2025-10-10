class User:
    """placeholder docstring"""
    def __init__(self, user_id, password, name, role):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.role = role

    def __repr__(self):
        return f"User(user_id='{self.user_id}', name='{self.name}', role='{self.role}')"