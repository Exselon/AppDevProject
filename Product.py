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

    def get_products_by_category(self, price_range=None, category_conditions=None, category_conditions_params=None):
        if category_conditions and price_range:
            query = f"SELECT * FROM products WHERE {category_conditions} AND price BETWEEN ? AND ?"
            params = category_conditions_params + [price_range.split('-')[0], price_range.split('-')[1]]
            self.cursor.execute(query, tuple(params))
        elif category_conditions:
            query = f"SELECT * FROM products WHERE {category_conditions}"
            if category_conditions_params:
                self.cursor.execute(query, tuple(category_conditions_params))
            else:
                self.cursor.execute(query)
        elif price_range:
            query = "SELECT * FROM products WHERE price BETWEEN ? AND ?"
            self.cursor.execute(query, (price_range.split('-')[0], price_range.split('-')[1]))
        else:
            query = "SELECT * FROM products"
            self.cursor.execute(query)

        products_data = self.cursor.fetchall()
        return [Product(*data) for data in products_data]

    def del_product(self,ID):
        self.cursor.execute('DELETE FROM products WHERE ProductID=?', (ID,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
