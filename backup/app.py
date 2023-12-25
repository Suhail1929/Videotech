from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videolibrary.db'
db = SQLAlchemy(app)

# Modèle de données pour les films
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    realisateur = db.Column(db.String(100), nullable=False)
    annee = db.Column(db.Integer, nullable=False)

# Crée la base de données (à utiliser uniquement pour la première fois)
# db.create_all()

@app.route('/')
def racine():
    # Redirige automatiquement vers la page d'accueil
    return redirect(url_for('home.html'))

@app.route('/')
def accueil():
    films = Film.query.all()
    return render_template('videolibrary.html', films=films, current_user=get_current_user())

@app.route('/ajouter', methods=['POST'])
def ajouter_film():
    titre = request.form['titre']
    realisateur = request.form['realisateur']
    annee = request.form['annee']

    nouveau_film = Film(titre=titre, realisateur=realisateur, annee=annee)
    db.session.add(nouveau_film)
    db.session.commit()

    return redirect(url_for('accueil'))

@app.route('/supprimer/<int:film_id>', methods=['POST'])
def supprimer_film(film_id):
    film_a_supprimer = Film.query.get(film_id)
    if film_a_supprimer:
        db.session.delete(film_a_supprimer)
        db.session.commit()

    return redirect(url_for('accueil'))

def get_current_user():
    # La logique de récupération de l'utilisateur actuel doit être implémentée
    # Cette fonction peut retourner l'utilisateur actuel ou None si l'utilisateur n'est pas connecté.
    return None

if __name__ == '__main__':
    app.run(debug=True)