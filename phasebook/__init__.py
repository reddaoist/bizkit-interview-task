from flask import Flask

from . import match, search, crud


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"

    app.register_blueprint(match.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(crud.bp)

    return app
