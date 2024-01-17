from app import app, api_url
import requests
from flask import jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, get_username, login_required


# Fonction pour demander la vérification du login
def validate_login(user):

    response = requests.post(f"{api_url}/validate_login", json=user)
    if response.status_code == 200 and response.json().get("result") == True:
        return True
    return False

# Fonction permettant de récupérer le rôle de l'utilisateur pour contrôler l'accès aux pages
def get_role(username):
    username = {'username': username}
    response = requests.post(f"{api_url}/get_role", json=username)
    if response.status_code == 201:
        role = response.json()
        return role

# Initialisation de Flask-simple login et personnalisation des différents messages
messages = {
    "login_success": Message("Bienvenue!", "success"),
    "is_logged_in": Message("Vous êtes déjà connecté", "success"),
    "logout": None,
    "login_failure": Message("Mauvais nom d'utilisateur ou mot de passe", "danger"),
    "login_required": Message("Vous devez d'abord vous connecter", "warning"),
}
SimpleLogin(app, login_checker=validate_login, messages=messages)

# Route de la page d'acceuil
@app.route("/")
def index():
    role = get_role(get_username())         
    return render_template('index.html',role=role)

# Route pour la création d'un compte
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "danger")
        else:
            data = {'username': username, 'password': password}
            response = requests.post(f"{api_url}/register", json=data)
            if response.status_code == 201 and response.json().get("result") == True:
                with app.app_context():
                    flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")
                return redirect(url_for("simplelogin.login"))
            else:
                with app.app_context():
                    flash("Ce nom d'utilisateur est déjà pris.", "danger")

    return render_template("register.html")

# Route pour la récupération des films d'une API externe
@app.route("/list_films", methods=['GET', 'POST'])
@login_required()
def list_films():

    role = get_role(get_username())     
            
    list_genre =requests.get(f"{api_url}/get_genre")
    genres = list_genre.json() if list_genre.status_code == 200 else []
    
    list_language =requests.get(f"{api_url}/get_languages")
    languages = list_language.json() if list_language.status_code == 200 else []
    
    title = request.args.get('title')
    genre = request.args.get('genre')
    year = request.args.get('year')
    language = request.args.get('language')
    vote = request.args.get('vote')
    
    if title and title != '':
        response_api = requests.get(f"{api_url}/get_movies_by_title/{title}")
        api_films = response_api.json() if response_api.status_code == 200 else []
        return render_template('list_films.html', role=role , api_films=api_films , genres=genres , languages=languages)
    elif genre and genre != '':
        response_api = requests.get(f"{api_url}/get_movies_by_genre/{genre}")
        api_films = response_api.json() if response_api.status_code == 200 else []
        return render_template('list_films.html', role=role , api_films=api_films , genres=genres , languages=languages)
    elif year and year != '':
        response_api = requests.get(f"{api_url}/get_movies_by_year/{year}")
        api_films = response_api.json() if response_api.status_code == 200 else []
        return render_template('list_films.html', role=role , api_films=api_films , genres=genres , languages=languages)
    elif language and language != '':
        response_api = requests.get(f"{api_url}/get_movies_by_language/{language}")
        api_films = response_api.json() if response_api.status_code == 200 else []
        return render_template('list_films.html', role=role , api_films=api_films , genres=genres , languages=languages)
    elif vote and vote != '':
        response_api = requests.get(f"{api_url}/get_movies_by_vote_average/{vote}")
        api_films = response_api.json() if response_api.status_code == 200 else []
        return render_template('list_films.html', role=role , api_films=api_films , genres=genres , languages=languages)
    else:
        response_api = requests.get(f"{api_url}/get_movies")
        api_films = response_api.json() if response_api.status_code == 200 else []
        return render_template('list_films.html', role=role , api_films=api_films , genres=genres , languages=languages)

# Route pour afficher tous les films créés par tous les utilisateurs
@app.route('/films_commu', methods=['POST', 'GET'])
@login_required()
def films_commu():
    response = requests.post(f"{api_url}/get_films")
    films = response.json() if response.status_code == 201 else []
    role = get_role(get_username())     
    return render_template('films_commu.html', role=role, films=films)

# Route pour afficher et pouvoir supprimer tous les films créés par l'utilisateur actuel
@app.route('/films_perso', methods=['GET'])
def films_perso():
    username = get_username()
    response = requests.post(f"{api_url}/get_films_user",json=username)
    films = response.json() if response.status_code == 201 else []
    role = get_role(username)     
    return render_template('films_perso.html', role=role, films=films)

# Route permettant à un utilisateur d'ajouter un film
@app.route('/add_film', methods=['GET', 'POST'])
@login_required()
def add_film():
    if request.method == "POST":

        film_data = {
            'username': get_username(),
            'title': request.form.get("title"),
            'director': request.form.get("director"),
            'year': request.form.get("year"),
            'actors': [actor.strip() for actor in request.form.get('actors').split(',')],
            'genre': request.form.get("genre"),
            'description': request.form.get("description"),
            'production': request.form.get("production"),
            'duree': request.form.get("duree")
        }

        response = requests.post(f"{api_url}/add_film", json=film_data)

        if response.status_code == 201:
            flash('Film ajouté avec succès !', 'success')
            return redirect(url_for('films_perso'))
        
        else:
            flash('Erreur lors de l\'ajout du film. Veuillez réessayer.', 'danger')
        
    role = get_role(get_username())   

    return render_template('add_film.html', role=role)

# Route permettant de supprimer un film
@app.route('/delete_film/<film>', methods=['POST', 'GET'])
@login_required()
def delete_film(film):
    data = {
        'username': get_username(),
        'film': film,
    }
    response = requests.post(f"{api_url}/delete_film",json=data)
    if response.status_code == 201:
        flash('Film supprimé avec succès !', 'success')
        return redirect(url_for('films_perso'))
    else:
        flash('Erreur avec la suppression.', 'danger')
    return redirect(url_for('films_perso'))

# Route de la page administrateur
@app.route("/administrator")
@login_required()
def administrator():
    response = requests.get(f"{api_url}/get_users")
    users = response.json() if response.status_code == 200 else []
    role = get_role(get_username())     
    if role != 'admin':
        return redirect(url_for('index'))
    
    return render_template("administrator.html", users=users , role=role)

# Route permettant de modifier les droits d'un utilisateur
@app.route('/update_role/<username>/<action>', methods=['POST', 'GET'])
@login_required()
def update_role(username, action):

    data = {
        'username': username,
        'role': action,
    }

    response = requests.post(f"{api_url}/update_role", json=data)
    if response.status_code == 201:
        flash('Rôle changé avec succès !', 'success')
        return redirect(url_for('administrator'))
    else:
        flash('Erreur avec le changement de rôle.', 'danger')

    return redirect(url_for('administrator'))

# Route permettant de supprimer un utilisateur
@app.route('/delete_user/<username>', methods=['POST', 'GET'])
@login_required()
def delete_user(username):
    data = {'username':username}
    response = requests.post(f"{api_url}/delete_user", json=data)
    if response.status_code == 201:
        flash('Utilisateur supprimé avec succès !', 'success')
        return redirect(url_for('administrator'))
    else:
        flash('Erreur avec la suppression.', 'danger')

    return redirect(url_for('administrator'))


    
    
