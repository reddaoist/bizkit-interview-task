from flask import Flask
from flask_mysqldb import MySQL
from .v1 import match, playground, search
import yaml

def create_app():
    
    with open('db.yaml', 'r') as file:
        env = yaml.safe_load(file)
    
    app = Flask(__name__)

    app.config["MYSQL_USER"] = env['mysql']['username']
    app.config["MYSQL_PASSWORD"] = env['mysql']['password']
    app.config["MYSQL_DB"] = env['mysql']['database']
    app.config["MYSQL_HOST"] = env['mysql']['host']

    mysql = MySQL(app)

    @app.route("/")
    def hello():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO test(variable,var_value) VALUES (%s,%s)",("x",10))
        mysql.connection.commit()
        cur.close()
        return "Hello World!"
    
    

    app.register_blueprint(match.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(playground.bp)

    return app
