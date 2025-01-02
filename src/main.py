from PyQt5 import QtWidgets, uic, QtCore
import sys
from BooksEditor import BookEditor
from UsersEditor import UserEditor
import database_setup
from PyQt5.QtWidgets import QLineEdit, QStyledItemDelegate
from PyQt5.QtGui import QIntValidator

class AddBookDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Book")
        
        layout = QtWidgets.QFormLayout()

        self.fields = {
            "ISBN": QtWidgets.QLineEdit(),
            "Barcode": QtWidgets.QLineEdit(),
            "Title": QtWidgets.QLineEdit(),
            "Author": QtWidgets.QLineEdit(),
            "Publisher": QtWidgets.QLineEdit(),
            "Publication Year": QtWidgets.QLineEdit(),
            "Category": QtWidgets.QLineEdit(),
            "Total Copies": QtWidgets.QLineEdit(),
            "Available Copies": QtWidgets.QLineEdit(),
            "Language": QtWidgets.QLineEdit(),
            "Description": QtWidgets.QTextEdit(),
            "Location": QtWidgets.QLineEdit()
        }

        for label, widget in self.fields.items():
            layout.addRow(label, widget)

        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addRow(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return {label: widget.text() if isinstance(widget, QtWidgets.QLineEdit) else widget.toPlainText()
                for label, widget in self.fields.items()}

class AddUserDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add User")
        
        layout = QtWidgets.QFormLayout()

        self.fields = {
            "First Name": QtWidgets.QLineEdit(),
            "Last Name": QtWidgets.QLineEdit(),
            "National ID": QtWidgets.QLineEdit(),
            "Email": QtWidgets.QLineEdit(),
            "Phone": QtWidgets.QLineEdit(),
            "Address": QtWidgets.QLineEdit(),
            "Membership Type": QtWidgets.QLineEdit()
        }

        for label, widget in self.fields.items():
            layout.addRow(label, widget)

        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addRow(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return {label: widget.text() for label, widget in self.fields.items()}

class IntDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QIntValidator())  # Sadece tamsayı
        return editor

class LibraryManagementApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./GUI/main_window.ui", self)
        self.book_editor = BookEditor("db/libary.db")
        self.user_editor = UserEditor("db/libary.db")

        self.booksButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.usersButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.addButton.clicked.connect(self.handle_add_book)
        self.deleteButton.clicked.connect(self.handle_delete_book)
        self.addUserButton.clicked.connect(self.handle_add_user)
        self.deleteUserButton.clicked.connect(self.handle_delete_user)

        self.bookTable.itemChanged.connect(self.handle_table_change)
        self.usersTable.itemChanged.connect(self.handle_table_change)

        self.load_books()
        self.load_users()



        self.booksButton.clicked.connect(self.handle_books_click)
        self.usersButton.clicked.connect(self.handle_users_click)
        
        # Mevcut seçili sayfa indeksini tut
        self.current_index = 0
        
    def handle_books_click(self):
        # Eğer zaten books sayfasındaysak sadece seçili durumu koru
        if self.current_index == 0:
            self.booksButton.setChecked(True)  # Seçili durumu zorla
            return
            
        # Users butonunun seçili durumunu kaldır
        self.usersButton.setChecked(False)
        # Books butonunu seçili yap
        self.booksButton.setChecked(True)
        # Sayfayı değiştir
        self.stackedWidget.setCurrentIndex(0)
        # Mevcut indeksi güncelle
        self.current_index = 0
        
    def handle_users_click(self):
        # Eğer zaten users sayfasındaysak sadece seçili durumu koru
        if self.current_index == 1:
            self.usersButton.setChecked(True)  # Seçili durumu zorla
            return
            
        # Books butonunun seçili durumunu kaldır
        self.booksButton.setChecked(False)
        # Users butonunu seçili yap
        self.usersButton.setChecked(True)
        # Sayfayı değiştir
        self.stackedWidget.setCurrentIndex(1)
        # Mevcut indeksi güncelle
        self.current_index = 1

    def load_books(self):
        delegate = IntDelegate()
        self.bookTable.setItemDelegateForColumn(2, delegate)
        self.bookTable.blockSignals(True)
        self.bookTable.setRowCount(0)
        books = self.book_editor.getdata()
        for book in books:
            row_position = self.bookTable.rowCount()
            self.bookTable.insertRow(row_position)
            for col, data in enumerate(book):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                self.bookTable.setItem(row_position, col, item)
        self.bookTable.blockSignals(False)
    def load_users(self):
        self.usersTable.blockSignals(True)
        self.usersTable.setRowCount(0)
        users = self.user_editor.getdata()
        for user in users:
            row_position = self.usersTable.rowCount()
            self.usersTable.insertRow(row_position)
            for col, data in enumerate(user):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                self.usersTable.setItem(row_position, col, item)
        self.usersTable.blockSignals(False)
    def handle_add_book(self):
        dialog = AddBookDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            book_data = dialog.get_data()
            try:
                self.book_editor.add_book(book_data["ISBN"], book_data["Barcode"], book_data["Title"], \
                                          book_data["Author"], book_data["Publisher"], book_data["Publication Year"], \
                                          book_data["Category"], book_data["Total Copies"], book_data["Available Copies"], \
                                          book_data["Language"], book_data["Description"], book_data["Location"])
                QtWidgets.QMessageBox.information(self, "Add Book", "Book added successfully!")
                self.load_books()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Add Book", f"Error adding book: {str(e)}")

    def handle_delete_book(self):
        selected_row = self.bookTable.currentRow()
        if (selected_row == -1):
            QtWidgets.QMessageBox.warning(self, "Delete Book", "No book selected for deletion.")
            return

        book_id = self.bookTable.item(selected_row, 0).text()
        confirmation = QtWidgets.QMessageBox.question(
            self, "Delete Book", f"Are you sure you want to delete book with ID: {book_id}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            try:
                self.book_editor.delete_book(book_id)
                QtWidgets.QMessageBox.information(self, "Delete Book", "Book deleted successfully!")
                self.load_books()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Delete Book", f"Error deleting book: {str(e)}")
        else:
            QtWidgets.QMessageBox.information(self, "Delete Book", "Deletion canceled.")

    def handle_add_user(self):
        dialog = AddUserDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_data = dialog.get_data()
            try:
                self.user_editor.add_user(user_data["First Name"], user_data["Last Name"], user_data["National ID"], \
                                          user_data["Email"], user_data["Phone"], user_data["Address"], user_data["Membership Type"])
                QtWidgets.QMessageBox.information(self, "Add User", "User added successfully!")
                self.load_users()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Add User", f"Error adding user: {str(e)}")

    def handle_delete_user(self):
        selected_row = self.usersTable.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Delete User", "No user selected for deletion.")
            return

        user_id = self.usersTable.item(selected_row, 0).text()
        confirmation = QtWidgets.QMessageBox.question(
            self, "Delete User", f"Are you sure you want to delete user with ID: {user_id}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            try:
                self.user_editor.delete_user(user_id)
                QtWidgets.QMessageBox.information(self, "Delete User", "User deleted successfully!")
                self.load_users()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Delete User", f"Error deleting user: {str(e)}")
        else:
            QtWidgets.QMessageBox.information(self, "Delete User", "Deletion canceled.")

    def handle_table_change(self, item):
        if item.flags() & QtCore.Qt.ItemIsEditable:
            q = QtWidgets.QMessageBox.question(self, "Edit", "Are you sure you want to edit this item?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if q == QtWidgets.QMessageBox.Yes:
                if self.sender() == self.usersTable:
                    c = self.usersTable.horizontalHeaderItem(item.column()).text().lower().replace(" ", "_")
                    print(self.usersTable.item(item.row(), 0).text(), c, item.text())
                    self.user_editor.edit_user(self.usersTable.item(item.row(), 0).text(),c, item.text())
                if self.sender() == self.bookTable:
                    c = self.bookTable.horizontalHeaderItem(item.column()).text().lower().replace(" ", "_")
                    self.book_editor.edit_book(self.bookTable.item(item.row(), 0).text(), c, item.text())
            else:
                self.load_books()


if __name__ == "__main__":
    database_setup.setup_database("db/libary.db")
    app = QtWidgets.QApplication(sys.argv)
    window = LibraryManagementApp()
    window.show()
    sys.exit(app.exec_())
