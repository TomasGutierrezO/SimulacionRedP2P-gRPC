import json

class AuthService:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        with open("auth/users.json") as f:
            return json.load(f)

    def authenticate(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False