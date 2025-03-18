from flask import Flask, request
import sqlite3

app = Flask(__name__)

DB_path = "impossi.db"
# Database setup
def init_db():
    conn = sqlite3.connect(DB_path)
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
def get_marsProducts():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM marsProducts')
    marsProducts = cursor.fetchall()
    conn.close()
    return marsProducts

# add product to db
def add_product(productName, quantity):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO marsProducts (productName, quantity) VALUES (?, ?)', (productName,quantity))
    conn.commit()
    conn.close()

# update products
def update_product(id, productName, quantity):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE marsProducts SET productName = ?, quantity = ? WHERE id = ?', (productName, quantity, id))
    conn.commit()
    conn.close()

# delete product
def delete_product(id):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM marsProducts WHERE id = ?', (id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

