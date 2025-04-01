# Module docstring
"""
This module provides a simple Flask API for managing products in a Mars Products database.
It allows users to create, read, update, and delete products from the database.
"""
import sqlite3
from flask import Flask, request, jsonify


app = Flask(__name__)

DB_PATH = "impossi.db"

# Database setup
def init_db():
    """Initializes the database by creating the table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mars_products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Get all the products
def get_mars_products():
    """Fetches all products from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mars_products')
    mars_products = cursor.fetchall()
    conn.close()
    return mars_products

# Add product to db
def add_product(product_name, quantity):
    """Adds a new product to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'INSERT INTO mars_products (product_name, quantity) VALUES (?, ?)'
    values = (product_name, quantity)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# Update product in db
def update_product(product_id, product_name, quantity):
    """Updates an existing product in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'UPDATE mars_products SET product_name = ?, quantity = ? WHERE product_id = ?'
    values = (product_name, quantity, product_id)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# Delete product from db
def delete_product(product_id):
    """Deletes a product from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mars_products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

# Routes
@app.route('/products', methods=['GET'])
def get_products():
    """Handles GET requests to fetch all products."""
    products = get_mars_products()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    """Handles POST requests to create a new product."""
    data = request.get_json()
    add_product(data['product_name'], data['quantity'])
    return jsonify({"message": "Product added"}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    """Handles PUT requests to update an existing product."""
    data = request.get_json()
    update_product(product_id, data['product_name'], data['quantity'])
    return jsonify({"message": "Product updated"})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    """Handles DELETE requests to delete a product."""
    delete_product(product_id)
    return jsonify({"message": "Product deleted"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

