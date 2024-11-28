from datetime import datetime
import sqlite3
import csv

class BookEditor:
    def __init__(self,db) -> None:
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
    
    def add_book(self,isbn,barcode,title,author,publisher,publication_year,category,total_copies,available_copies,language,description,location):
        query = "INSERT INTO books (isbn,barcode,title,author,publisher,publication_year,category,total_copies,available_copies,language,description,location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        self.cursor.execute(query, (isbn,barcode,title,author,publisher,publication_year,category,total_copies,available_copies,language,description,location))
        self.connection.commit()
    
    def edit_book(self, id, column, new_value):
        current_timestamp = datetime.now()
        query = f"UPDATE books SET {column} = ?, updated_at = ? WHERE id = ?"
        self.cursor.execute(query, (new_value,current_timestamp, id))
        self.connection.commit()

    def delete_book(self,id):
        query = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.connection.commit()
    
    def add_data_from_csv(self,output_path):
        with open(output_path, mode='r', encoding="utf-8") as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                try:
                    self.add_book(lines["isbn"],lines["barcode"],lines["title"],lines["author"],lines["publisher"],lines["publication_year"],lines["category"],lines["total_copies"],lines["available_copies"],lines["language"],lines["description"],lines["location"])
                    print(lines["id"],"Added")
                except Exception as e :
                    print(lines["id"],"Error:",e)

    def export_to_csv(self,output_path):
        query = "SELECT * FROM books"
        self.cursor.execute(query)
        column_names = [desc[0] for desc in self.cursor.description[1:]]
        data = [row[1:] for row in self.cursor.fetchall()]
        with open(output_path, "w", newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(data)

