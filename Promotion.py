import sqlite3

class Promotion:
    def __init__(self,PromoID,PromotionName,PromotionDiscount,PromotionDescription):
        self.__ID = PromoID
        self.__Name = PromotionName
        self.__Discount = PromotionDiscount
        self.__Description = PromotionDescription

class PromotionManager:
    def __init__(self, db="Promotion.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def get_all_promotion(self):
        self.cursor.execute("SELECT * FROM promotions")
        promotion_data = self.cursor.fetchall()
        promotion = [Promotion(*data) for data in promotion_data]
        return promotion

    def add_promotion(self,ID,name,discount,description):
        self.cursor.execute(
            "INSERT INTO promotions (ID,name, discount,description) VALUES (? ,?, ?, ?)",
            (ID,name,discount,description))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

