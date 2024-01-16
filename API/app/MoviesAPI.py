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
    
    params = { 'api_key': api_key , 'language': 'fr-FR' , 'page': 10 , 'sort_by': 'popularity.desc' , 'include_adult': 'false' , 'include_video': 'false' }
    
    response = requests.get(url, headers=headers, params=params)
    
    # If the request was successful, extract the films from the response
    if response.status_code == 200:
        id_films = response.json()["results"]

    # Make subsequent requests to get the next 20 films, 40 films, and so on
    for i in range(2, 20, 10):
        params["page"] = i
        response = requests.get(url, params=params)

        # If the request was successful, append the films to the list
        if response.status_code == 200:
            id_films += response.json()["results"]
            
    films = []
            
    for ids in id_films:
        url = "https://api.themoviedb.org/3/movie/" + str(ids['id'])
        params = { 'api_key': api_key , 'language': 'fr-FR' }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            films += [response.json()]
        
    
    
    return jsonify(films)

@app.route('/get_movies_by_title/<title>', methods=['GET', 'POST'])
def get_movies_by_title(title):
    
    url = "https://api.themoviedb.org/3/search/movie?query="+title+"&include_adult=false&language=fr-FR&page=1"
    

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTdjZmNiYmRlODNlYTRmYWM0ZTg2MGI0ODJlYWQxYyIsInN1YiI6IjY1OWZhYjg4MmUwNjk3MDEzMDc0NTIwMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xy6h82kB8u6wBsgAKg3ePYTCrHlraw1elxIOOkL3yTE"
    }
    
    response = requests.get(url, headers=headers)

    # If the request was successful, extract the films from the response
    if response.status_code == 200:
        id_films = response.json()["results"]


    id_films = response.json()["results"]
            
    films = []
            
    for ids in id_films:
        url = "https://api.themoviedb.org/3/movie/" + str(ids['id'])
        params = { 'api_key': api_key , 'language': 'fr-FR' }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            films += [response.json()]
        
    
    
    return jsonify(films)

@app.route('/get_movies_by_genre/<genre>', methods=['GET', 'POST'])
def get_movies_by_genre(genre):
        
        url = "https://api.themoviedb.org/3/discover/movie"
        
        params = { 'api_key': api_key , 'language': 'fr-FR' , 'page': 1 , 'sort_by': 'popularity.desc' , 'include_adult': 'false' , 'include_video': 'false' , 'with_genres': genre }
        
        response = requests.get(url, headers=headers, params=params)
        
        # If the request was successful, extract the films from the response
        if response.status_code == 200:
            id_films = response.json()["results"]
    
        # Make subsequent requests to get the next 20 films, 40 films, and so on
        for i in range(2, 20, 10):
            params["page"] = i
            response = requests.get(url, params=params)
    
            # If the request was successful, append the films to the list
            if response.status_code == 200:
                id_films += response.json()["results"]
                
        films = []
                
        for ids in id_films:
            url = "https://api.themoviedb.org/3/movie/" + str(ids['id'])
            params = { 'api_key': api_key , 'language': 'fr-FR' }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                films += [response.json()]
            
        
        
        return jsonify(films)

@app.route('/get_genre', methods=['GET'])
def get_genre():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=fr"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTdjZmNiYmRlODNlYTRmYWM0ZTg2MGI0ODJlYWQxYyIsInN1YiI6IjY1OWZhYjg4MmUwNjk3MDEzMDc0NTIwMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xy6h82kB8u6wBsgAKg3ePYTCrHlraw1elxIOOkL3yTE"
    }

    response = requests.get(url, headers=headers)
    
    return response.json()

@app.route('/get_languages', methods=['GET'])
def get_languages():
    url = "https://api.themoviedb.org/3/configuration/languages"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTdjZmNiYmRlODNlYTRmYWM0ZTg2MGI0ODJlYWQxYyIsInN1YiI6IjY1OWZhYjg4MmUwNjk3MDEzMDc0NTIwMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xy6h82kB8u6wBsgAKg3ePYTCrHlraw1elxIOOkL3yTE"
    }
    
    reponse = requests.get(url, headers=headers)
    
    return reponse.json()

@app.route('/get_movies_by_year/<year>', methods=['GET', 'POST'])
def get_movies_by_year(year):
        
        url = "https://api.themoviedb.org/3/discover/movie"
        
        params = { 'api_key': api_key , 'language': 'fr-FR' , 'page': 1 , 'sort_by': 'popularity.desc' , 'include_adult': 'false' , 'include_video': 'false' , 'year': year }
        
        response = requests.get(url, headers=headers, params=params)
        
        # If the request was successful, extract the films from the response
        if response.status_code == 200:
            id_films = response.json()["results"]
    
        # Make subsequent requests to get the next 20 films, 40 films, and so on
        for i in range(2, 20, 10):
            params["page"] = i
            response = requests.get(url, params=params)
    
            # If the request was successful, append the films to the list
            if response.status_code == 200:
                id_films += response.json()["results"]
                
        films = []
                
        for ids in id_films:
            url = "https://api.themoviedb.org/3/movie/" + str(ids['id'])
            params = { 'api_key': api_key , 'language': 'fr-FR' }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                films += [response.json()]
            
        
        
        return jsonify(films)
    
@app.route('/get_movies_by_language/<language>', methods=['GET', 'POST'])
def get_movies_by_language(language):
        
        url = "https://api.themoviedb.org/3/discover/movie"
        
        params = { 'api_key': api_key , 'language': 'fr-FR' , 'page': 1 , 'sort_by': 'popularity.desc' , 'include_adult': 'false' , 'include_video': 'false' , 'with_original_language': language }
        
        response = requests.get(url, headers=headers, params=params)
        
        # If the request was successful, extract the films from the response
        if response.status_code == 200:
            id_films = response.json()["results"]
    
        # Make subsequent requests to get the next 20 films, 40 films, and so on
        for i in range(2, 20, 10):
            params["page"] = i
            response = requests.get(url, params=params)
    
            # If the request was successful, append the films to the list
            if response.status_code == 200:
                id_films += response.json()["results"]
                
        films = []
                
        for ids in id_films:
            url = "https://api.themoviedb.org/3/movie/" + str(ids['id'])
            params = { 'api_key': api_key , 'language': 'fr-FR' }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                films += [response.json()]
            
        
        
        return jsonify(films)

@app.route('/get_movies_by_vote_average/<vote_average>', methods=['GET', 'POST'])
def get_movies_by_vote_average(vote_average):
        
        url = "https://api.themoviedb.org/3/discover/movie"
        
        params = { 'api_key': api_key , 'language': 'fr-FR' , 'page': 1 , 'sort_by': 'popularity.desc' , 'include_adult': 'false' , 'include_video': 'false' , 'vote_average.gte': vote_average }
        
        response = requests.get(url, headers=headers, params=params)
        
        # If the request was successful, extract the films from the response
        if response.status_code == 200:
            id_films = response.json()["results"]
    
        # Make subsequent requests to get the next 20 films, 40 films, and so on
        for i in range(2, 20, 10):
            params["page"] = i
            response = requests.get(url, params=params)
    
            # If the request was successful, append the films to the list
            if response.status_code == 200:
                id_films += response.json()["results"]
                
        films = []
                
        for ids in id_films:
            url = "https://api.themoviedb.org/3/movie/" + str(ids['id'])
            params = { 'api_key': api_key , 'language': 'fr-FR' }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                films += [response.json()]
            
        
        
        return jsonify(films)

