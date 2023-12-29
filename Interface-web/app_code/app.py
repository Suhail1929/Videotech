import json
import os
from functools import wraps

import click
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash


# [ -- Utils -- ]


def validate_login(user):
    db_users = json.load(open("users.json"))
    if not db_users.get(user["username"]):
        return False
    stored_password = db_users[user["username"]]["password"]
    if check_password_hash(stored_password, user["password"]):
        return True
    return False


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
    json.dump(db_users, open("users.json", "w"))
    return data


# [--- Flask Factories  ---]


def create_app():
    app = Flask(__name__)
    #app.config.from_object("settings")
    return app


def configure_extensions(app):
    messages = {
        "login_success": Message("Bienvenue!", "success"),
        "is_logged_in": Message("Vous êtes déjà connecté", "success"),
        "logout": None,
        "login_failure": Message("Mauvais nom d'utilisateur ou mot de passe", "danger"),
    }
    SimpleLogin(app, login_checker=validate_login, messages=messages)
    if not os.path.exists("users.json"):
        with open("users.json", "a") as json_file:
            # This just touch create a new dbfile
            json.dump({"username": "", "password": ""}, json_file)


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

    @app.route("/complex")
    @login_required(username=["admin"] or ["1"])
    def complexview():
        return render_template("secret.html")

    @app.route("/create", methods=["GET", "POST"])
    def create():
        if request.method == "POST":
            # Récupère les données du formulaire
            username = request.form.get("username")
            password = request.form.get("password")

            # Vérifie si le nom d'utilisateur existe déjà
            db_users = json.load(open("users.json"))
            if username in db_users:
                with app.app_context():
                    flash("Ce nom d'utilisateur est déjà pris.", "danger")
            else:
                # Crée l'utilisateur
                create_user(username=username, password=password)
                with app.app_context():
                    flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")
                return redirect(url_for("simplelogin.login"))

        # Affiche le formulaire de création de compte
        return render_template("create.html")

# [--- Command line functions ---]


def with_app(f):
    """Calls function passing app as first argument"""

    @wraps(f)
    def decorator(*args, **kwargs):
        app = create_app()
        configure_extensions(app)
        configure_views(app)
        return f(app=app, *args, **kwargs)

    return decorator


@click.group()
def main():
    """Flask Simple Login Example App"""

@main.command()
@with_app
def runserver(app=None):
    app.run(host="0.0.0.0")

# [--- Entry point ---]    
if __name__ == "__main__":
    # python manage.py to see help
    main()




