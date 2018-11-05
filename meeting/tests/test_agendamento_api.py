def test_recuperar_agendamentos(app):
    with app.test_client() as client:
        agendamentos = client.get('api/agendamento/')
        assert agendamentos.status_code == 200


def test_inserir_agendamento(app):
    sala = app.db['salas'].find_one({"ativa": True})
    agendamento = {
        'titulo': 'Weekly meeting',
        'sala_id': sala['_id'],
        'inicio': '2018-12-02 08:00:00',
        'fim': '2018-12-02 08:10:00',
    }

    with app.test_client() as client:
        novo_agendamento = client.post('api/agendamento/', json=agendamento)
        assert novo_agendamento.status_code == 201


def test_inserir_agendamento_sala_nao_existente(app):
    agendamento = {
        'titulo': 'Weekly meeting',
        'sala_id': 123,
        'inicio': '2018-12-02 08:00:00',
        'fim': '2018-12-02 08:10:00',
    }

    with app.test_client() as client:
        novo_agendamento = client.post('api/agendamento/', json=agendamento)
        assert novo_agendamento.status_code == 409


def test_inserir_agendamento_mesmo_horario(app):
    sala = app.db['salas'].find_one({"ativa": True})
    agendamento = {
        'titulo': 'Simple meeting',
        'sala_id': sala['_id'],
        'inicio': '2018-12-02 08:00:00',
        'fim': '2018-12-02 08:10:00',
    }

    with app.test_client() as client:
        novo_agendamento = client.post('api/agendamento/', json=agendamento)
        assert novo_agendamento.status_code == 409

        agendamento['inicio'] = '2018-12-02 07:00:00'
        novo_agendamento = client.post('api/agendamento/', json=agendamento)
        assert novo_agendamento.status_code == 409

        agendamento['inicio'] = '2018-12-02 08:05:00'
        novo_agendamento = client.post('api/agendamento/', json=agendamento)
        assert novo_agendamento.status_code == 409


def test_atualizar_agendamento(app):
    agendamento = app.db['agendamentos'].find_one({})
    agendamento['inicio'] = "2018-12-03 08:00:00"
    agendamento['fim'] = "2018-12-03 08:20:00"

    with app.test_client() as client:
        agendamento_atualizado = client.put(f"api/agendamento/{agendamento['_id']}", json=agendamento)
        assert agendamento_atualizado.status_code == 200

        agendamento['inicio'] = "2018-12-03 08:10:00"
        agendamento_atualizado = client.put(f"api/agendamento/{agendamento['_id']}", json=agendamento)
        assert agendamento_atualizado.status_code == 200


def test_atualizar_agendamento_em_horario_ocupado(app):
    agendamento = app.db['agendamentos'].find_one({})
    agendamento['inicio'] = "2018-12-02 08:00:00"
    agendamento['fim'] = "2018-12-02 08:20:00"

    with app.test_client() as client:
        agendamento_atualizado = client.put(f"api/agendamento/{agendamento['_id']}", json=agendamento)
        assert agendamento_atualizado.status_code == 409
