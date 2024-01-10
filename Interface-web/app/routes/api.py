from app import app , api_url
import json
import os
import requests
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required , get_username


def validate_login(user):

    # Requête HTTP vers votre API pour valider le login
    response = requests.post(f"{api_url}/validate_login", json=user)

    # Si la requête est réussie (code 200) et le résultat est True, retournez True
    if response.status_code == 200 and response.json().get("result") == True:
        return True
    return False

# [--- Flask Factories  ---]
messages = {
    "login_success": Message("Bienvenue!", "success"),
    "is_logged_in": Message("Vous êtes déjà connecté", "success"),
    "logout": None,
    "login_failure": Message("Mauvais nom d'utilisateur ou mot de passe", "danger"),
    "login_required": Message("Vous devez d'abord vous connecter", "warning"),
}
SimpleLogin(app, login_checker=validate_login, messages=messages)
