from app import app
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash

class UserDatabase:
    def __init__(self):
        pass
    
    def validate_login(self, user):
        username = user.get('username')
        password = user.get('password')
        users = self.load_users()

        for u in users:
            if u.get('username') == username and check_password_hash(u.get('password'), password):
                return True
        
        return False
    
    def load_users(self):
        try:
            with open('DB/users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []  # In case of file not found or invalid JSON data, return an empty dictionary
        return users

    def create_user(self, username, password, role="user"):
        """Creates user with encrypted password"""
        users = self.load_users()

        if users and any(user.get('username') == username for user in users):
            return False  # User already exists
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_users = {"username": username, "password": hashed_password , "role": role}
        
        users.append(new_users)
        
        with open('DB/users.json', 'w') as file:
            json.dump(users, file)
        
        return True

    def get_users(self):
        with open("DB/users.json", "r") as json_file:
            data = json.load(json_file)
        usernames = [username for username in data.keys() if isinstance(data[username], dict)]
        return usernames 

    def delete_users(self, username):
        users = self.load_users()
        new_users = [user for user in users if user.get('username') != username]
        if users == new_users:
            return False
        with open("DB/users.json", "w") as json_file:
            json.dump(new_users, json_file)
             
        with open("DB/films.json", "r") as json_file2:
            data = json.load(json_file2)
        del data[username]    
        with open("DB/films.json", "w") as json_file2:
            json.dump(data, json_file2) 
        
        return True
        
    def update_roles(self, username, role):
            users = self.load_users()
            for u in users:
                if u.get('username') == username:
                    u['role'] = role
                    with open("DB/users.json", "w") as json_file:
                        json.dump(users, json_file) 
                    return True
            return False    

user_db = UserDatabase()

@app.route("/validate_login", methods=["POST"])
def api_validate_login():
    user = request.json  # Get form data from JSON request
    result = user_db.validate_login(user)
    return jsonify({"result": result})

@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Ensure content is in JSON format
    result = user_db.create_user(data["username"], data["password"])
    return jsonify({"result": result}), 201 if result else 400

@app.route('/get_users', methods=['GET'])
def get_users():
    users = user_db.load_users()
    return jsonify(users), 200

@app.route('/update_role', methods=['POST'])
def update_role():
    data = request.json
    username = data.get('username')
    role = data.get('role')
    result = user_db.update_roles(username, role)
    return 201 if result else 400

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    username = data.get('username')
    result = user_db.delete_users(username)
    return 201 if result else 400

    