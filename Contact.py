import sqlite3

class ContactManager:
    def __init__(self, db="Contact.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def Create_Enquiry(self, Name, Email, Subject, Enquiry, Status, ResolveID, Resolveby):
        self.cursor.execute('INSERT INTO Contact (Name, Email, Subject, Enquiry, Status, ResolveID, Resolveby) VALUES (?, ?, ?, ?, ?, ?, ?)',(Name, Email, Subject, Enquiry, Status, ResolveID, Resolveby,))
        self.conn.commit()

    def get_all_enquiry(self):
        self.cursor.execute("SELECT * FROM Contact")
        enquiry_data = self.cursor.fetchall()
        return enquiry_data

    def get_enquiry_by_id(self,ID):
        self.cursor.execute("SELECT * FROM Contact WHERE ID=?",(ID,))
        enquiry_data = self.cursor.fetchall()
        return enquiry_data

    def updated_status(self, adminid, adminname,contact_id):
        self.cursor.execute("UPDATE Contact SET Status='closed', ResolveID=?, Resolveby=? WHERE ID=?", (adminid, adminname, contact_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()