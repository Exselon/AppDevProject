import sqlite3

class DisplayUser:
    def __init__(self, db="UserData.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def get_all_user(self):
        self.cursor.execute("SELECT * FROM users")
        user_data = self.cursor.fetchall()
        return user_data
    def del_user(self,user_id):
        self.id = user_id
        self.cursor.execute("DELETE FROM users WHERE UserID = ?",(user_id,))
        self.conn.commit()

    def get_user_by_id(self,user_id):
        self.cursor.execute("SELECT * FROM users WHERE UserID = ?",(user_id,))
        user_data = self.cursor.fetchall()
        return user_data

    #################INCOMPLETE#########################
    def get_password_by_id(self,user_id):
        self.cursor.execute("SELECT Password FROM users WHERE UserID = ?", (user_id,))
        current_password = self.cursor.fetchone()
        return current_password

    def close_connection(self):
        self.conn.close()