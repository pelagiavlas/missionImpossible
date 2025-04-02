import pytest
import os
from backend.impo import app, init_db, DB_PATH


@pytest.fixture(scope='module')
def setup_db():
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    init_db()

    yield

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_get_products(client, setup_db):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_product(client, setup_db):
    # Test successful creation
    response = client.post('/products', json={"product_name": "Test Product", "quantity": 10})
    assert response.status_code == 201
    assert response.json['message'] == "Product added successfully"

    # Test missing parameters
    response = client.post('/products', json={"wrong_field": "Test"})
    assert response.status_code == 400


def test_update_product(client, setup_db):
    # First create a product
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})

    # Test successful update
    response = client.put('/products/1', json={"product_name": "Updated Product", "quantity": 20})
    assert response.status_code == 200
    assert response.json['message'] == "Product updated successfully"

    # Test missing parameters
    response = client.put('/products/1', json={"wrong_field": "Test"})
    assert response.status_code == 400


def test_delete_product(client, setup_db):
    # First create a product
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})

    # Test deletion
    response = client.delete('/products/1')
    assert response.status_code == 200
    assert response.json['message'] == "Product deleted successfully"

    # Test deleting non-existent product
    response = client.delete('/products/999')
    assert response.status_code == 404