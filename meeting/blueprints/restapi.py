from flask import Blueprint
from flask import current_app as app
from flask_restful import Api, Resource, reqparse

bp = Blueprint('restapi', __name__, url_prefix='/api')
api = Api(bp)

sala_post_parser = reqparse.RequestParser()
sala_post_parser.add_argument('nome', required=True)
sala_post_parser.add_argument('capacidade', required=True)


class Sala(Resource):
    def get(self):
        return {'salas': list(app.db['salas'].find())}

    def post(self):
        sala = sala_post_parser.parse_args()
        nova_sala = app.db['salas'].insert({'nome': sala.nome, 'capacidade': sala.capacidade})
        return {'sala criada': nova_sala.inserted_id}, 201


def configure(app):
    api.add_resource(Sala, '/sala/')
    app.register_blueprint(bp)
