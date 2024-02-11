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

    def update_cart_quantity(self, cart_id, new_quantity):
        # Check if the cart item with the given cart_id exists
        try:
            if new_quantity < 1:
                print(f"Validation error: Cannot decrement below 1 for CartID {cart_id}")
                return

            self.cursor.execute('SELECT * FROM cart WHERE CartID = ?', (cart_id,))
            cart_item = self.cursor.fetchone()

            if cart_item:
                # Update the quantity for the cart item
                self.cursor.execute('UPDATE cart SET quantity = ? WHERE CartID = ?', (new_quantity, cart_id))
                self.conn.commit()
                print(f"Quantity updated for CartID {cart_id} to {new_quantity}")
            else:
                print(f"Cart item with CartID {cart_id} not found.")
        finally:
            self.conn.close()

    def get_cart_item_by_id(self, cart_id):
        self.cursor.execute("SELECT * FROM cart WHERE CartID = ?",(cart_id,))
        cart_item = self.cursor.fetchone()

        return cart_item

    def get_current_quantity(self, cart_id):
        # Retrieve the current quantity from the database
        self.cursor.execute('SELECT quantity FROM cart WHERE CartID = ?', (cart_id,))
        result = self.cursor.fetchone()

        self.conn.close()

        if result:
            return result[0]
        else:
            # Return 0 if the cart item is not found
            return 0


    def close_connection(self):
        self.conn.close()
