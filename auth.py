import json
import os
from Crypto.Hash import SHA256

USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return SHA256.new(password.encode()).hexdigest()

def signup(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists"

    users[username] = hash_password(password)
    save_users(users)
    return True, "Signup successful"

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"

    if users[username] != hash_password(password):
        return False, "Wrong password"

    return True, "Login successful"