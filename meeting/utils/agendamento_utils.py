from datetime import datetime


def valida_sala(db, sala_id):
    if not db['salas'].find_one({'_id': sala_id, 'ativa': True}):
        raise Exception("A sala informada nao existe")


def valida_sala_livre(db, sala_id, horario, agendamento_id):
    if db['agendamentos'].find_one({
            'inicio': {'$lte': horario},
            'fim': {'$gte': horario},
            "sala_id": sala_id,
            "_id": {"$ne": agendamento_id},
            }):
        raise Exception("Ja existe reuniao para esta sala neste horario")


def valida_datas(agendamento):
    dateformat = "%Y-%m-%dT%H:%M:%S"
    try:
        datetime.strptime(agendamento['inicio'], dateformat)
        datetime.strptime(agendamento['fim'], dateformat)
    except Exception:
        raise Exception("Formato de data/hora invalido (%Y-%m-%dT%H:%M:%S), confira inicio e fim")


def valida_agendamento(db, agendamento, agendamento_id=""):

    valida_datas(agendamento)

    valida_sala(db, agendamento['sala_id'])

    valida_sala_livre(db, agendamento['sala_id'], agendamento['inicio'], agendamento_id)
    valida_sala_livre(db, agendamento['sala_id'], agendamento['fim'], agendamento_id)
