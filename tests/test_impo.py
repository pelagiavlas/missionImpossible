import pytest
import os
import tempfile
from backend.impo import app, init_db, DB_PATH


@pytest.fixture(scope='module')
def setup_db():
    # Δημιουργούμε ένα προσωρινό αρχείο βάσης δεδομένων
    fd, temp_db_path = tempfile.mkstemp()
    os.close(fd)

    # Αλλάζουμε προσωρινά το DB_PATH για τα tests
    original_db_path = DB_PATH
    import backend.impo
    backend.impo.DB_PATH = temp_db_path

    # Αρχικοποιούμε τη βάση
    init_db()

    yield

    # Καθαρισμός
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)
    backend.impo.DB_PATH = original_db_path


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
    # Test επιτυχούς δημιουργίας
    response = client.post('/products', json={"product_name": "Test Product", "quantity": 10})
    assert response.status_code == 201
    assert response.json['message'] == "Product added successfully"

    # Test με λάθος πεδία
    response = client.post('/products', json={"wrong_field": "Test"})
    assert response.status_code == 400


def test_update_product(client, setup_db):
    # Δημιουργούμε πρώτα ένα προϊόν
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})

    # Test επιτυχούς ενημέρωσης
    response = client.put('/products/1', json={"product_name": "Updated Product", "quantity": 20})
    assert response.status_code == 200
    assert response.json['message'] == "Product updated successfully"

    # Test με λάθος πεδία
    response = client.put('/products/1', json={"wrong_field": "Test"})
    assert response.status_code == 400


def test_delete_product(client, setup_db):
    # Δημιουργούμε πρώτα ένα προϊόν
    client.post('/products', json={"product_name": "Test Product", "quantity": 10})

    # Test διαγραφής
    response = client.delete('/products/1')
    assert response.status_code == 200
    assert response.json['message'] == "Product deleted successfully"

    # Test διαγραφής μη υπάρχοντος προϊόντος
    response = client.delete('/products/999')
    assert response.status_code == 404