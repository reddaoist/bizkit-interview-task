from flask import Flask
from .v1 import match, playground, search
from . import models

def create_app():
    
    app = Flask(__name__)

    with app.app_context():
        app = models.initialize_db(app)

    @app.route("/")
    def hello():
        return "Hello World!"
    
    app.register_blueprint(match.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(playground.bp)

    return app

