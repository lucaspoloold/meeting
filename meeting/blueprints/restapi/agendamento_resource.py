from flask import current_app as app
from flask_restful import Resource, reqparse

from meeting.utils.agendamento_utils import valida_agendamento

agendamento_post_parser = reqparse.RequestParser()
agendamento_post_parser.add_argument('titulo', required=True)
agendamento_post_parser.add_argument('sala_id', required=True)
agendamento_post_parser.add_argument('inicio', required=True)
agendamento_post_parser.add_argument('fim', required=True)


class AgendamentoList(Resource):

    def get(self):
        app.logger.info("Buscando todos os agendamentos")
        return {'agendamentos': list(app.db['agendamentos'].find())}

    def post(self):
        agendamento = agendamento_post_parser.parse_args()
        try:
            valida_agendamento(app.db, agendamento)
        except Exception as e:
            app.logger.info(f"Agendamento inválido: {e} - Request {agendamento}")
            return {"Agendamento inválido": str(e)}, 409
        else:
            agendamento_novo = app.db['agendamentos'].insert(agendamento)
            app.logger.info(f"Agendamento {agendamento} criado com sucesso: {agendamento_novo.inserted_id}")
            return {"agendamento criado": agendamento_novo.inserted_id}, 201


class Agendamento(Resource):

    def get(self, agendamento_id):
        agendamento = app.db['agendamentos'].find_one({"_id": agendamento_id})
        if agendamento:
            return agendamento, 200
        else:
            return "Registro nao encontrado", 404

    def put(self, agendamento_id):
        agendamento = agendamento_post_parser.parse_args()

        try:
            valida_agendamento(app.db, agendamento, agendamento_id)
        except Exception as e:
            app.logger.info(f"Agendamento inválido: {e} - Request {agendamento}")
            return {"Agendamento inválido": str(e)}, 409
        else:
            app.db['agendamentos'].update_one({'_id': agendamento_id}, {'$set': agendamento})
            app.logger.info(f"Agendamento {agendamento_id} atualizada para {agendamento}")
            return {'agendamento atualizado': agendamento_id}, 200

    def delete(self, agendamento_id):
        app.db['agendamentos'].delete_one({'_id': agendamento_id})
        app.logger.info(f"Agendamento {agendamento_id} excluido")
        return {'agendamento excluido': agendamento_id}, 200
