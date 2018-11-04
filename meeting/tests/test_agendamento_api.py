def test_recuperar_agendamentos(app):
    with app.test_client() as client:
        agendamentos = client.get('api/agendamento/')
        assert agendamentos.status_code == 200
