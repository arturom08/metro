
class User:
    def __init__(self, id, name, email, username, type, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.type = type
