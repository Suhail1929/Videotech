from app import app, api_url
import json
import os
import requests
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required , get_username

def validate_login(user):

    # Requête HTTP vers votre API pour valider le login
    response = requests.post(f"{api_url}/validate_login", json=user)

    # Si la requête est réussie (code 200) et le résultat est True, retournez True
    if response.status_code == 200 and response.json().get("result") == True:
        return True
    return False

# [--- Flask Factories  ---]
messages = {
    "login_success": Message("Bienvenue!", "success"),
    "is_logged_in": Message("Vous êtes déjà connecté", "success"),
    "logout": None,
    "login_failure": Message("Mauvais nom d'utilisateur ou mot de passe", "danger"),
    "login_required": Message("Vous devez d'abord vous connecter", "warning"),
}
SimpleLogin(app, login_checker=validate_login, messages=messages)

@app.route("/")
def index():
    # Faites une requête à votre API pour obtenir la liste des films
    response = requests.get(f"{api_url}/get_films")
    films = response.json() if response.status_code == 200 else []
    # Passez la liste des films au template Jinja
    reponse_user = requests.get(f"{api_url}/get_users")
    users = reponse_user.json() if reponse_user.status_code == 200 else []
    # La liste des films de IMDB
    response_api = requests.get(f"{api_url}/get_movies")
    api_films = response_api.json() if response_api.status_code == 200 else []
    #chercher le nom d'utilisateur
    user = None
    username = get_username()
    for u in users:
        if u.get('username') == username:
            user = u
            
    return render_template('index.html', films=films, user=user , api_films=api_films)


@app.route("/api", methods=["POST"])
@login_required(basic=True)
def api():
    return jsonify(data="You are logged in with basic auth")

@app.route("/administrator")
@login_required()
def administrator():
    reponse_user = requests.get(f"{api_url}/get_users")
    users = reponse_user.json() if reponse_user.status_code == 200 else []
    #chercher le nom d'utilisateur
    user = None
    username = get_username()
    for u in users:
        if u.get('username') == username:
            user = u
    if user.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template("administrator.html", users=users , user=user)

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


@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    if request.method == "POST":
        # Ajouter le film à la base de données via l'API
        title = request.form.get("title")
        director = request.form.get("director")
        year = request.form.get("year")
        actors = [actor.strip() for actor in request.form.get('actors').split(',')]
        genre = request.form.get("genre")
        description = request.form.get("description")
        film_data = {
            'title': title,
            'director': director,
            'year': year,
            'actors': actors,
            'genre': genre,
            'description': description
        }
        response = requests.post(f"{api_url}/add_film", json=film_data)
        if response.status_code == 201:
            flash('Film ajouté avec succès !', 'success')
            return redirect(url_for('add_film'))
        else:
            flash('Erreur lors de l\'ajout du film. Veuillez réessayer.', 'danger')
        
    reponse_user = requests.get(f"{api_url}/get_users")
    users = reponse_user.json() if reponse_user.status_code == 200 else []
    #chercher le nom d'utilisateur
    user = None
    username = get_username()
    for u in users:
        if u.get('username') == username:
            user = u
                
    return render_template('add_film.html', user=user)