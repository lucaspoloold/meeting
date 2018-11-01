from flask import Flask
from meeting.ext import db
from meeting.blueprints import restapi


def create_app():
    """Create a new App"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    # Extensão para o banco de dados
    db.configure(app)

    # Blueprint da API
    restapi.configure(app)
    return app
