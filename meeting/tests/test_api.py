def test_get_salas(app):
    with app.test_client() as client:
        salas = client.get('/api/sala/')
        assert salas.status_code == 200
        assert 'salas' in salas.json


def test_put_salas(app):
    with app.test_client() as client:
        nova_sala = {
            'nome': 'Currie',
            'capacidade': 10,
        }

        created = client.post('api/sala/', json=nova_sala)
        assert created.status_code == 201
