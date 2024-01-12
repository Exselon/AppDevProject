import sqlite3
from Product import ProductManager



class Cart:
    def __init__(self, User_ID, Product_ID, quantity, size):
        self.User_ID = User_ID
        self.Product_ID = Product_ID
        self.quantity = quantity
        self.size = size

class CartManager:
    def __init__(self, db="Cart.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def add_to_cart(self, User_id, Product_id, quantity, size):
        self.cursor.execute(
            "INSERT INTO Cart (user_id, product_id, quantity, size) VALUES (?, ?, ?, ?)",
            (User_id, Product_id, quantity, size))
        self.conn.commit()

    def get_all_cart(self):
        self.cursor.execute("SELECT * FROM cart")
        cart = self.cursor.fetchall()
        return cart

    def get_cart_by_id(self,userid):
        self.cursor.execute("SELECT * FROM cart WHERE user_id =?",(userid,))
        cart = self.cursor.fetchall()
        return cart

    def del_cart(self, cartid):
        self.cursor.execute("DELETE FROM cart WHERE CartID = ?", (cartid,))
        self.conn.commit()


    # def get_cart_data(self, user_id):
    #     self.cursor.execute('''
    #         SELECT products.name, cart.quantity
    #         FROM cart
    #         JOIN products ON cart.Product_ID = "product.db".products.id
    #         WHERE cart.user_id = ?
    #     ''', (user_id,))
    #     cart_data = self.cursor.fetchall()
    #     return cart_data



    # def get_cart_data(self, user_id):
    #     self.cursor.execute('''
    #         SELECT c.User_ID, c.Product_ID, c.quantity, c.size, p.name, p.image_path, p.description, p.price
    #         FROM cart c
    #         JOIN products p ON c.Product_ID = p.id
    #         WHERE c.User_ID = ?
    #     ''', (user_id,))
    #     cart_data = self.cursor.fetchall()
    #     return cart_data






    def close_connection(self):
        self.conn.close()
