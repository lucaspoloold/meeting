from pymongo import MongoClient
from tinymongo import TinyMongoClient


def configure(app):
    if app.env == "production":
        client = MongoClient(host="localhost")
    else:
        client = TinyMongoClient('database')

    db_name = app.config.get('MONGODB_NAME', 'db')
    app.db = client[db_name]