from app import app, api_url
import json
import os
import requests
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required


@app.route("/")
def index():
    # Faites une requête à votre API pour obtenir la liste des films
    response = requests.get(f"{api_url}/get_films")
    films = response.json() if response.status_code == 200 else []
    # Passez la liste des films au template Jinja
    return render_template('index.html', films=films)

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
    return render_template('add_film.html')