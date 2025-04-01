from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "impossi.db"
# Database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marsProducts (
            product_id INTEGER PRIMARY KEY,
            productName TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# get all the products
def get_mars_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM marsProducts')
    mars_products = cursor.fetchall()
    conn.close()
    return mars_products

# add product to db
def add_product(product_name, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO marsProducts (product_name, quantity) VALUES (?, ?)', (product_name,quantity))
    conn.commit()
    conn.close()

# update products
def update_product(product_id, product_name, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE mars_products SET product_name = ?, quantity = ? WHERE product_id = ?', (product_name, quantity, product_id))
    conn.commit()
    conn.close()

# delete product
def delete_product(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mars_products WHERE product_id = ?', product_id)
    conn.commit()
    conn.close()

# Routes
@app.route('/products', methods=['GET'])
def get_products():
    products = get_mars_products()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    add_product(data['product_name'], data['quantity'])
    return jsonify({"message": "Product added"}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    data = request.get_json()
    update_product(product_id, data['product_name'], data['quantity'])
    return jsonify({"message": "Product updated"})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    delete_product(product_id)
    return jsonify({"message": "Product deleted"})



if __name__ == '__main__':
    init_db()
    app.run(debug=True)


