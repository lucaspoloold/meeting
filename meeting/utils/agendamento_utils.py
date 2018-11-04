def valida_sala(db, sala_id):
    if not db['salas'].find_one({'_id': sala_id, 'ativa': True}):
        raise Exception("A sala informada nao existe")


def valida_sala_livre(db, sala_id, horario):
    if db['agendamentos'].find_one({
            'inicio': {'$lte': horario},
            'fim': {'$gte': horario},
            "sala_id": sala_id}):
        raise Exception("Ja existe reuniao para esta sala neste horario")


def valida_agendamento(db, agendamento):
    valida_sala(db, agendamento['sala_id'])

    valida_sala_livre(db, agendamento['sala_id'], agendamento['inicio'])
    valida_sala_livre(db, agendamento['sala_id'], agendamento['fim'])
