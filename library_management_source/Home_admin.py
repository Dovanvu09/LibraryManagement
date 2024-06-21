from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon,QAction, QColor
from PyQt6.QtCore import Qt, QSize,QDate
import sys 
from DiaLog import(
     EditDialog_Event,EditDialog_Account,EditDialog_Room,EditDialog_Book,EditDialog_Order,
     EditDialog_Orderline,EditDialog_Schedule, EditDialog_archiving,EditDialog_Archive,
     EditDialog_Student,EditDialog_Stock)
import psycopg2



class admin_home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(100,100,800,800)
        self.setWindowTitle("Admin Management Interface")
        self.setupTabandLayout()
        # self.show()
    def setupTabandLayout(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        side_menu = QWidget()
        side_menu.setFixedWidth(200)
        side_menu.setStyleSheet("background-color: #2E2E2E; color : white;")

        side_layout = QVBoxLayout(side_menu)
        label_layout = QHBoxLayout()
        title_label = QLabel("Thư Viện Tạ Quang Bửu")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white; padding: 10px;")
        title_label.setWordWrap(True)
        label_layout.addWidget (title_label, alignment = Qt.AlignmentFlag.AlignCenter)
        side_layout.addLayout(label_layout)
        side_layout.addStretch() 

        buttons = [
            ("Order Management","D:\\test\\PyQt\\order.png"),
            ("Book Management","D:\\test\\PyQt\\book.png"),
            ("Account Management","D:\\test\\PyQt\\account.png"),
            ("Event Management","D:\\test\\PyQt\\event.png"),
            ("Room Management","D:\\test\\PyQt\\room.png"),
            ("OrderLine Management","D:\\test\\PyQt\\orderline.png"),
            ("Schedule Management", "D:\\test\\PyQt\\schedule.png"),
            ("Archiving Management", "D:\\test\\PyQt\\archiving.png"),
            ("Archive Room Management", "D:\\test\\PyQt\\archive.png"),
            ("Student Management", "D:\\test\\PyQt\\student.png"),
            ("Librarian Management", "D:\\test\\PyQt\\librarian.png"),
            ("Checkin Management", "D:\\test\\PyQt\\checkin.png"),
            ("Stocked Management", "D:\\test\\PyQt\\stock.png"),
            ("Notification Management","D:\\test\\PyQt\\notification"),
        ]
        self.buttons_group = QButtonGroup()
        self.sub_buttons_group = QButtonGroup()

        for index, (text, icon_path) in enumerate(buttons):
            btn = QToolButton()
            btn.setText(text)
            btn.setIcon(QIcon(icon_path))
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            btn.setFixedWidth(230)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #2E2E2E;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: left;
                }
                QToolButton:hover {
                    background-color: #3E3E3E;
                }
            """) 
            btn.clicked.connect(lambda checked, idx = index: self.display_page(idx))
            self.buttons_group.addButton(btn, index)
            side_layout.addWidget(btn)
            side_layout.addStretch() 
        # thêm spacer để đẩy các nút lên
        # side_layout.addStretch()
        self.stacked_widget = QStackedWidget()
        self.page = []
        self.setupPage_1()
        self.setupPage_2()
        self.setupPage_3()
        self.setupPage_4()
        self.setupPage_5()
        self.setupPage_6()
        self.setupPage_7()
        self.setupPage_8()
        self.setupPage_9()
        self.setupPage_10()
        self.setupPage_11()
        self.setupPage_12()
        self.setupPage_13()
        main_layout.addWidget(side_menu)
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)
    def setupPage_1(self):
        page_1  = QWidget()
        layout_1 = QVBoxLayout()
        
        title_label = QLabel("Order Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget_1 = QTableWidget(0, 4)
        self.table_widget_1.setHorizontalHeaderLabels(["Order ID", "Book ID", "Quantity", "Actions"])
        self.table_widget_1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_1.verticalHeader().setVisible(False)
        self.table_widget_1.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_1.setAlternatingRowColors(True)

        self.load_order_from_db()

        layout_1.addWidget(title_label)
        layout_1.addWidget(self.table_widget_1)
        page_1.setLayout(layout_1)

        self.page.append(page_1)
        self.stacked_widget.addWidget(page_1)

        self.table_widget_1.resizeColumnsToContents()
        self.table_widget_1.resizeRowsToContents()
    def setupPage_2(self):
        page_2 = QWidget()
        layout_2 = QVBoxLayout()
        
        title_label = QLabel("Quản Lý Sách")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_2.addWidget(title_label)

        button_layout_2 = QHBoxLayout()
        add_book_btn = QPushButton("add book")
        add_book_btn.setStyleSheet("background-color: #007bff; color: White; padding: 10px;")
        
        button_layout_2.addWidget(add_book_btn)
        button_layout_2.addStretch()

        #block search
        search_layout = QHBoxLayout()
        search_layout.addStretch()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Name book")
        search_combo = QComboBox()
        search_combo.addItems(["All", "Textbooks", "Coursebooks", "Reference books", "Novels", "Children's books","IT Book"])
        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("background-color: #007bff; color : white; padding: 10px;")

        search_layout.addWidget(search_input)
        search_layout.addWidget(search_combo)
        search_layout.addWidget(search_btn)

        self.table_widget_2 = QTableWidget(0, 9)
        self.table_widget_2.setHorizontalHeaderLabels(["stt","book_id", "Name", "Author", "Publisher", "origin", "Publisheed_year", "category", "Edit"])
        self.table_widget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_2.verticalHeader().setVisible(False)
        self.table_widget_2.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_2.setAlternatingRowColors(True)

        self.load_book_from_db()

        layout_2.addLayout(search_layout)
        layout_2.addLayout(button_layout_2)
        layout_2.addWidget(self.table_widget_2)
        page_2.setLayout(layout_2)
        self.page.append(page_2)
        self.stacked_widget.addWidget(page_2)
    def setupPage_3(self):
        page_3 = QWidget()
        layout_3 = QVBoxLayout(page_3)
        # Create title
        title_label = QLabel("Account Management")
        title_label.setStyleSheet("""
             font-size: 24px;
             font-weight: bold;
             color: #ffffff;
             background-color:#333333;
             border-radius: 5px;
             margin-bottom:20px;
                                  """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Create table account
        self.table_widget_3 = QTableWidget(0,5)

        self.table_widget_3.setHorizontalHeaderLabels(["Email","PassWord","Status","Created","Edit"])
        self.table_widget_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_3.verticalHeader().setVisible(False)
        self.table_widget_3.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_3.setAlternatingRowColors(True)
        self.load_data_account_from_db()
        
        layout_3.addWidget(title_label)
        layout_3.addWidget(self.table_widget_3)
       
        self.page.append(page_3)
        self.stacked_widget.addWidget(page_3)
        self.table_widget_3.resizeColumnsToContents()
        self.table_widget_3.resizeRowsToContents()
    def setupPage_4(self):
        page_4 = QWidget()
        layout_4 = QVBoxLayout(page_4)

        title_label = QLabel("Event Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget_4 = QTableWidget(0, 9)
        self.table_widget_4.setHorizontalHeaderLabels(["Event Name", "Organizer", "Sponsor", "Description", "Destination", "Target Participant", "Date", "Schedule", "Actions"])
        self.table_widget_4.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_4.verticalHeader().setVisible(False)
        self.table_widget_4.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_4.setAlternatingRowColors(True)

        self.load_event_from_db()

        layout_4.addWidget(title_label)
        layout_4.addWidget(self.table_widget_4)
        page_4.setLayout(layout_4)
        self.page.append(page_4)
        self.stacked_widget.addWidget(page_4)

        self.table_widget_4.resizeColumnsToContents()
        self.table_widget_4.resizeRowsToContents()
    def setupPage_5(self):
        page_5 = QWidget()
        layout_5 = QVBoxLayout(page_5)
        title_label = QLabel("Self Study and Reading Room Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget_room = QTableWidget(0, 5)  # Cập nhật số cột thành 6
        self.table_widget_room.setHorizontalHeaderLabels(["Room ID", "Room Number", "Current Attendant", "Max Capacity", "Status"])
        self.table_widget_room.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_room.verticalHeader().setVisible(False)
        self.table_widget_room.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_room.setAlternatingRowColors(True)
        self.load_data_Room_from_db()
        layout_5.addWidget(title_label)
        layout_5.addWidget(self.table_widget_room)
        self.stacked_widget.addWidget(page_5)
        self.page.append(page_5)
    def setupPage_6(self):
        page_6 = QWidget()
        layout_6 = QVBoxLayout(page_6)

        title_label = QLabel("Orderline Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input_6 = QLineEdit()
        self.search_input_6.setPlaceholderText("Enter Orderline ID to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_orderline)
        search_layout.addWidget(self.search_input_6)
        search_layout.addWidget(search_button)

        self.table_widget_6 = QTableWidget(0, 11)
        self.table_widget_6.setHorizontalHeaderLabels(["Orderline ID", "Student ID", "Order Time", "Expiration Date", "Deadline", "Extension", "Status", "Book Return Date", "Method", "Violation", "Actions"])
        self.table_widget_6.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_6.verticalHeader().setVisible(False)
        self.table_widget_6.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_6.setAlternatingRowColors(True)

        self.load_orderline_from_db()

        layout_6.addWidget(title_label)
        layout_6.addLayout(search_layout)
        layout_6.addWidget(self.table_widget_6)

        self.page.append(page_6)
        self.stacked_widget.addWidget(page_6)

        self.table_widget_6.resizeColumnsToContents()
        self.table_widget_6.resizeRowsToContents()
    def setupPage_7(self):
        page_7 = QWidget()
        layout_7 = QVBoxLayout(page_7)

        title_label = QLabel("Schedule Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Librarian ID to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_schedule)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        self.table_widget_7 = QTableWidget(0, 5)
        self.table_widget_7.setHorizontalHeaderLabels(["Timeshift", "Date", "Librarian ID", "Room ID", "Actions"])
        self.table_widget_7.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_7.verticalHeader().setVisible(False)
        self.table_widget_7.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_7.setAlternatingRowColors(True)

        self.load_schedule_from_db()

        layout_7.addWidget(title_label)
        layout_7.addLayout(search_layout)
        layout_7.addWidget(self.table_widget_7)

        self.page.append(page_7)
        self.stacked_widget.addWidget(page_7)

        self.table_widget_7.resizeColumnsToContents()
        self.table_widget_7.resizeRowsToContents()
    def setupPage_8(self):
        page_8 = QWidget()
        layout_8 = QVBoxLayout(page_8)

        title_label = QLabel("Book archiving Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Room ID or Book ID to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_inventory)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        self.table_widget_8 = QTableWidget(0, 7)
        self.table_widget_8.setHorizontalHeaderLabels(["Room ID", "Book ID", "Stock", "Available", "In Order", "Away", "Actions"])
        self.table_widget_8.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_8.verticalHeader().setVisible(False)
        self.table_widget_8.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_8.setAlternatingRowColors(True)

        self.load_archiving_from_db()

        layout_8.addWidget(title_label)
        layout_8.addLayout(search_layout)
        layout_8.addWidget(self.table_widget_8)
        page_8.setLayout(layout_8)

        self.page.append(page_8)
        self.stacked_widget.addWidget(page_8)

        self.table_widget_8.resizeColumnsToContents()
        self.table_widget_8.resizeRowsToContents()
    def setupPage_9(self):
        page_9 = QWidget()
        layout_9 = QVBoxLayout(page_9)

        title_label = QLabel("Archive Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget_9 = QTableWidget(0, 3)
        self.table_widget_9.setHorizontalHeaderLabels(["Room ID", "Room Number","Actions"])
        self.table_widget_9.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_9.verticalHeader().setVisible(False)
        self.table_widget_9.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_9.setAlternatingRowColors(True)

        self.load_archive_from_db()

        layout_9.addWidget(title_label)
        layout_9.addWidget(self.table_widget_9)
        page_9.setLayout(layout_9)

        self.page.append(page_9)
        self.stacked_widget.addWidget(page_9)

        self.table_widget_9.resizeColumnsToContents()
        self.table_widget_9.resizeRowsToContents()
    def setupPage_10(self):
        page_10 = QWidget()
        layout_10 = QVBoxLayout(page_10)

        title_label = QLabel("Student Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Student ID or Name to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        self.table_widget_10 = QTableWidget(0, 8)
        self.table_widget_10.setHorizontalHeaderLabels(["Student ID", "First Name", "Last Name", "DOB", "Gender", "Email", "Phone Number", "Actions"])
        self.table_widget_10.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_10.verticalHeader().setVisible(False)
        self.table_widget_10.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_10.setAlternatingRowColors(True)

        self.load_student_from_db()

        layout_10.addWidget(title_label)
        layout_10.addLayout(search_layout)
        layout_10.addWidget(self.table_widget_10)

        self.page.append(page_10)
        self.stacked_widget.addWidget(page_10)

        self.table_widget_10.resizeColumnsToContents()
        self.table_widget_10.resizeRowsToContents()
    def setupPage_11(self):
        page_11 = QWidget()
        layout_11 = QVBoxLayout()

        title_label = QLabel("Librarian Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Librarian ID or Name to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_librarian)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        self.table_widget_11 = QTableWidget(0, 7)
        self.table_widget_11.setHorizontalHeaderLabels(["Librarian ID", "First Name", "Last Name", "DOB", "Gender", "Email", "Phone Number"])
        self.table_widget_11.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_11.verticalHeader().setVisible(False)
        self.table_widget_11.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_11.setAlternatingRowColors(True)

        self.load_librarian_from_db()

        layout_11.addWidget(title_label)
        layout_11.addLayout(search_layout)
        layout_11.addWidget(self.table_widget_11)

        page_11.setLayout(layout_11)
        self.page.append(page_11)
        self.stacked_widget.addWidget(page_11)

        self.table_widget_11.resizeColumnsToContents()
        self.table_widget_11.resizeRowsToContents()
    def setupPage_12(self):
        page_12 = QWidget()
        layout_12 = QVBoxLayout(page_12)

        title_label = QLabel("Room Check Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Student ID to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_room_check)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        self.table_widget_12 = QTableWidget(0, 4)
        self.table_widget_12.setHorizontalHeaderLabels(["Student ID", "Room ID", "Check In", "Check Out"])
        self.table_widget_12.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_12.verticalHeader().setVisible(False)
        self.table_widget_12.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_12.setAlternatingRowColors(True)

        self.load_check_from_db()

        layout_12.addWidget(title_label)
        layout_12.addLayout(search_layout)
        layout_12.addWidget(self.table_widget_12)

        self.page.append(page_12)
        self.stacked_widget.addWidget(page_12)

        self.table_widget_12.resizeColumnsToContents()
        self.table_widget_12.resizeRowsToContents()
    
    def setupPage_13(self):
        page_13 = QWidget()
        layout_13 = QVBoxLayout(page_13)

        title_label = QLabel("Stock Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff;
            background-color: #333333;
            border-radius: 5px;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget_13 = QTableWidget(0, 4)
        self.table_widget_13.setHorizontalHeaderLabels(["Book ID", "Stock In Date", "Stock Out Date", "Quantity"])
        self.table_widget_13.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget_13.verticalHeader().setVisible(False)
        self.table_widget_13.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #dddddd;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #dddddd;
            }
        """)
        self.table_widget_13.setAlternatingRowColors(True)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_stock_row)
        btn_layout.addWidget(add_btn)

        self.load_stock_from_db()

        layout_13.addWidget(title_label)
        layout_13.addWidget(self.table_widget_13)
        layout_13.addLayout(btn_layout)

        self.page.append(page_13)
        self.stacked_widget.addWidget(page_13)

        self.table_widget_13.resizeColumnsToContents()
        self.table_widget_13.resizeRowsToContents()
