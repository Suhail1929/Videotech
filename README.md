# Vidéothèque: Cinverse library

Site internet codé à l'aide du framework flask codé en python, le CSS est fait à l'aide de boostrap et les templates des pages web en jinja (lié à flask).
Il permet de créer, visualiser, modifier et supprimer des films.

## Table des matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Fonctionnalités](#fonctionnalités)
4. [Comptes par défaut](#comptes-par-défaut)

## Introduction

Site internet permettant de créer, de visualiser le profil de différents films, d'en ajouter et d'en supprimer. Une liste de films provenant d'une API externe peut aussi être affichée.

## Installation

Une VM de type linux est nécessaire afin de faire fonctionner le projet.
Il est nécessaire d'avoir docker installé pour ce projet car il utilise deux conteneurs, ainsi que git afin de pouvoir cloner le projet.

Mettez vous dans le dossier ou vous souhaitez recevoir le projet puis effectuez cette commande:
```bash
git clone https://github.com/Suhail1929/Videotech.git
```
Allez ensuite dans le fichier Interface-web/app/app.py et modifiez la sixième ligne en mettant l'adresse IP de votre propre machine à la place de 10.11.5.113.
Positionnez vous à la racine du projet puis effectuez cette commande:
```bash
sudo docker-compose --build
```
Vous devriez être en mesure d'accéder au site en tapant dans la barre d'adresse de votre navigateur votre.adresse.i.p:5000

## Fonctionnalités

- **Ajout de films:** Enregistrez vos films préférés avec des détails tels que le titre, le réalisateur, les acteurs, l'année de sortie, le genre, et plus encore.
- **Exploration conviviale:** Parcourez votre collection de films de manière intuitive avec des options de tri et de recherche.
- **Partage avec la communauté:** Partagez vos recommandations de films avec d'autres utilisateurs et découvrez de nouvelles pépites cinématographiques.
- **Affichage de films issus d'une API externe** Obtenez une longue liste de films issus d'une API externe.

## Comptes par défaut

Il existe deux comptes par défaut allant avec le projet.
- **Premier compte:** Nom d'utilisateur: admin, mot de passe ?. Il dispose des privilèges d'administrateur
- **Deuxième compte:** Nom d'utilisateur: ?, mot de passe ?. N'a aucun privilège particulier

Il reste toutefois possible de créer de nouveaux comptes et l'administrateur peut donner des droits d'admin aux simples utilisateurs.


