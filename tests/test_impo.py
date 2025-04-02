import pytest
import os
import tempfile
from backend.impo import app, init_db, DB_PATH


@pytest.fixture(scope='module')
def setup_db():
    # Use a temporary directory for tests
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test.db')

    # Set the DB_PATH for testing
    os.environ['TESTING'] = 'true'
    from backend.impo import DB_PATH as original_db_path
    original_db_path = test_db_path  # Override the path

    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    init_db()

    yield

    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    os.environ.pop('TESTING', None)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_get_products(client, setup_db):
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json == []


def test_create_product(client, setup_db):
    # Test successful creation
    response = client.post('/products', json={"product_name": "Test Product", "quantity": 10})
    assert response.status_code == 201

    # Verify the product was actually created
    response = client.get('/products')
    assert len(response.json) == 1
    assert response.json[0]['product_name'] == "Test Product"
    assert response.json[0]['quantity'] == 10


def test_update_product(client, setup_db):
    # Create a product first
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})

    # Update the product
    response = client.put('/products/1', json={"product_name": "Updated Product", "quantity": 20})
    assert response.status_code == 200

    # Verify the update
    response = client.get('/products')
    assert response.json[0]['product_name'] == "Updated Product"
    assert response.json[0]['quantity'] == 20


def test_delete_product(client, setup_db):
    # Create a product first
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})

    # Delete the product
    response = client.delete('/products/1')
    assert response.status_code == 200

    # Verify deletion
    response = client.get('/products')
    assert response.json == []