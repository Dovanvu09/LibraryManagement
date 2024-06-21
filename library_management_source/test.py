
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QDateEdit, QFormLayout, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate, QDateTime
import sys
import psycopg2
import uuid

style_sheet = """
QPushButton {
    background-color: #2E2E2E;
    color: white;
    border: none;
    padding: 5px 12px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 12px;
    margin: 2px 1px;
    cursor: pointer;
    border-radius: 4px;
}
QPushButton:checked {
    background-color: #5E5E5E;
    color: white;
}
QPushButton:hover {
    background-color: #0099FF;
}
"""

class OrderWindow(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Order Books")
        self.setupOrderTab()
        self.show()

    def setupOrderTab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Order Books")
        title_label.setFont(QFont("Arial", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.order_table = QTableWidget(0, 8)
        self.order_table.setHorizontalHeaderLabels(["Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category", "Quantity"])
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Mock data to fill the order table
        self.load_mock_data()

        self.order_date_edit = QDateEdit()
        self.order_date_edit.setCalendarPopup(True)
        self.order_date_edit.setDate(QDate.currentDate())

        self.deadline_edit = QLineEdit()
        self.deadline_edit.setPlaceholderText("Enter deadline (YYYY-MM-DD)")

        order_button = QPushButton("Order")
        order_button.clicked.connect(self.create_orderline)

        form_layout = QFormLayout()
        form_layout.addRow("Order Date:", self.order_date_edit)
        form_layout.addRow("Deadline:", self.deadline_edit)

        layout.addWidget(title_label)
        layout.addWidget(self.order_table)
        layout.addLayout(form_layout)
        layout.addWidget(order_button, alignment=Qt.AlignmentFlag.AlignRight)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_mock_data(self):
        mock_data = [
            ["0040A8", "Introduction to Surface", "Russell Marshall", "Flowers PLC", "Korea", "2007-07-26", "Coursebooks", "1"],
            ["00EYIZ", "Utilize best-of-breed networks", "Carolyn Hamilton", "Cole, Taylor and Lop", "Italy", "2006-03-20", "Children's books", "1"]
        ]
        for row_data in mock_data:
            row_position = self.order_table.rowCount()
            self.order_table.insertRow(row_position)
            for column, item in enumerate(row_data):
                self.order_table.setItem(row_position, column, QTableWidgetItem(str(item)))

    def create_orderline(self):
        user_id = self.get_user_id(self.user_info['email'])
        if not user_id:
            QMessageBox.warning(self, "Error", "User ID not found for the given email.")
            return

        orderline_id = str(uuid.uuid4())[:5]
        order_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        expiration_date = self.deadline_edit.text()
        status = "In queue"
        extension = None
        method = "Online"
        violation = None

        connection = None
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO orderline (orderline_id, student_id, order_time, expiration_date, deadline, extension, status, book_return_date, method, violation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, %s, %s)
            """
            cursor.execute(insert_query, (orderline_id, user_id, order_time, expiration_date, expiration_date, extension, status, method, violation))
            connection.commit()

            QMessageBox.information(self, "Success", "Orderline created successfully!")

        except (Exception, psycopg2.Error) as error:
            QMessageBox.warning(self, "Error", f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_user_id(self, email):
        connection = None
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT student_id FROM student WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                cursor.execute("SELECT librarian_id FROM librarian WHERE email = %s", (email,))
                result = cursor.fetchone()
                return result[0] if result else None
        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    user_info = {
        'email': 'example@sis.hust.edu.vn'
    }
    window = OrderWindow(user_info)
    sys.exit(app.exec())