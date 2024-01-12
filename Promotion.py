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
        return promotion_data


    def add_promotion(self,name,discount,description):
        self.cursor.execute(
            "INSERT INTO promotions (name, discount,description) VALUES (?, ?, ?)",
            (name,discount,description))
        self.conn.commit()

    def del_promotion(self,promotion_id):
        self.id = promotion_id
        self.cursor.execute("DELETE FROM promotions WHERE ID = ?",(promotion_id,))
        self.conn.commit()
        
    def close_connection(self):
        self.conn.close()

