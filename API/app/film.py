from app import app
import json
from flask import request, jsonify

# Classe concernant toutes les fonctions liées aux films
class FilmDatabase:
    def __init__(self):
        pass
    
    # Fonction pour l'ouverture du fichier film.json
    def load_films(self):
        try:
            with open('DB/films.json', 'r') as file:
                films = json.load(file)
        except FileNotFoundError:
            films = {}
        return films

    # Fonction pour sauvegarder les modifications de films.json
    def save_films(self, films):
        with open('DB/films.json', 'w') as file:
            json.dump(films, file)


    # Permet d'ajouter un film en fonction de l'utilisateur qui l'a créé
    def add_film(self, data):
        username = data['username']
        title = data['title']
        genre = data['genre']
        director = data['director']
        actors = data['actors']
        year = data['year']
        description = data['description']
        duree = data['duree']
        production = data['production']
        poster = data['poster']
        visibilite = data['visibilite']
        
        films = self.load_films()
        if username not in films:
            films[username] = []

        new_film = {
            'title': title,
            'genre': genre,
            'director': director,
            'actors': actors,
            'year': year,
            'description': description,
            'production': production,
            'duree': duree,
            'poster': poster,
            'visibilite': visibilite
        }

        films[username].append(new_film)
        self.save_films(films)
        return {"result": True}, 201
    
    # Renvoie tous les films présents dans la base de donnée ainsi que le nom de leur créateur
    def get_films(self):
        return self.load_films()
    
    # Renvoie les films d'un utilisateur en particulier
    def get_user_film(self,username):
        films = self.load_films()
        return films.get(username, [])
    
    # Cette fonction supprime le film choisi par l'utilisateur
    # Si l'utilisateur n'a plus aucun film, son nom est supprimé également du fichier film.json
    def delete_film(self, username, film_title):
        films = self.load_films()
        if username in films:
            x=0
            for film in films[username]:
                if films[username][x]['title'] == film_title:
                    del films[username][x]
                    if films[username] == []:
                        del films[username]
                    self.save_films(films)
                    return {"result": True}
                x+=1
        return {"result": False}
    
    def update_film(self,data):
        username = data['username']
        films = self.load_films()
        if username in films:
            x=0
            for film in films[username]:
                if films[username][x]['title'] == data['film']:
                    films[username][x]['genre'] = data['genre']
                    films[username][x]['director'] = data['director']
                    films[username][x]['actors'] = data['actors']
                    films[username][x]['year'] = data['year']
                    films[username][x]['description'] = data['description']
                    films[username][x]['production'] = data['production']
                    films[username][x]['duree'] = data['duree']
                    films[username][x]['visibilite'] = data['visibilite']
                    if 'poster' in data:
                        films[username][x]['poster'] = data['poster']
                    self.save_films(films)
                    return {"result": True}
                x+=1
        return {"result": False}

# Instancier la classe FilmDatabase
film_db = FilmDatabase()

# Route pour l'ajout d'un film
@app.route('/add_film', methods=['POST'])
def add_film():
    data = request.json
    result = film_db.add_film(data)
    return jsonify(result), 201

# Route pour la récupération des films d'un utilisateur
@app.route('/get_films_user', methods=['POST'])
def get_films_user():
    username = request.json
    films = film_db.get_user_film(username)
    return jsonify(films), 201

# Route pour la suppression d'un film d'un utilisateur
@app.route('/delete_film', methods=['POST'])
def delete_film():
    data = request.json
    username = data["username"]
    film = data["film"]
    result = film_db.delete_film(username=username,film_title=film)
    return jsonify(result), 201

@app.route('/update_film', methods=['POST'])
def update_film():
    data = request.json
    username = data["username"]
    result = film_db.update_film(data=data)
    return jsonify(result), 201

# Route pour la récupération de tous les films créés par les utilisateurs
@app.route('/get_films', methods=['POST'])
def get_films():
    films = film_db.get_films()
    return jsonify(films), 201