from app import app
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash

class FilmDatabase:
    def __init__(self):
        pass

    def load_films(self):
        try:
            with open('DB/films.json', 'r') as file:
                films = json.load(file)
        except FileNotFoundError:
            films = {}
        return films

    def save_films(self, films):
        with open('DB/films.json', 'w') as file:
            json.dump(films, file, indent=2)

    def add_film(self, data):
        #username = data.pop('username', None)
        username = data['username']
        title = data['title']
        genre = data['genre']
        director = data['director']
        actors = data['actors']
        year = data['year']
        description = data['description']
        duree = data['duree']
        production = data['production']
        # Load existing films
        films = self.load_films()
        if username not in films:
            films[username] = []

        # Add the new film to the list
        new_film = {
            'title': title,
            'genre': genre,
            'director': director,
            'actors': actors,
            'year': year,
            'description': description,
            'production': production,
            'duree': duree
        }
        films[username].append(new_film)
        # Save the updated films
        self.save_films(films)
        return {"result": True}, 201
    
    def get_user_film(self,username):
        films = self.load_films()
        return films.get(username, [])


film_db = FilmDatabase()

@app.route('/add_film', methods=['POST'])
def add_film():
    data = request.json  # Assuming data is sent as a JSON object
    result = film_db.add_film(data)
    return jsonify(result), 201

@app.route('/get_films', methods=['GET'])
def get_films():
    username = request.json
    films = film_db.get_user_film(username)
    return jsonify(films), 201

