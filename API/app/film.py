from app import app
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash

def load_films():
    try:
        with open('DB/films.json', 'r') as file:
            films = json.load(file)
    except FileNotFoundError:
        films = []
    return films

# Fonction pour enregistrer les films dans le fichier JSON
def save_films(films):
    with open('DB/films.json', 'w') as file:
        json.dump(films, file, indent=2)

# Route pour ajouter un film
@app.route('/add_film', methods=['POST'])
def add_film():
    data = request.json  # Supposons que les données sont envoyées en tant qu'objet JSON
    title = data['title']
    genre = data['genre']
    director = data['director']
    actors = data['actors']
    year = data['year']
    description = data['description']

    # Charger les films existants
    films = load_films()

    # Ajouter le nouveau film à la liste
    new_film = {
        'title': title,
        'genre': genre,
        'director': director,
        'actors': actors,
        'year': year,
        'description': description
    }

    films.append(new_film)

    # Enregistrer les films mis à jour
    save_films(films)
    return jsonify({"result": True}), 201


@app.route('/get_films', methods=['GET'])
def get_films():
    # Charger les films existants
    films = load_films()
    return jsonify(films), 200