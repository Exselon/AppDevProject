import sqlite3


class Product:
    def __init__(self, ProductID,ProductImg,ProductName,ProductPrice,ProductCategory,ProductStock,ProductDescription,ProductSize):
        self.id = ProductID
        self.image_path = ProductImg
        self.name = ProductName
        self.price = ProductPrice
        self.category = ProductCategory
        self.stock = ProductStock
        self.description = ProductDescription
        self.size = ProductSize


class ProductManager:
    def __init__(self, db="Product.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        products_data = self.cursor.fetchall()
        products = [Product(*data) for data in products_data]
        return products

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE ProductID=?", (product_id,))
        product_data = self.cursor.fetchone()
        if product_data:
            return Product(*product_data)
        return None

    def add_product(self, image_path,name,price,category,stock,description,size):
        self.cursor.execute(
            "INSERT INTO products (image, name, price, category, stock,description,size) VALUES (?, ?, ?, ?, ?, ?,?)",
            (image_path,name,price,category,stock,description,size))
        self.conn.commit()

    def get_products_by_category(self, category, price_range=None):
        if price_range:
            query = "SELECT * FROM products WHERE category LIKE ? AND price BETWEEN ? AND ?"
            self.cursor.execute(query, ('%' + category + '%', price_range.split('-')[0], price_range.split('-')[1]))
        else:
            query = "SELECT * FROM products WHERE category LIKE ?"
            self.cursor.execute(query, ('%' + category + '%',))

        products_data = self.cursor.fetchall()
        return [Product(*data) for data in products_data]

    def get_products_by_price(self, price_range):
        query = "SELECT * FROM products WHERE price BETWEEN ? AND ?"
        self.cursor.execute(query, (price_range.split('-')[0], price_range.split('-')[1]))
        products_data = self.cursor.fetchall()
        return [Product(*data) for data in products_data]

    def close_connection(self):
        self.conn.close()