#----------------------------------------------Stock --------------------------------------------
    def load_stock_from_db(self):
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

            cursor.execute("SELECT book_id, stock_in_date, stock_out_date, quantity FROM stock")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_table_stock_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_table_stock_row(self, row_data):
        row = self.table_widget_13.rowCount()
        self.table_widget_13.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_13.setItem(row, column, table_item)

    def add_stock_row(self):
        dialog = EditDialog_Stock(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            self.add_table_stock_row(new_data)
            
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
                INSERT INTO stock (book_id, stock_in_date, stock_out_date, quantity)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, tuple(new_data))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error inserting into PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
#----------------------------------------------check_in--------------------------------------------
    def load_check_from_db(self):
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

            cursor.execute("SELECT student_id, room_id, check_in, check_out FROM check_in")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_check_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_check_row(self, row_data):
        row = self.table_widget_12.rowCount()
        self.table_widget_12.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_12.setItem(row, column, table_item)

    def search_room_check(self):
        search_text = self.search_input.text()
        if not search_text:
            return

        for row in range(self.table_widget_12.rowCount()):
            student_id = self.table_widget_12.item(row, 0).text()
            if search_text.lower() in student_id.lower():
                for column in range(self.table_widget_12.columnCount()):
                    self.table_widget_12.item(row, column).setBackground(QColor(255, 0, 0))
                return
