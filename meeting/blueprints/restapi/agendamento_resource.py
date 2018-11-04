from flask import current_app as app
from flask_restful import Resource, reqparse

agendamento_post_parser = reqparse.RequestParser()
agendamento_post_parser.add_argument('titulo', required=True)
agendamento_post_parser.add_argument('sala_id', required=True)
agendamento_post_parser.add_argument('inicio', required=True)
agendamento_post_parser.add_argument('fim', required=True)


class AgendamentoList(Resource):

    @staticmethod
    def __valida_agendamento(db, agendamento):
        if not db['salas'].find_one({'_id': agendamento['sala_id']}):
            raise Exception("A sala informada nao existe")

        if app.db['agendamentos'].find_one({
                'inicio': {'$lte': agendamento['inicio']},
                'fim': {'$gte': agendamento['inicio']},
                "sala_id": agendamento['sala_id']}):
            raise Exception("Ja existe reuniao para esta sala neste horario")

        if app.db['agendamentos'].find_one({
                'inicio': {'$lte': agendamento['fim']},
                'fim': {'$gte': agendamento['fim']},
                "sala_id": agendamento['sala_id']}):
            raise Exception("Ja existe reuniao para esta sala neste horario")

    def get(self):
        return {'agendamentos': list(app.db['agendamentos'].find())}

    def post(self):
        agendamento = agendamento_post_parser.parse_args()
        try:
            self.__valida_agendamento(app.db, agendamento)
        except Exception as e:
            return {"Agendamento inválido": str(e)}, 409
        else:
            agendamento_novo = app.db['agendamentos'].insert(agendamento)
            return {"agendamento criado": agendamento_novo.inserted_id}, 201
