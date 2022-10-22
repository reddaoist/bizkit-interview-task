from dataclasses import dataclass
from . import db,app

@dataclass
class User(db.Model):
    id: int
    name: str
    age: int
    occupation: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    occupation = db.Column(db.String(50), nullable = False)

    interests = db.relationship('Interest', backref='user')

@dataclass       
class Interest(db.Model):
    user_id: int
    fav_num: int
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    fav_num = db.Column(db.Integer, nullable = False, primary_key=True)
    
with app.app_context():        
    db.create_all()