#----------------------------------------------Librarian--------------------------------------------
    def load_librarian_from_db(self):
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

            cursor.execute("SELECT librarian_id, first_name, last_name, dob, gender, email, phone_number FROM librarian")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_librarian_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_librarian_row(self, row_data):
        row = self.table_widget_11.rowCount()
        self.table_widget_11.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_11.setItem(row, column, table_item)

    def search_librarian(self):
        search_text = self.search_input.text()
        if not search_text:
            return

        for row in range(self.table_widget_11.rowCount()):
            librarian_id = self.table_widget_11.item(row, 0).text()
            first_name = self.table_widget_11.item(row, 1).text()
            last_name = self.table_widget_11.item(row, 2).text()
            if search_text.lower() in librarian_id.lower() or search_text.lower() in first_name.lower() or search_text.lower() in last_name.lower():
                for column in range(self.table_widget_11.columnCount()):
                    self.table_widget_11.item(row, column).setBackground(QColor(255, 0, 0))
                return

#----------------------------------------------Student--------------------------------------------
    def load_student_from_db(self):
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

            cursor.execute("SELECT student_id, first_name, last_name, dob, gender, email, phone_number FROM student")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_student_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_student_row(self, row_data):
        row = self.table_widget_10.rowCount()
        self.table_widget_10.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_10.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_student_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_student_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_10.setCellWidget(row, 7, btn_widget)

    def edit_student_row(self, parent, row):
        row_data = [self.table_widget_10.item(row, i).text() for i in range(7)]
        dialog = EditDialog_Student(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_10.setItem(row, i, QTableWidgetItem(item))

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

                update_query = """
                UPDATE student
                SET student_id = %s, first_name = %s, last_name = %s, dob = %s, gender = %s, email = %s, phone_number = %s
                WHERE student_id = %s
                """
                cursor.execute(update_query, (new_data[0], new_data[1], new_data[2], new_data[3], new_data[4], new_data[5], new_data[6], row_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_student_row(self, parent, row):
        row_data = [self.table_widget_10.item(row, i).text() for i in range(7)]

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

            delete_query = "DELETE FROM student WHERE student_id = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_10.removeRow(row)

    def search_student(self):
        search_text = self.search_input.text()
        if not search_text:
            return

        for row in range(self.table_widget_10.rowCount()):
            student_id = self.table_widget_10.item(row, 0).text()
            first_name = self.table_widget_10.item(row, 1).text()
            last_name = self.table_widget_10.item(row, 2).text()
            if search_text.lower() in student_id.lower() or search_text.lower() in first_name.lower() or search_text.lower() in last_name.lower():
                for column in range(self.table_widget_10.columnCount()):
                    self.table_widget_10.item(row, column).setBackground(QColor(255, 0, 0))
                return
#----------------------------------------------ArchiVe_room--------------------------------------- 
    def load_archive_from_db(self):
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT room_id, room_number FROM archive_room")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_archive_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_archive_row(self, row_data):
        row = self.table_widget_9.rowCount()
        self.table_widget_9.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_9.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_archive_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_archive_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_9.setCellWidget(row, 2, btn_widget)

    def edit_archive_row(self, parent, row):
        row_data = [self.table_widget_9.item(row, i).text() for i in range(2)]
        dialog = EditDialog_Archive(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_9.setItem(row, i, QTableWidgetItem(item))

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

                update_query = """
                UPDATE archive_room
                SET room_id = %s, room_number = %s
                WHERE room_id = %s
                """
                cursor.execute(update_query, (new_data[0], new_data[1], row_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_archive_row(self, parent, row):
        row_data = [self.table_widget_9.item(row, i).text() for i in range(2)]

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

            delete_query = "DELETE FROM archive_room WHERE room_id = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_9.removeRow(row)

#----------------------------------------------ArchiVing--------------------------------------- 
    def load_archiving_from_db(self):
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

            cursor.execute("SELECT room_id, book_id, stock, available, in_order, away FROM archiving")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_archiving_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_archiving_row(self, row_data):
        row = self.table_widget_8.rowCount()
        self.table_widget_8.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_8.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_archiving_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_archiving_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_8.setCellWidget(row, 6, btn_widget)

    def edit_archiving_row(self, parent, row):
        row_data = [self.table_widget_8.item(row, i).text() for i in range(6)]
        dialog = EditDialog_archiving(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_8.setItem(row, i, QTableWidgetItem(str(item)))

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

                update_query = """
                UPDATE book_inventory
                SET room_id = %s, book_id = %s, stock = %s, available = %s, in_order = %s, away = %s
                WHERE room_id = %s AND book_id = %s
                """
                cursor.execute(update_query, (new_data[0], new_data[1], new_data[2], new_data[3], new_data[4], new_data[5], row_data[0], row_data[1]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_archiving_row(self, parent, row):
        row_data = [self.table_widget_8.item(row, i).text() for i in range(6)]

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

            delete_query = "DELETE FROM archiving WHERE room_id = %s AND book_id = %s"
            cursor.execute(delete_query, (row_data[0], row_data[1]))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_8.removeRow(row)

    def search_inventory(self):
        search_text = self.search_input.text()
        if not search_text:
            return

        for row in range(self.table_widget_8.rowCount()):
            room_id = self.table_widget_8.item(row, 0).text()
            book_id = self.table_widget_8.item(row, 1).text()
            if room_id == search_text or book_id == search_text:
                for column in range(self.table_widget_8.columnCount()):
                    self.table_widget_8.item(row, column).setBackground(QColor(255, 0, 0))
                return
#----------------------------------------------OrderLine---------------------------------------
    def load_orderline_from_db(self):
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

            cursor.execute("SELECT orderline_id, student_id, order_time, expiration_date, deadline, extension, status, book_return_date, method, violation FROM orderline")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_orderline_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_orderline_row(self, row_data):
        row = self.table_widget_6.rowCount()
        self.table_widget_6.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_6.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_orderline_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_orderline_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_6.setCellWidget(row, 10, btn_widget)

    def edit_orderline_row(self, parent, row):
        row_data = [self.table_widget_6.item(row, i).text() for i in range(10)]
        dialog = EditDialog_Orderline(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_6.setItem(row, i, QTableWidgetItem(item))

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

                update_query = """
                UPDATE orderline
                SET student_id = %s, order_time = %s, expiration_date = %s, deadline = %s, extension = %s, status = %s, book_return_date = %s, method = %s, violation = %s
                WHERE orderline_id = %s
                """
                cursor.execute(update_query, (new_data[1], new_data[2], new_data[3], new_data[4], new_data[5], new_data[6], new_data[7], new_data[8], new_data[9], new_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_orderline_row(self, parent, row):
        row_data = [self.table_widget_6.item(row, i).text() for i in range(10)]

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

            delete_query = "DELETE FROM orderline WHERE orderline_id = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_6.removeRow(row)

    def search_orderline(self):
        search_text = self.search_input_6.text()
        if not search_text:
            return

        for row in range(self.table_widget_6.rowCount()):
            orderline_id = self.table_widget_6.item(row, 0).text()
            if orderline_id == search_text:
                self.table_widget_6.selectRow(row)
                return
#----------------------------------------------Order-------------------------------------------
    def load_order_from_db(self):
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

            cursor.execute("SELECT order_id, book_id, quantity FROM orders")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_order_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_order_row(self, row_data):
        row = self.table_widget_1.rowCount()
        self.table_widget_1.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_1.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_1.setCellWidget(row, 3, btn_widget)

    def edit_row(self, parent, row):
        row_data = [self.table_widget_1.item(row, i).text() for i in range(3)]
        dialog = EditDialog_Order(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_1.setItem(row, i, QTableWidgetItem(item))

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

                update_query = """
                UPDATE orders
                SET book_id = %s, quantity = %s
                WHERE order_id = %s
                """
                cursor.execute(update_query, (new_data[1], new_data[2], new_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_row(self, parent, row):
        row_data = [self.table_widget_1.item(row, i).text() for i in range(3)]

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

            delete_query = "DELETE FROM orders WHERE order_id = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_1.removeRow(row)
#----------------------------------------------Book--------------------------------------------


    def load_book_from_db(self):
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT book_id, name, author, publisher, origin, published_year, category FROM book")
            rows = cursor.fetchall()

            self.data = []  # Danh sách lưu trữ dữ liệu từ cơ sở dữ liệu

            for row in rows:
                self.data.append(row)
                self.add_book_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Lỗi khi kết nối tới PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_book_row(self, row_data):
        row = self.table_widget_2.rowCount()
        self.table_widget_2.insertRow(row)
        stt_item = QTableWidgetItem(str(row+1))
        self.table_widget_2.setItem(row,0,stt_item)
        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_2.setItem(row, column+1, table_item)

        # Thêm nút chức năng vào cột "Chức Năng"
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Chỉnh sửa")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_book_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Xóa")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_2.setCellWidget(row, 8, btn_widget)

    def edit_book_row(self, parent, row):
        row_data = [self.table_widget_2.item(row, i).text() for i in range(1,8)]
        dialog = EditDialog_Book(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_2.setItem(row, i+1, QTableWidgetItem(item))

            # Update database
            try:
                connection = psycopg2.connect(
                    dbname="library_db",
                    user="postgres",
                    password="admin",
                    host="localhost",
                    port="5432"
                )
                cursor = connection.cursor()

                update_query = """
                UPDATE books
                SET book_id = %s, name = %s, author = %s, publisher = %s, origin = %s, published_year = %s, category = %s
                WHERE book_id = %s
                """
                cursor.execute(update_query, (*new_data, row_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Lỗi khi cập nhật PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_book_row(self, parent, row):
        row_data = [self.table_widget_2.item(row, i).text() for i in range(1,8)]

        # Remove from database
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            delete_query = "DELETE FROM books WHERE book_id = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Lỗi khi xóa từ PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        # Remove from table widget
        self.table_widget_2.removeRow(row)
        self.update_stt_column()
    def update_stt_column(self):
        for row in range(self.table_widget_2.rowCount()):
            stt_item = QTableWidgetItem(str(row + 1))
            self.table_widget_2.setItem(row, 0, stt_item)


#----------------------------------------------Room--------------------------------------------

    def load_data_Room_from_db(self):
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT room_id, room_number, current_attendant, max_capacity, status FROM self_study_and_reading_room")
            rows = cursor.fetchall()

            self.data = []  # Danh sách lưu trữ dữ liệu từ cơ sở dữ liệu

            for row in rows:
                self.data.append(row)
                self.add_Room_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Lỗi khi kết nối tới PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
    def add_Room_row(self, row_data):
        row = self.table_widget_room.rowCount()
        self.table_widget_room.insertRow(row)
        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_room.setItem(row, column, table_item)

        # # Thêm nút chức năng vào cột "Chức Năng"
        # btn_widget = QWidget()
        # btn_layout = QHBoxLayout(btn_widget)
        
        # edit_btn = QPushButton("Chỉnh sửa")
        # edit_btn.setStyleSheet("""
        #     background-color: blue;
        #     color: white;
        #     padding: 5px;
        #     border: none;
        #     border-radius: 3px;
        # """)
        # edit_btn.clicked.connect(lambda checked, r=row: self.edit_room(r))
        # btn_layout.addWidget(edit_btn)

        # delete_btn = QPushButton("Xóa")
        # delete_btn.setStyleSheet("""
        #     background-color: red;
        #     color: white;
        #     padding: 5px;
        #     border: none;
        #     border-radius: 3px;
        # """)
        # delete_btn.clicked.connect(lambda checked, r=row: self.delete_room(r))
        # btn_layout.addWidget(delete_btn)
        
        # btn_layout.addStretch()
        # btn_layout.setContentsMargins(0, 0, 0, 0)
        # btn_widget.setLayout(btn_layout)
        # self.table_widget_room.setCellWidget(row, 5, btn_widget)
    # def edit_room(self, row):
    #     row_data = [self.table_widget_room.item(row, i).text() for i in range(5)]
    #     dialog = EditDialog_Room(row_data, self)
    #     if dialog.exec() == QDialog.DialogCode.Accepted:
    #         new_data = dialog.get_data()
    #         for i, item in enumerate(new_data):
    #             self.table_widget_room.setItem(row, i, QTableWidgetItem(item))

    def delete_room(self, row):
        self.table_widget_room.removeRow(row)

#----------------------------------------------Account-------------------------------------------- 
    def load_data_account_from_db(self):
        try:
            connection = psycopg2.connect(
                dbname="library_db",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT email, password, created_date,status FROM account")
            rows = cursor.fetchall()

            self.data = []  # Danh sách lưu trữ dữ liệu từ cơ sở dữ liệu

            for row in rows:
                self.data.append(row)
                self.add_account_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Lỗi khi kết nối tới PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
    def add_account_row(self,row_data):
        row = self.table_widget_3.rowCount()
        self.table_widget_3.insertRow(row)
        for column,item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_3.setItem(row,column, table_item)
        
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("D:\\test\\PyQT\\edit.png"))
        edit_btn.setToolTip("edit")
        edit_btn.clicked.connect(lambda checked, parent = self, r = row : self.edit_row_account(parent,r))
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: White;
            padding: 5px;
            border: none;
            border-radius: 3px;
                                """)
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("D:\\test\\PyQT\\delete.png"))
        delete_btn.setToolTip("Xóa")
        delete_btn.clicked.connect(lambda checked,parent = self,  r = row: self.delete_row_account(parent,r))
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
    
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_3.setCellWidget(row,4,btn_widget)
    def edit_row_account(self, parent, row):
        row_data = [self.table_widget_3.item(row, i).text() for i in range(4)]
        dialog = EditDialog_Account(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_3.setItem(row, i, QTableWidgetItem(item))

            # Update database
            try:
                connection = psycopg2.connect(
                    dbname="lbrary_db",
                    user="postgres",
                    password="admin",
                    host="localhost",
                    port="5432"
                )
                cursor = connection.cursor()

                update_query = """
                UPDATE accout
                SET email = %s, password = %s, created_date = %s,  status = %s
                WHERE email = %s
                """
                cursor.execute(update_query, (*new_data, row_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Lỗi khi cập nhật PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
    def delete_row_account(self, parent, row):
        row_data = [self.table_widget_3.item(row, i).text() for i in range(4)]

        # Remove from database
        try:
            connection = psycopg2.connect(
                    dbname="lbrary_db",
                    user="postgres",
                    password="admin",
                    host="localhost",
                    port="5432"
                )
            cursor = connection.cursor()

            delete_query = "DELETE FROM accout WHERE email = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Lỗi khi xóa từ PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        # Remove from table widget
        self.table_widget_3.removeRow(row)
    
#----------------------------------------------EVent--------------------------------------------
    def load_event_from_db(self):
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

            cursor.execute("SELECT name, organiser, sponsor, description, destination, target_participant, date, schedule FROM special_event")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_event_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_event_row(self, row_data):
        row = self.table_widget_4.rowCount()
        self.table_widget_4.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_4.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_event_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_4.setCellWidget(row, 8, btn_widget)

    def edit_event_row(self, parent, row):
        row_data = [self.table_widget_4.item(row, i).text() for i in range(9)] 
        dialog = EditDialog_Event(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_4.setItem(row, i, QTableWidgetItem(item))

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

                update_query = """
                UPDATE special_event
                SET name = %s, organiser = %s, sponsor = %s, description = %s, destination = %s, target_participant = %s, date = %s, schedule = %s
                WHERE name = %s
                """
                cursor.execute(update_query, (*new_data, row_data[0]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_event_row(self, parent, row):
        row_data = [self.table_widget_4.item(row, i).text() for i in range(8)]

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

            delete_query = "DELETE FROM special_event WHERE name = %s"
            cursor.execute(delete_query, (row_data[0],))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_4.removeRow(row)
#----------------------------------------------Schedule--------------------------------------------
    def load_schedule_from_db(self):
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

            cursor.execute("SELECT timeshift, date, librarian_id, room_id FROM schedule")
            rows = cursor.fetchall()

            self.data = []
            for row in rows:
                self.data.append(row)
                self.add_schedule_row(row)

        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_schedule_row(self, row_data):
        row = self.table_widget_7.rowCount()
        self.table_widget_7.insertRow(row)

        for column, item in enumerate(row_data):
            table_item = QTableWidgetItem(str(item))
            self.table_widget_7.setItem(row, column, table_item)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        edit_btn.clicked.connect(lambda checked, parent=self, r=row: self.edit_schedule_row(parent, r))
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            background-color: red;
            color: white;
            padding: 5px;
            border: none;
            border-radius: 3px;
        """)
        delete_btn.clicked.connect(lambda checked, parent=self, r=row: self.delete_schedule_row(parent, r))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.table_widget_7.setCellWidget(row, 4, btn_widget)

    def edit_schedule_row(self, parent, row):
        row_data = [self.table_widget_7.item(row, i).text() for i in range(4)]
        dialog = EditDialog_Schedule(row_data, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            for i, item in enumerate(new_data):
                self.table_widget_7.setItem(row, i, QTableWidgetItem(item))

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

                update_query = """
                UPDATE schedule
                SET timeshift = %s, date = %s, librarian_id = %s, room_id = %s
                WHERE timeshift = %s AND date = %s AND librarian_id = %s AND room_id = %s
                """
                cursor.execute(update_query, (new_data[0], new_data[1], new_data[2], new_data[3], row_data[0], row_data[1], row_data[2], row_data[3]))
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error updating PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def delete_schedule_row(self, parent, row):
        row_data = [self.table_widget_7.item(row, i).text() for i in range(4)]

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

            delete_query = "DELETE FROM schedule WHERE timeshift = %s AND date = %s AND librarian_id = %s AND room_id = %s"
            cursor.execute(delete_query, (row_data[0], row_data[1], row_data[2], row_data[3]))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error deleting from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        self.table_widget_7.removeRow(row)

    def search_schedule(self):
        search_text = self.search_input.text()
        if not search_text:
            return

        for row in range(self.table_widget_7.rowCount()):
            librarian_id = self.table_widget_7.item(row, 2).text()
            if librarian_id == search_text:
                self.highlight_row(row) 
                return
    def highlight_row(self, row):
        for column in range(self.table_widget_7.columnCount()):
            item = self.table_widget_7.item(row, column)
            if item:
                item.setBackground(QColor("yellow"))
    def display_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = admin_home()
    exit(app.exec()) 

