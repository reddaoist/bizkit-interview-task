from flask_sqlalchemy import SQLAlchemy
import pymysql
from .v1 import match, playground, search
import yaml


def initialize_db(app):

    with open('db.yaml', 'r') as file:
        env = yaml.safe_load(file)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+env['mysql']['username']+':'+env['mysql']['password']+'@'+env['mysql']['host']+'/'+env['mysql']['database']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db = SQLAlchemy(app)

    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), unique = True, nullable = False)
        age = db.Column(db.Integer, nullable = False)
        occupation = db.Column(db.String(50), nullable = False)

        interests = db.relationship('Interest', backref='user')

       
    class Interest(db.Model):
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
        fav_num = db.Column(db.Integer, nullable = False, primary_key=True)


    db.create_all()

    return app


