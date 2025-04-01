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
            id INTEGER PRIMARY KEY,
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
def add_product(productName, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO marsProducts (productName, quantity) VALUES (?, ?)', (productName,quantity))
    conn.commit()
    conn.close()

# update products
def update_product(id, productName, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE marsProducts SET productName = ?, quantity = ? WHERE id = ?', (productName, quantity, id))
    conn.commit()
    conn.close()

# delete product
def delete_product(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM marsProducts WHERE id = ?', (id))
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
    add_product(data['productName'], data['quantity'])
    return jsonify({"message": "Product added"}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product_route(id):
    data = request.get_json()
    update_product(id, data['productName'], data['quantity'])
    return jsonify({"message": "Product updated"})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product_route(id):
    delete_product(id)
    return jsonify({"message": "Product deleted"})



if __name__ == '__main__':
    init_db()
    app.run(debug=True)


