def test_404(app):
    with app.test_client() as client:
        result = client.get('/')
        assert result.status_code == 404
