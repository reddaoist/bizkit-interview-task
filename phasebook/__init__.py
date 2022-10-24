from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
import yaml

app = Flask(__name__)
CORS(app)

with open('env-vars.yaml', 'r') as file:
    env = yaml.safe_load(file)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+env['mysql']['username']+':'+env['mysql']['password']+'@'+env['mysql']['host']+'/'+env['mysql']['database']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Hello World!"

from .v1 import match, playground, search
app.register_blueprint(match.bp)
app.register_blueprint(search.bp)
app.register_blueprint(playground.bp)

from .v2 import searchV2
from .v2.playground import usercrud, interestcrud
app.register_blueprint(searchV2.bp)
app.register_blueprint(usercrud.bp)
app.register_blueprint(interestcrud.bp)
