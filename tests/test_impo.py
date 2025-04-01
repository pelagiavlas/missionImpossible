import pytest
from impo import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200

def test_create_product(client):
    response = client.post('/products', json={"productName": "Test Product", "quantity": 10})
    assert response.status_code == 201


