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
            json.dump(films, file)

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

        # for film in films:
        #     if film['title'] == title:
        #         return {"error": "Un film avec ce titre existe déjà"}, 400

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
    
    def delete_film(self, username, film_title):
        films = self.load_films()
        films = [user for user in films if user.get('username') != username]
        user_film = self.get_user_film(username)
        user_film = [film for film in user_film if film.get('title') != film_title]
        films.append(user_film)
        self.save_films(films)
        return {"result": True}, 201

film_db = FilmDatabase()

@app.route('/add_film', methods=['POST'])
def add_film():
    data = request.json  # Assuming data is sent as a JSON object
    result = film_db.add_film(data)
    return jsonify(result), 201

@app.route('/get_films', methods=['POST'])
def get_films():
    username = request.json
    films = film_db.get_user_film(username)
    return jsonify(films), 201

@app.route('/delete_film')
def delete_film():
    data = request.json
    username = data["username"]
    film = data["film"]
    result = film_db.delete_film(username,film)
    return jsonify(result), 201
