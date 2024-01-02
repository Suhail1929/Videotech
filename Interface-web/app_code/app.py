import json
import os
import requests
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required

api_url = "http://10.11.5.145:5100"

def validate_login(user):

    # Requête HTTP vers votre API pour valider le login
    response = requests.post(f"{api_url}/validate_login", json=user)

    # Si la requête est réussie (code 200) et le résultat est True, retournez True
    if response.status_code == 200 and response.json().get("result") == True:
        return True
    return False

# [--- Flask Factories  ---]
def configure_extensions(app):
    messages = {
        "login_success": Message("Bienvenue!", "success"),
        "is_logged_in": Message("Vous êtes déjà connecté", "success"),
        "logout": None,
        "login_failure": Message("Mauvais nom d'utilisateur ou mot de passe", "danger"),
        "login_required": Message("Vous devez d'abord vous connecter", "warning"),
    }
    SimpleLogin(app, login_checker=validate_login, messages=messages)
    # if not os.path.exists("users.json"):
    #     with open("users.json", "a") as json_file:
    #         # This just touch create a new dbfile
    #         json.dump({"username": "", "password": ""}, json_file)

def configure_views(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/secret")
    @login_required()
    def secret():
        return render_template("secret.html")

    @app.route("/api", methods=["POST"])
    @login_required(basic=True)
    def api():
        return jsonify(data="You are logged in with basic auth")

    @app.route("/administrator")
    @login_required(username=["admin"] or ["1"])
    def administrator():
        response = requests.get(f"{api_url}/users")
        # Vérifier si la requête a réussi (code de statut HTTP 200)
        if response.status_code == 200:
            # Analyser la réponse JSON
            users = response.json()
            users = list(users)               
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
        return render_template("administrator.html", users=users)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            # Récupère les données du formulaire
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas.", "danger")
            else:
                data = {'username': username, 'password': password}
                response = requests.post(f"{api_url}/register", json=data)
                # Vérifie si le nom d'utilisateur existe déjà
                if response.status_code == 201 and response.json().get("result") == True:
                    with app.app_context():
                        flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")
                    return redirect(url_for("simplelogin.login"))
                else:
                    with app.app_context():
                        flash("Ce nom d'utilisateur est déjà pris.", "danger")
        # Affiche le formulaire de création de compte
        return render_template("register.html")

def runserver(app=None):
    app = Flask(__name__)
    configure_extensions(app)
    configure_views(app)
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    runserver()
    



