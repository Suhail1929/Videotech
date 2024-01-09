import json
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

from user import *
from film import *


if __name__ == '__main__':
    app.run(host='0.0.0.0')
