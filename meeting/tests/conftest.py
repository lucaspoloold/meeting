import pytest

from meeting.app import create_app


@pytest.fixture(scope="session")
def app():
    app_obj = create_app()
    app_obj.db['salas'].delete_many({})
    app_obj.db['agendamentos'].delete_many({})

    app_obj.db['salas'].insert_one({'nome': 'Turing', 'capacidade': 20, 'ativa': True})
    sala = app_obj.db['salas'].insert({'nome': 'Ramalho', 'capacidade': 15, 'ativa': True})

    agendamento = {
        'titulo': 'Daily meeting',
        'sala_id': sala.inserted_id,
        'inicio': '2018-12-01 08:00:00',
        'fim': '2018-12-01 08:10:00',
    }

    app_obj.db['agendamentos'].insert_one(agendamento)

    agendamento = {
        'titulo': 'Fechamento mensal',
        'sala_id': sala.inserted_id,
        'inicio': '2018-12-02 08:00:00',
        'fim': '2018-12-02 08:10:00',
    }

    app_obj.db['agendamentos'].insert_one(agendamento)

    yield app_obj

    # app_obj.db['salas'].delete_many({})
    # app_obj.db['agendamentos'].delete_many({})
