import sqlite3

class Product:
    def __init__(self, ProductID, ProductName, ProductDetail, ProductPrice, ProductCategory, ProductStock, ProductImg):
        self.id = ProductID
        self.name = ProductName
        self.detail = ProductDetail
        self.price = ProductPrice
        self.category = ProductCategory
        self.stock = ProductStock
        self.image_path = ProductImg

class ProductManager:
    def __init__(self, db="products.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        products_data = self.cursor.fetchall()
        products = [Product(*data) for data in products_data]
        return products

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product_data = self.cursor.fetchone()
        if product_data:
            return Product(*product_data)
        return None

    def add_product(self, name, price, image_path):
        self.cursor.execute("INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
                            (name, price, image_path))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()