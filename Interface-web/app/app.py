from flask import Flask
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

ip = "10.11.5.145"


api_url = "http://"+ip+":5100"

print("API URL:", api_url)

from routes.api import *
from routes.web import *

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    



