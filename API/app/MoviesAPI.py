from app import app
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
import requests

headers = {
    "X-RapidAPI-Key": "e9a3b6cd69msh586db169351ffb7p163bb1jsnaa1c07fd0927",
    "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
}

@app.route('/get_movies', methods=['GET'])
def get_movies():
    
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    
    querystring = {"limit":"50" , "list":"top_boxoffice_200"}

    response = requests.get(url, headers=headers , params=querystring)
    
    return response.json()

@app.route('/get_movies_by_year/<year>', methods=['GET'])
def get_movies_by_year(year):
    
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"year": year , "limit":"50"}

    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

@app.route('/get_movies_by_genre/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"genre": genre , "limit":"50"}

    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()


@app.route('/get_movies_by_title/<title>', methods=['GET'])
def get_movies_by_title(title):
    
    url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/"+title

    querystring = {"exact":"true","titleType":"movie"}

    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

@app.route('/get_movies_by_titleType/<titleType>', methods=['GET'])
def get_movies_by_titleType(titleType):
    
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"titleType": titleType , "limit":"50"}

    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

@app.route('/get_genres', methods=['GET'])
def get_genres():
    
    url = "https://moviesdatabase.p.rapidapi.com/titles/utils/genres"

    response = requests.get(url, headers=headers)
    
    return response.json()


@app.route('/get_titleType', methods=['GET'])
def get_titleType():
    
    url = "https://moviesdatabase.p.rapidapi.com/titles/utils/titleTypes"

    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

