def test_get_salas(app):
    with app.test_client() as client:
        result = client.get('/api/sala/')
        assert result.status_code == 200
