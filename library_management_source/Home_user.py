
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QFont, QIcon, QAction
from PyQt6.QtCore import Qt, QSize, QDate, QDateTime
import sys
import psycopg2
import uuid

style_sheet = """
QRadioButton{
    background-color: #FCF9F3;
}
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
QPushButton:hover{
    background-color: #0099FF;
}
"""

class HomeWindow_user(QMainWindow):
    def __init__(self,user_info):
        super().__init__()
        self.selected_data = []
        self.user_info = user_info
        self.initializeUI()
        self.show()
    def initializeUI(self):
        self.setGeometry(100, 100, 750, 550)
        self.setupTabAndLayout()
        # self.show()

    def setupTabAndLayout(self):
        self.stacked_widget = QStackedWidget()  # QStackedWidget để chứa các widget

        self.home_tab = QTabWidget()
        self.home_tab.setObjectName("Tabs")
        self.home_page = QWidget()
        self.home_page.setObjectName("Home")
        self.Order_tab = QWidget()  # Khởi tạo thuộc tính Order_tab
        self.Order_tab.setObjectName("Order")

        self.pending_books_page = QWidget()
        self.borrowed_books_page = QWidget()
        self.returned_books_page = QWidget()
        self.overdue_page = QWidget()
        self.information_page = QWidget()
        self.event_page = QWidget()
        self.logout_page = QWidget()

        self.HomeTab()
        self.pending_books()
        self.borrowed_books()
        self.returned_books()
        self.overdue_books()
        self.EventTab() 
        self.information_tab()

        side_menu = QWidget()
        side_menu.setObjectName("Tabs")
        side_menu.setFixedWidth(150)
        side_menu.setStyleSheet("background-color: #2E2E2E; color: White;")

        side_layout = QVBoxLayout()
        user_image = self.loadImage("D:\\test\\PyQt\\user3.jpg")
        side_layout.addWidget(user_image)

        buttons = ["Home", "Pending Books", "Borrowed Books", "Returned Books", "Overdue","Event", "Information", "Log out"]
        for i, text in enumerate(buttons):
            btn = QToolButton()
            btn.setText(text)
            btn.setFixedWidth(120)
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #2E2E2E;
                    color: white;
                    border: 5px;
                    padding: 20px;
                    text-align: left;
                }
                QToolButton:hover {
                    background-color: #3E3E3E;
                }
            """)
            btn.clicked.connect(lambda checked, index=i: self.switch_widget(index))
            side_layout.addWidget(btn)
        side_menu.setLayout(side_layout)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(side_menu)
        main_h_box.addWidget(self.stacked_widget)  # Thêm QStackedWidget vào layout chính

        central_widget = QWidget()
        central_widget.setLayout(main_h_box)
        self.setCentralWidget(central_widget)
    def EventTab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Events")
        title_label.setFont(QFont("Arial", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.event_table = QTableWidget(0, 8)
        self.event_table.setHorizontalHeaderLabels(["Name", "Organiser", "Sponsor", "Description", "Destination", "Target Participant", "Date", "Schedule"])
        self.event_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_events()

        layout.addWidget(title_label)
        layout.addWidget(self.event_table)

        container = QWidget()
        container.setLayout(layout)
        self.event_page.setLayout(layout)
        self.stacked_widget.addWidget(self.event_page)
    def load_events(self):
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

            query = "SELECT name, organiser, sponsor, description, destination, target_participant, date, schedule FROM special_event"
            cursor.execute(query)
            rows = cursor.fetchall()

            self.event_table.setRowCount(0)  # Clear any existing rows

            for row in rows:
                row_position = self.event_table.rowCount()
                self.event_table.insertRow(row_position)
                for column, item in enumerate(row):
                    self.event_table.setItem(row_position, column, QTableWidgetItem(str(item)))

        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()


    def overdue_books(self):
        layout = QVBoxLayout()

        title_label = QLabel("Overdue Books")
        title_label.setFont(QFont("Arial", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.overdue_books_table = QTableWidget(0, 7)
        self.overdue_books_table.setHorizontalHeaderLabels(["Order ID", "Student ID", "Order Time", "Expiration Date", "Status", "Method","Violation"])
        self.overdue_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_overdue_books()

        layout.addWidget(title_label)
        layout.addWidget(self.overdue_books_table)

        self.overdue_page.setLayout(layout)
        self.stacked_widget.addWidget(self.overdue_page)
    def load_overdue_books(self):
        user_id = self.get_user_id(self.user_info['email'])
        if not user_id:
            QMessageBox.warning(self, "Error", "User ID not found for the given email.")
            return

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

            query = """
                SELECT orderline_id, student_id, order_time, expiration_date, status, method, violation
                FROM orderline 
                WHERE violation = 'X' AND student_id = %s
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            self.overdue_books_table.setRowCount(0)  # Clear any existing rows

            for row in rows:
                row_position = self.overdue_books_table.rowCount()
                self.overdue_books_table.insertRow(row_position)
                for column, item in enumerate(row):
                    self.overdue_books_table.setItem(row_position, column, QTableWidgetItem(str(item)))

        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()
            

    def borrowed_books(self):
        layout = QVBoxLayout()

        title_label = QLabel("Borrowed Books")
        title_label.setFont(QFont("Arial", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.borrowed_books_table = QTableWidget(0, 6)
        self.borrowed_books_table.setHorizontalHeaderLabels(["Order ID", "Student ID", "Order Time", "Expiration Date", "Status", "Method"])
        self.borrowed_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_borrowed_books()

        layout.addWidget(title_label)
        layout.addWidget(self.borrowed_books_table)

        self.borrowed_books_page.setLayout(layout)
        self.stacked_widget.addWidget(self.borrowed_books_page)

    def pending_books(self):
        layout = QVBoxLayout()

        title_label = QLabel("Pending Books")
        title_label.setFont(QFont("Arial",20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pending_books_table = QTableWidget(0,5)
        self.pending_books_table.setHorizontalHeaderLabels(["Orderline_id","Student_ID","Order Time","Expiration Date", "Status", "Method"])
        self.pending_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_pending_books()
        layout.addWidget(title_label)
        layout.addWidget(self.pending_books_table)

        self.pending_books_page.setLayout(layout)
        self.stacked_widget.addWidget(self.pending_books_page)
    def returned_books(self):
        layout = QVBoxLayout()

        title_label = QLabel("Returned Books")
        title_label.setFont(QFont("Arial", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.returned_books_table = QTableWidget(0, 6)
        self.returned_books_table.setHorizontalHeaderLabels(["Order ID", "Student ID", "Order Time", "Expiration Date", "Status", "Method"])
        self.returned_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_returned_books()

        layout.addWidget(title_label)
        layout.addWidget(self.returned_books_table)
        self.returned_books_page.setLayout(layout)
        self.stacked_widget.addWidget(self.returned_books_page)

    def load_returned_books(self):
        user_id = self.get_user_id(self.user_info['email'])
        if not user_id:
            QMessageBox.warning(self, "Error", "User ID not found for the given email.")
            return

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

            query = """
                SELECT orderline_id, student_id, order_time, expiration_date, status, method 
                FROM orderline 
                WHERE status = 'Returned' AND student_id = %s
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            self.returned_books_table.setRowCount(0)  # Clear any existing rows

            for row in rows:
                row_position = self.returned_books_table.rowCount()
                self.returned_books_table.insertRow(row_position)
                for column, item in enumerate(row):
                    self.returned_books_table.setItem(row_position, column, QTableWidgetItem(str(item)))

        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()
    def load_borrowed_books(self):
        user_id = self.get_user_id(self.user_info['email'])
        if not user_id:
            QMessageBox.warning(self, "Error", "User ID not found for the given email.")
            return

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

            query = """
                SELECT orderline_id, student_id, order_time, expiration_date, status, method 
                FROM orderline 
                WHERE status = 'Successful' AND student_id = %s
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            self.borrowed_books_table.setRowCount(0)  # Clear any existing rows

            for row in rows:
                row_position = self.borrowed_books_table.rowCount()
                self.borrowed_books_table.insertRow(row_position)
                for column, item in enumerate(row):
                    self.borrowed_books_table.setItem(row_position, column, QTableWidgetItem(str(item)))

        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def load_pending_books(self):
        user_id = self.get_user_id(self.user_info['email'])
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

            query = """
                SELECT orderline_id, student_id, order_time, expiration_date, status, method 
                FROM orderline 
                WHERE status IN ('In queue', 'Accepted') and student_id = %s
            """
            cursor.execute(query,(user_id,))
            rows = cursor.fetchall()

            self.pending_books_table.setRowCount(0)  # Clear any existing rows

            for row in rows:
                row_position = self.pending_books_table.rowCount()
                self.pending_books_table.insertRow(row_position)
                for column, item in enumerate(row):
                    self.pending_books_table.setItem(row_position, column, QTableWidgetItem(str(item)))

        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def information_tab(self):
        info_label = QLabel(
        f"User Information:\n\n"
        f"Email: {self.user_info['email']}\n"
        f"First Name: {self.user_info['first_name']}\n"
        f"Last Name: {self.user_info['last_name']}\n"
        f"DOB: {self.user_info['dob']}\n"
        f"Gender: {self.user_info['gender']}\n"
        # f"Phone Number: {self.user_info['phone_number']}\n"
        )

        info_label.setObjectName("Header")

        page3_v_box = QVBoxLayout()
        page3_v_box.addWidget(info_label)
        page3_v_box.addStretch(1)

        self.information_page.setLayout(page3_v_box)
        self.stacked_widget.addWidget(self.information_page)

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

    def switch_widget(self, index):
        if index == 7:
            self.close()
        else:
            self.stacked_widget.setCurrentIndex(index)

    def HomeTab(self):
        # Search Block
        search_box_label = QLabel("SEARCH FOR BOOK")
        search_box_label.setObjectName("Header")
        search_box = QWidget()
        self.search_button = QPushButton("Search")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Please enter")

        h_box_search = QHBoxLayout()
        h_box_search.addWidget(self.search_button)
        h_box_search.addWidget(self.search_input)
        search_box.setLayout(h_box_search)

        search_title = QGroupBox()
        self.title_group = QButtonGroup()
        v_box_title = QVBoxLayout()
        search_list = ["Book ID", "Name", "Publisher", "Category"]

        for ls in search_list:
            ls_rb = QRadioButton(ls)
            v_box_title.addWidget(ls_rb)
            self.title_group.addButton(ls_rb)
        search_title.setLayout(v_box_title)
        self.search_button.clicked.connect(self.search_book)

        # Result Block
        self.result_table = QTableWidget(0, 8)
        self.result_table.setHorizontalHeaderLabels(["Select", "Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_order_button = QPushButton("Add to Cart")
        self.add_order_button.clicked.connect(self.process_selected_data)

        page1_v_box = QVBoxLayout()
        page1_v_box.addWidget(search_box_label)
        page1_v_box.addWidget(search_box)
        page1_v_box.addWidget(search_title)
        page1_v_box.addWidget(self.result_table)
        page1_v_box.addWidget(self.add_order_button, alignment=Qt.AlignmentFlag.AlignRight)
        page1_v_box.addStretch(1)

        self.home_page.setLayout(page1_v_box)
        self.home_tab.addTab(self.home_page, "Home")

        self.OrderTab()  # Thêm trang Order vào home_tab
        self.home_tab.addTab(self.Order_tab, "Order")
        self.stacked_widget.addWidget(self.home_tab) 

    def OrderTab(self):
        order_group = QGroupBox()
        order_group.setTitle("Order")
        layout = QVBoxLayout()
        self.table_widget = QTableWidget(0, 8)
        self.table_widget.setHorizontalHeaderLabels(["Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category", "Quantity"])
        layout.addWidget(self.table_widget)
        order_group.setLayout(layout)

        order_widget = QWidget()
        layout_form = QFormLayout()
        self.order_date = QDateEdit()
        self.order_date.setCalendarPopup(True)
        self.order_date.setDate(QDate.currentDate())
        self.return_date = QDateEdit()
        self.return_date.setCalendarPopup(True)
        self.return_date.setDate(QDate.currentDate())
        layout_form.addRow("Order Date:", self.order_date)
        layout_form.addRow("Return Date:", self.return_date)
        order_widget.setLayout(layout_form)

        self.order_button = QPushButton("Order")
        self.order_button.clicked.connect(self.order)

        page2_v_box = QVBoxLayout()
        page2_v_box.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        page2_v_box.addWidget(order_group, alignment=Qt.AlignmentFlag.AlignTop)
        page2_v_box.addStretch(1)
        page2_v_box.addWidget(order_widget)
        page2_v_box.addWidget(self.order_button, alignment=Qt.AlignmentFlag.AlignRight)
        page2_v_box.addStretch(6)

        self.Order_tab.setLayout(page2_v_box)
    def order(self):
        user_id = self.get_user_id(self.user_info['email'])
        if not user_id:
            QMessageBox.warning(self, "Error", "User ID not found for the given email.")
            return

        orderline_id = str(uuid.uuid4())[:5]
        order_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        order_date = self.order_date.date().toString("yyyy-MM-dd")
        expiration_date = QDateTime.fromString(order_date, "yyyy-MM-dd").addDays(3).toString("yyyy-MM-dd")
        deadline = self.return_date.text()
        status = "In queue"
        extension = None
        method = "Online"
        violation = None
        book_return_date = None

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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (orderline_id, user_id, order_time, expiration_date, deadline, extension, status,book_return_date, method, violation))
            for row in range(self.table_widget.rowCount()):
                book_id = self.table_widget.item(row,0).text()
                quantity_spinbox_1 = self.table_widget.cellWidget(row,7)
                quantity = quantity_spinbox_1.value()
                print(book_id,quantity)
                insert_query_2 = """
                    INSERT INTO orders (order_id, book_id, quantity)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query_2, (orderline_id, book_id, quantity))
            connection.commit()

            QMessageBox.information(self, "Success", "Orderline created successfully!")

        except (Exception, psycopg2.Error) as error:
            QMessageBox.warning(self, "Error", f"Error while connecting to PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()


    def search_book(self):
        selected_button = self.title_group.checkedButton()
        if not selected_button:
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(8)
            self.result_table.setHorizontalHeaderLabels(["Select", "Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category"])
            self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem("Please select a search criterion."))
            return

        search_option = selected_button.text()
        search_value = self.search_input.text()

        if not search_value:
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(8)
            self.result_table.setHorizontalHeaderLabels(["Select", "Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category"])
            self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem("Please enter a search value."))
            return

        column_map = {
            "Book ID": "book_id",
            "Name": "name",
            "Author": "author",
            "Publisher": "publisher",
            "Origin": "origin",
            "Published Year": "published_year",
            "Category": "category"
        }
        column_name = column_map.get(search_option)

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

            query = f"SELECT book_id, name, author, publisher, origin, published_year, category FROM book WHERE {column_name} ILIKE %s"
            cursor.execute(query, (f"%{search_value}%",))
            rows = cursor.fetchall()

            if not rows:
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(8)
                self.result_table.setHorizontalHeaderLabels(["Select", "Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category"])
                self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                self.result_table.setRowCount(1)
                self.result_table.setItem(0, 0, QTableWidgetItem("No results found."))
                return

            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(8)
            self.result_table.setHorizontalHeaderLabels(["Select", "Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category"])
            self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for row in rows:
                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)
                select_check_box = QCheckBox()
                self.result_table.setCellWidget(row_position, 0, select_check_box)
                for column, item in enumerate(row):
                    self.result_table.setItem(row_position, column + 1, QTableWidgetItem(str(item)))

        except (Exception, psycopg2.Error) as error:
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(8)
            self.result_table.setHorizontalHeaderLabels(["Select", "Book ID", "Name", "Author", "Publisher", "Origin", "Published Year", "Category"])
            self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem(f"Error while connecting to PostgreSQL: {error}"))
        finally:
            if connection:
                cursor.close()
                connection.close()

    def process_selected_data(self):
        self.selected_data.clear()  # Xóa danh sách trước khi thêm dữ liệu mới
        for row in range(self.result_table.rowCount()):
            checkbox = self.result_table.cellWidget(row, 0)  # Lấy QCheckBox từ cột đầu tiên
            if checkbox and checkbox.isChecked():  # Kiểm tra xem QCheckBox có được chọn hay không
                row_data = []
                for column in range(1, self.result_table.columnCount()):  # Bỏ qua cột đầu tiên (QCheckBox)
                    item = self.result_table.item(row, column)
                    if item:
                        row_data.append(item.text())
                self.selected_data.append(row_data)
        
        self.update_order_tab()

    def update_order_tab(self):
        self.table_widget.setRowCount(0)  # Xóa các hàng hiện tại trong bảng Order
        for row_data in self.selected_data:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))
                self.table_widget.setItem(row, column, table_item)
            quantity_spinBox = QSpinBox()
            quantity_spinBox.setMinimum(1)
            quantity_spinBox.setMaximum(20)
            quantity_spinBox.setValue(1)
            self.table_widget.setCellWidget(row, 7, quantity_spinBox)

    def limit_selection(self):
        selected_checkboxes = [self.result_table.cellWidget(row, 0) for row in range(self.result_table.rowCount()) if self.result_table.cellWidget(row, 0).isChecked()]
        while(len(selected_checkboxes) > 5):
            self.sender().setChecked(False)

    def loadImage(self, img_path):
        try:
            with open(img_path):
                image = QLabel(self)
                image.setObjectName("ImageInfo")
                pixmap = QPixmap(img_path)
                image.setPixmap(pixmap.scaled(image.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                              Qt.TransformationMode.SmoothTransformation))
                return image
        except FileNotFoundError:
            print("Image not found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    sys.exit(app.exec())