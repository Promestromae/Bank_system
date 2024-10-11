import hashlib
import json
import os
from models import User
from models import Session

class AuthSystem:
    def __init__(self, db_path='users.json'):
        self.db_path = db_path
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.users, file)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if username in self.users:
            return "Username already exists."
        self.users[username] = self.hash_password(password)
        self.save_users()
        return "User registered successfully."

    def login(self, username, password):
        if username not in self.users:
            return "Username does not exist."
        if self.users[username] != self.hash_password(password):
            return "Incorrect password."
        return "Login successful."

# Example usage
if __name__ == "__main__":
    auth_system = AuthSystem()

    # Register a new user
    print(auth_system.register("user1", "password123"))

    # Attempt to login
    print(auth_system.login("user1", "password123"))
    print(auth_system.login("user1", "wrongpassword"))
    print(auth_system.login("nonexistentuser", "password123"))