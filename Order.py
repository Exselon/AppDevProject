import sqlite3

class Order:
    def __init__(self, user_id, product_id, quantity, size,  order_date):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.size = size
        self.order_date = order_date

class OrderManager:
    def __init__(self, db="Order.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    # def checkout(user_id):
    #     conn = sqlite3.connect('Cart.db')
    #     cursor = conn.cursor()
    #
    #     # Retrieve cart items for the user
    #     cursor.execute('SELECT * FROM cart WHERE user_id = ?', (user_id,))
    #     cart_items = cursor.fetchall()
    #
    #     # Insert cart items into the orders table
    #     conn_order = sqlite3.connect('Order.db')
    #     cursor_order = conn_order.cursor()
    #
    #     for item in cart_items:
    #         cursor_order.execute('''
    #             INSERT INTO orders (user_id, product_id, quantity, size, total_price, order_date)
    #             VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    #         ''', (item[1], item[2], item[3], item[4], calculate_total_price(item[2], item[
    #             3])))  # Adjust the total price calculation based on your product prices
    #
    #     conn_order.commit()
    #     conn_order.close()





    def close_connection(self):
        self.conn.close()