from flask import Flask

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

from user import *
from film import *
from MoviesAPI import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
