from datetime import datetime, timedelta
import random
import string
import sqlite3
import csv

def generate_uid(length=5):
    characters = string.ascii_letters + string.digits  
    uid = ''.join(random.choices(characters, k=length))
    return uid

class UserEditor:
    def __init__(self,db) -> None:
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def add_user(self,firstname,lastname,national_id,email,phone,address,type):
        uid = generate_uid()
        current_date = datetime.now()
        future_date = current_date + timedelta(days=365)
        sqlite_date = future_date.strftime("%Y-%m-%d")
        query = "INSERT INTO users (user_id,first_name,last_name,national_id,email,phone,address,membership_expiry,membership_type) VALUES (?,?,?,?,?,?,?,?,?)"
        self.cursor.execute(query, (uid,firstname,lastname,national_id,email,phone,address,sqlite_date,type))
        self.connection.commit()
    
    def delete_user(self,uid):
        query = "DELETE FROM users WHERE uid = ?"
        self.cursor.execute(query, (uid,))
        self.connection.commit()
    
    def edit_user(self,id,column,new_value):
        current_timestamp = datetime.now()
        query = f"UPDATE users SET {column} = ?, updated_at = ? WHERE user_id = ?"
        self.cursor.execute(query, (new_value,current_timestamp, id))
        self.connection.commit()


    def add_data_from_csv(self,path):
        with open(path, mode='r', encoding="utf-8") as file:
            csvFile = csv.DictReader(file)
            print("start")
            for lines in csvFile:
                try:
                    self.add_user(lines["first_name"],lines["last_name"],lines["national_id"],lines["email"],lines["phone"],lines["address"],lines["membership_type"])
                    print(lines["first_name"],"ok")
                except Exception as e :
                    print(lines["first_name"],e)
        
    def export_to_csv(self,path):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        column_names = [desc[0] for desc in self.cursor.description]
        data = self.cursor.fetchall()
        with open(path, "w", newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(data)


