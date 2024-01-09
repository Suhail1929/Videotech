from app import app
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash



def validate_login(user):
    db_users = json.load(open("users.json"))
    if not db_users.get(user["username"]):
        return False
    stored_password = db_users[user["username"]]["password"]
    if check_password_hash(stored_password, user["password"]):
        return True
    return False

@app.route("/validate_login", methods=["POST"])
def api_validate_login():
    user = request.json  # Récupère les données du formulaire depuis la requête JSON
    result = validate_login(user)
    return jsonify({"result": result})

def create_user(**data):
    """Creates user with encrypted password"""
    if "username" not in data or "password" not in data:
        raise ValueError("username and password are required.")

    # Hash the user password
    data["password"] = generate_password_hash(
        data.pop("password"), method="pbkdf2:sha256"
    )

    # Here you insert the `data` in your users database
    # for this simple example we are recording in a json file
    db_users = json.load(open("users.json"))
    # add the new created user to json
    db_users[data["username"]] = data
    # commit changes to database
    json.dump(db_users, open("users.json", "w"),indent=1)
    return data


@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Assurez-vous que le contenu est au format JSON
    db_users = json.load(open("users.json"))
    if db_users.get(data["username"]):
        return jsonify({'result': False})
    else:
        create_user(username=data["username"], password=data["password"])
        return jsonify({"result": True}), 201   


@app.route('/users', methods=['POST']) 
def users():
    with open("votre_fichier.json", "r") as json_file:
        data = json.load(json_file)

    # Extraire les identifiants (noms d'utilisateur)
    usernames = [username for username in data.keys() if isinstance(data[username], dict)]

    # Convertir la liste d'identifiants en JSON
    usernames_json = json.dumps(usernames)
    return(usernames_json)
