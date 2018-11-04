from flask import current_app as app
from flask_restful import Resource


class AgendamentoList(Resource):
    def get(self):
        return {'agendamentos': list(app.db['agendamentos'].find())}
