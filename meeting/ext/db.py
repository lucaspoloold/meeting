from pymongo import MongoClient
from tinydb_serialization import SerializationMiddleware
from tinymongo import TinyMongoClient
from tinymongo.serializers import DateTimeSerializer


class CustomClient(TinyMongoClient):
    @property
    def _storage(self):
        serialization = SerializationMiddleware()
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

        return serialization


def configure(app):
    if app.env == "production":
        client = MongoClient(host="localhost")
    else:
        client = CustomClient('database')

    db_name = app.config.get('MONGODB_NAME', 'db')
    app.db = client[db_name]
