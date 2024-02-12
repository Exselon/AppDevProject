import sqlite3

class UserAccount:
    def __init__(self, db="UserData.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def number_exists(self, number):
        self.cursor.execute('SELECT * FROM users WHERE PhoneNumber=?', (number,))
        existing_number = self.cursor.fetchone()
        return existing_number is not None

    def logincheck(self, number):
        self.cursor.execute('SELECT * FROM users WHERE PhoneNumber=?', (number,))
        user = self.cursor.fetchone()
        return user

    def register_user(self, username, password, number, email, dob):
        self.cursor.execute('INSERT INTO users (Username, Password, PhoneNumber, Email, DateOfBirth) VALUES (?, ?, ?, ?, ?)',(username, password, number, email, dob,))
        self.conn.commit()

    def create_admin(self, username, password, number, email, dob,role):
        self.cursor.execute('INSERT INTO users (Username, Password, PhoneNumber, Email, DateOfBirth,Role) VALUES (?, ?, ?, ?, ?,?)',(username, password, number, email, dob,role))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

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

    def update_password(self,new_password,user_id):
        self.cursor.execute("UPDATE users SET Password = ? WHERE UserID = ?", (new_password, user_id))
        self.conn.commit()

    def update_password_by_email(self, random_new_password, email):
        self.cursor.execute("UPDATE users SET Password = ? WHERE email = ?", (random_new_password, email))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()