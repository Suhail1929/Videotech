from app import app
import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
import requests

api_key = '3e7cfcbbde83ea4fac4e860b482ead1c'

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTdjZmNiYmRlODNlYTRmYWM0ZTg2MGI0ODJlYWQxYyIsInN1YiI6IjY1OWZhYjg4MmUwNjk3MDEzMDc0NTIwMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xy6h82kB8u6wBsgAKg3ePYTCrHlraw1elxIOOkL3yTE',
    'accept': 'application/json'
}

@app.route('/get_movies', methods=['GET'])
def get_movies():
    
    url = "https://api.themoviedb.org/3/discover/movie"
    
    params = { 'api_key': api_key , 'language': 'en-US' , 'page': 10 , 'sort_by': 'popularity.desc' , 'include_adult': 'false' , 'include_video': 'false' }
    
    response = requests.get(url, headers=headers, params=params)
    
    # If the request was successful, extract the films from the response
    if response.status_code == 200:
        films = response.json()["results"]

    # Make subsequent requests to get the next 20 films, 40 films, and so on
    for i in range(2, 100, 20):
        params["page"] = i
        response = requests.get(url, params=params)

        # If the request was successful, append the films to the list
        if response.status_code == 200:
            films += response.json()["results"]
    
    
    return jsonify(films)

# @app.route('/get_movies_by_year/<year>', methods=['GET'])
# def get_movies_by_year(year):
    
#     url = "https://moviesdatabase.p.rapidapi.com/titles"

#     querystring = {"year": year , "limit":"50"}

#     response = requests.get(url, headers=headers, params=querystring)
    
#     return response.json()

# @app.route('/get_movies_by_genre/<genre>', methods=['GET'])
# def get_movies_by_genre(genre):
    
#     url = "https://moviesdatabase.p.rapidapi.com/titles"

#     querystring = {"genre": genre , "limit":"50"}

#     response = requests.get(url, headers=headers, params=querystring)
    
#     return response.json()


# @app.route('/get_movies_by_title/<title>', methods=['GET'])
# def get_movies_by_title(title):
    
#     url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/"+title

#     querystring = {"exact":"true","titleType":"movie"}

#     response = requests.get(url, headers=headers, params=querystring)
    
#     return response.json()

# @app.route('/get_movies_by_titleType/<titleType>', methods=['GET'])
# def get_movies_by_titleType(titleType):
    
#     url = "https://moviesdatabase.p.rapidapi.com/titles"

#     querystring = {"titleType": titleType , "limit":"50"}

#     response = requests.get(url, headers=headers, params=querystring)
    
#     return response.json()

# @app.route('/get_genres', methods=['GET'])
# def get_genres():
    
#     url = "https://moviesdatabase.p.rapidapi.com/titles/utils/genres"

#     response = requests.get(url, headers=headers)
    
#     return response.json()


# @app.route('/get_titleType', methods=['GET'])
# def get_titleType():
    
#     url = "https://moviesdatabase.p.rapidapi.com/titles/utils/titleTypes"

#     response = requests.get(url, headers=headers, params=querystring)
    
#     return response.json()

