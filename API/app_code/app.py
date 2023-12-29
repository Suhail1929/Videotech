import json
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello():
    return 'Hello, AdddddPIs'

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