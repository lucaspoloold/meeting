import pytest

from meeting.app import create_app


@pytest.fixture(scope="module")
def app():
    app_obj = create_app()
    app_obj.db['salas'].delete_many({})

    app_obj.db['salas'].insert_one({'nome': 'Turing', 'capacidade': 20})

    yield app_obj

    app_obj.db['salas'].delete_many({})
