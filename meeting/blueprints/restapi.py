from flask import Blueprint
from flask import current_app as app
from flask_restful import Api, Resource

bp = Blueprint('restapi', __name__, url_prefix='/api')
api = Api(bp)


class Sala(Resource):
    def get(self):
        return {'salas': list(app.db['salas'].find())}


def configure(app):
    api.add_resource(Sala, '/sala/')
    app.register_blueprint(bp)
