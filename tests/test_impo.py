import pytest
import os
from src.impo import app, init_db, DB_PATH


@pytest.fixture(scope='module')
def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    init_db()

    yield

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_products(client, setup_db):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_product(client, setup_db):
    response = client.post('/products', json={"product_name": "Test Product", "quantity": 10})
    assert response.status_code == 201
    assert response.json['message'] == "Product added"


def test_update_product(client, setup_db):
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})
    response = client.put('/products/1', json={"product_name": "Updated Product", "quantity": 20})
    assert response.status_code == 200
    assert response.json['message'] == "Product updated"


def test_delete_product(client, setup_db):
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})
    response = client.delete('/products/1')
    assert response.status_code == 200
    assert response.json['message'] == "Product deleted"
