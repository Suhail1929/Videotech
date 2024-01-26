from app import app
import json
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

# Classe concernant toutes les fonctions liées aux utilisateurs
class UserDatabase:
    def __init__(self):
        pass
    
    # Fonction qui teste si le login et mot de passe sont valides
    def validate_login(self, user):
        username = user.get('username')
        password = user.get('password')
        users = self.load_users()

        for u in users:
            if u.get('username') == username and check_password_hash(u.get('password'), password):
                return True
        
        return False
    
    # Charge la base de donnée des utilisateurs
    def load_users(self):
        try:
            with open('DB/users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []
        return users

    # Fonction pour sauvegarder les modifications de users.json
    def save_users(self, films):
        with open('DB/users.json', 'w') as file:
            json.dump(films, file)

    # Fonction pour créer un nouvel utilisateur, les mots de passe sont chiffrés
    def create_user(self, username, password, role="user"):
        users = self.load_users()
        if users and any(user.get('username') == username for user in users):
            return False 
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_users = {"username": username, "password": hashed_password , "role": role}
        
        users.append(new_users)    
        self.save_users(users)  

        return True

    # Fonction pour récupérer la liste des utilisateurs
    def get_users(self):
        users = self.load_users()
        usernames = [username for username in users.keys() if isinstance(users[username], dict)]
        return usernames 

    # Fonction pour supprimer un utilisateur
    def delete_users(self, username):
        users = self.load_users()
        new_users = [user for user in users if user.get('username') != username]
        if users == new_users:
            return False
        self.save_users(new_users)

        # Partie permettant de supprimer tous les films de l'utilisateur 
        # supprimé pour éviter les résidus dans le fichier des films
        with open("DB/films.json", "r") as json_films:
            data = json.load(json_films)
        if data[username]:
            del data[username]    
        with open("DB/films.json", "w") as json_films:
            json.dump(data, json_films) 
        return True
    
    def change_password(self, username, old_password, new_password):
        users = self.load_users()
        for u in users:
            if u.get('username') == username and check_password_hash(u.get('password'), old_password):
                hashed_password = generate_password_hash(new_password, method="pbkdf2:sha256")
                u['password'] = hashed_password
                self.save_users(users)
                return True
        return False

    # Permet de changer les droits d'un utilisateur
    def update_roles(self, username, role):
        users = self.load_users()
        for u in users:
            if u.get('username') == username:
                u['role'] = role
                self.save_users(users)                    
                return True
        return False    

# Instancier la classe UserDatabase
user_db = UserDatabase()

# Route pour la validation du login
@app.route("/validate_login", methods=["POST"])
def api_validate_login():
    user = request.json
    result = user_db.validate_login(user)
    return jsonify({"result": result})

# Route pour la création d'un compte
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    result = user_db.create_user(data["username"], data["password"])
    return jsonify({"result": result}), 201 if result else 400

# Route pour la récupération de tous les utilisateurs
@app.route('/get_users', methods=['GET'])
def get_users():
    users = user_db.load_users()
    return jsonify(users), 201

# Route pour le changement des droits d'un utilisateur
@app.route('/update_role', methods=['POST'])
def update_role():
    data = request.json
    username = data.get('username')
    role = data.get('role')
    result = user_db.update_roles(username, role)
    return jsonify({"result": result}), 201 if result else 400

# Route pour la suppression d'un utilisateur
@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    username = data.get('username')
    result = user_db.delete_users(username)
    return jsonify({"result": result}), 201 if result else 400

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    result = user_db.change_password(username, old_password, new_password)
    return jsonify({"result": result}), 201 if result else 400

@app.route('/get_role', methods=['POST','GET'])
def get_role():
    data = request.json
    username = data.get('username')
    users = user_db.load_users()
    for u in users:
        if u.get('username') == username:
            role = u['role']
    return jsonify(role), 201


    