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

