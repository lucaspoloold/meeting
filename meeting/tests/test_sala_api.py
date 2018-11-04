def test_recuperar_salas(app):
    with app.test_client() as client:
        salas = client.get('/api/sala/')
        assert salas.status_code == 200
        assert 'salas' in salas.json


def test_inserir_sala(app):
    with app.test_client() as client:
        nova_sala = {
            'nome': 'Currie',
            'capacidade': 10,
        }

        created = client.post('api/sala/', json=nova_sala)
        assert created.status_code == 201


def test_atualizar_sala_existente(app):
    registro = app.db['salas'].find_one({})
    with app.test_client() as client:
        updated = client.put(f"api/sala/{registro['_id']}", json={
            'nome': registro['nome'],
            'capacidade': 40,
        })

        registro_atualizado = app.db['salas'].find_one({"_id": registro["_id"]})

        assert updated.status_code == 200
        assert registro_atualizado['capacidade'] == '40'


def test_apagar_sala(app):
    registro = app.db['salas'].find_one({})
    with app.test_client() as client:
        deleted = client.delete(f"api/sala/{registro['_id']}")

        assert deleted.status_code == 200
        sala_excluida = app.db['salas'].find_one({'_id': registro['_id']})
        assert not sala_excluida['ativa']
