# auth.py
import json


# Load users from the JSON file
def load_users(file_path="login_data.json"):
    """Load all user data from the JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data["users"]
    except FileNotFoundError:
        return []


# Function to authenticate users during login
def login(username, password):
    """Authenticate the user by matching username and password."""
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user  # Return user details if authentication is successful
    return None  # Return None if authentication fails


# Function to create a new account
def create_account(username, password, role, file_path="login_data.json"):
    """Create a new user account and save it in the JSON file."""
    users = load_users(file_path)
    user_id = len(users) + 1  # Incremental user ID

    new_user = {
        "user_id": user_id,
        "username": username,
        "password": password
    }
    users.append(new_user)

    # Save the updated user list back to the JSON file
    with open(file_path, "w") as file:
        json.dump({"users": users}, file, indent=4)
