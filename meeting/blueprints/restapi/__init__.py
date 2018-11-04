from flask import Blueprint
from flask_restful import Api

from meeting.blueprints.restapi.agendamento_resource import AgendamentoList
from meeting.blueprints.restapi.sala_resource import SalaList, Sala

bp = Blueprint('restapi', __name__, url_prefix='/api')
api = Api(bp)


def configure(app):
    api.add_resource(SalaList, '/sala/')
    api.add_resource(Sala, '/sala/<sala_id>')
    api.add_resource(AgendamentoList, '/agendamento/')
    app.register_blueprint(bp)
