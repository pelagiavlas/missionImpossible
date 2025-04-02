"""
Mars Products API

This module provides a RESTful API for managing products in a Mars Products database.
It allows CRUD operations (Create, Read, Update, Delete) for products.
"""

import os
import sqlite3
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configuration
UI_FOLDER = os.path.join(os.getcwd(), 'ui')
DB_PATH = "/impossi.db"

# Set static folder properly using Flask's public interface
app.static_folder = os.path.join(UI_FOLDER, 'static')


def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Initialize the database by creating the table if it doesn't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mars_products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        conn.commit()


def get_mars_products():
    """Fetch all products from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mars_products')
        return cursor.fetchall()


def add_product(product_name, quantity):
    """Add a new product to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO mars_products (product_name, quantity) VALUES (?, ?)',
            (product_name, quantity)
        )
        conn.commit()


def update_product(product_id, product_name, quantity):
    """Update an existing product in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE mars_products SET product_name = ?, quantity = ? WHERE product_id = ?',
            (product_name, quantity, product_id)
        )
        conn.commit()


def delete_product(product_id):
    """Delete a product from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM mars_products WHERE product_id = ?',
            (product_id,)
        )
        conn.commit()


@app.route('/')
def index():
    """Serve the main index.html page."""
    return send_from_directory('/app/ui', 'index.html')


@app.route('/products', methods=['GET'])
def get_products():
    """Handle GET requests to fetch all products."""
    products = get_mars_products()
    return jsonify(products)


@app.route('/products', methods=['POST'])
def create_product():
    """Handle POST requests to create a new product."""
    data = request.get_json()

    if not data or 'product_name' not in data or 'quantity' not in data:
        return jsonify({"error": "Product name and quantity are required"}), 400

    add_product(data['product_name'], data['quantity'])
    return jsonify({"message": "Product added successfully"}), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    """Handle PUT requests to update an existing product."""
    data = request.get_json()

    if not data or 'product_name' not in data or 'quantity' not in data:
        return jsonify({"error": "Product name and quantity are required"}), 400

    update_product(product_id, data['product_name'], data['quantity'])
    return jsonify({"message": "Product updated successfully"})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    """Handle DELETE requests to delete a product."""
    delete_product(product_id)
    return jsonify({"message": "Product deleted successfully"})


@app.after_request
def after_request(response):
    """Add CORS headers to every response."""
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)