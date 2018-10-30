from flask import Flask
from meeting.ext import db


def create_app():
    """Create a new App"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    # Extensão para o banco de dados
    db.configure(app)
    return app
