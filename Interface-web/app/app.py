from flask import Flask

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
api_url = "http://10.11.5.145:5100"

from routes.api import *
from routes.web import *

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    



