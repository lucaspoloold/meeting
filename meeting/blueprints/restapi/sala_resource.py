from flask import current_app as app
from flask_restful import reqparse, Resource

sala_post_parser = reqparse.RequestParser()
sala_post_parser.add_argument('nome', required=True)
sala_post_parser.add_argument('capacidade', required=True)
sala_post_parser.add_argument('ativa')


class SalaList(Resource):
    def get(self):
        app.logger.info("Buscando todas as salas")
        return {'salas': list(app.db['salas'].find())}

    def post(self):
        sala = sala_post_parser.parse_args()
        nova_sala = app.db['salas'].insert({
            'nome': sala.nome,
            'capacidade': sala.capacidade,
            'ativa': True
        })
        app.logger.info(f"Sala {sala} criada com sucesso")
        return {'sala criada': nova_sala.inserted_id}, 201


class Sala(Resource):

    def put(self, sala_id):
        sala = sala_post_parser.parse_args()
        app.db['salas'].update_one({'_id': sala_id}, {"$set": sala})
        app.logger.info(f"Sala {sala_id} atualizada para {sala}")
        return {'sala atualizada': sala_id}, 200

    def delete(self, sala_id):
        '''Irá excluir a sala de maneira lógica'''
        app.db['salas'].update_one({'_id': sala_id}, {"$set": {"ativa": False}})
        app.logger.info(f"Sala {sala_id} excluida")
        return {'sala excluida': sala_id}, 200
