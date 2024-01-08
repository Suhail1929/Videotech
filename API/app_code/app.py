import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
api = Api(app)

@app.route('/')
def hello():
    return 'Hello, AdPIs'

# Charger les données depuis le fichier JSON au démarrage de l'application
DATA_FILE = "videolibrary.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

videolibrary = load_data()

class UserResource(Resource):
    def get(self, username):
        if username in videolibrary["users"]:
            return videolibrary["users"][username]
        else:
            return {"error": "Utilisateur non trouvé"}, 404

    def put(self, username):
        data = request.get_json()
        if username not in videolibrary["users"]:
            videolibrary["users"][username] = {"films": []}
        videolibrary["users"][username]["films"] = data.get("films", [])
        save_data(videolibrary)
        return videolibrary["users"][username], 201

api.add_resource(UserResource, "/user/<string:username>")

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


def load_films():
    try:
        with open('films.json', 'r') as file:
            films = json.load(file)
    except FileNotFoundError:
        films = []
    return films

# Fonction pour enregistrer les films dans le fichier JSON
def save_films(films):
    with open('films.json', 'w') as file:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')


# with open("video.json") as jsfic:
# myvideo = json.load(jsfic)
# for film in myvideo["films"]:
# print("Film : {} année : {}".format(film["titre"], film["année"]))
# print(" réalisateur : {} {}".format(film["réalisateur"]["prénom"],film["réalisateur"]["nom"]))
# print(" acteurs : ", end="")
# for act in film["acteurs"]:
# print("{} {}".format(act["prénom"],act["nom"]),end=" ")
# print ("\n ----------------------------------------")
# jsfic.close()