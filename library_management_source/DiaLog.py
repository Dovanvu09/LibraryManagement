from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon,QAction
from PyQt6.QtCore import Qt, QSize,QDateTime,QDate
import sys 

class EditDialog_Account(QDialog):
    def __init__(self,row_data,parent = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Information")
        self.setModal(True)
        self.row_data = row_data
        self.initUI()
    def initUI(self):
        layout = QFormLayout(self)
        self.Email_edit = QLineEdit(self.row_data[0])
        self.Pass_edit  = QLineEdit(self.row_data[1])
        self.status_edit = QLineEdit(self.row_data[3])
        self.date_edit = QLineEdit(self.row_data[3])

        layout.addRow("New Email:",self.Email_edit)
        layout.addRow("New PassWord: ",self.Pass_edit)
        layout.addRow("New Status:",self.status_edit)
        layout.addRow("Created Date:",self.date_edit)
                      
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
    def get_data(self):
        return [ 
            self.Email_edit.text(),
            self.Pass_edit.text(),
            self.status_edit.text(),
            self.date_edit.text()
        ]
class EditDialog_Event(QDialog):
    def __init__(self, event_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Event Information")
        self.setModal(True)

        self.event_data = event_data if event_data is not None else ["", "", "", "", "", "", "", ""]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.name_edit = QLineEdit(self.event_data[0])
        self.organizer_edit = QLineEdit(self.event_data[1])
        self.sponsor_edit = QLineEdit(self.event_data[2])
        self.description_edit = QTextEdit(self.event_data[3])
        self.destination_edit = QLineEdit(self.event_data[4])
        self.target_participant_edit = QLineEdit(self.event_data[5])
        self.date_edit = QLineEdit(self.event_data[6])
        self.schedule_edit = QTextEdit(self.event_data[7])

        layout.addRow("Event Name:", self.name_edit)
        layout.addRow("Organiser:", self.organizer_edit)
        layout.addRow("Sponsor:", self.sponsor_edit)
        layout.addRow("Description:", self.description_edit)
        layout.addRow("Destination:", self.destination_edit)
        layout.addRow("Target Participant:", self.target_participant_edit)
        layout.addRow("Date:", self.date_edit)
        layout.addRow("Schedule:", self.schedule_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.name_edit.text(),
            self.organizer_edit.text(),
            self.sponsor_edit.text(),
            self.description_edit.toPlainText(),
            self.destination_edit.text(),
            self.target_participant_edit.text(),
            self.date_edit.text(),
            self.schedule_edit.toPlainText()
        ]
class EditDialog_Room(QDialog):
        def __init__(self, room_data=None, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Thông Tin Phòng")
            self.setModal(True)

            self.room_data = room_data if room_data is not None else ["", "", "", "", ""]
            self.initUI()

        def initUI(self):
            layout = QFormLayout(self)

            self.room_id_edit = QLineEdit(self.room_data[0])
            self.room_number_edit = QLineEdit(self.room_data[1])
            self.current_attendant_edit = QLineEdit(self.room_data[2])
            self.max_capacity_edit = QLineEdit(self.room_data[3])
            self.status_edit = QComboBox()
            self.status_edit.addItems(["Còn chỗ", "Tạm Đóng Cửa"])
            self.status_edit.setCurrentText(self.room_data[4])

            layout.addRow("Mã Phòng:", self.room_id_edit)
            layout.addRow("Số Phòng:", self.room_number_edit)
            layout.addRow("Số Người Hiện Tại:", self.current_attendant_edit)
            layout.addRow("Sức Chứa Tối Đa:", self.max_capacity_edit)
            layout.addRow("Trạng Thái:", self.status_edit)

            btn_layout = QHBoxLayout()
            save_btn = QPushButton("Lưu")
            save_btn.clicked.connect(self.accept)
            cancel_btn = QPushButton("Hủy")
            cancel_btn.clicked.connect(self.reject)
            btn_layout.addWidget(save_btn)
            btn_layout.addWidget(cancel_btn)

            layout.addRow(btn_layout)
        
        def get_data(self):
           return [
            self.room_id_edit.text(),
            self.room_number_edit.text(),
            self.current_attendant_edit.text(),
            self.max_capacity_edit.text(),
            self.status_edit.currentText()
           ]
class EditDialog_Book(QDialog):
    def __init__(self, book_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông Tin Sách")
        self.setModal(True)

        self.book_data = book_data if book_data is not None else ["", "", "", "", "", "", "", ""]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.book_id_edit = QLineEdit(self.book_data[0])
        self.name_edit = QLineEdit(self.book_data[1])
        self.author_edit = QLineEdit(self.book_data[2])
        self.publisher_edit = QLineEdit(self.book_data[3])
        self.origin_edit = QLineEdit(self.book_data[4])
        self.published_year_edit = QLineEdit(self.book_data[5])
        self.category_edit = QLineEdit(self.book_data[6])

        layout.addRow("Mã Sách:", self.book_id_edit)
        layout.addRow("Tên Sách:", self.name_edit)
        layout.addRow("Tác Giả:", self.author_edit)
        layout.addRow("Nhà Xuất Bản:", self.publisher_edit)
        layout.addRow("Xuất Xứ:", self.origin_edit)
        layout.addRow("Năm Xuất Bản:", self.published_year_edit)
        layout.addRow("Thể Loại:", self.category_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Lưu")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)
    def get_data(self):
        return [
            self.book_id_edit.text(),
            self.name_edit.text(),
            self.author_edit.text(),
            self.publisher_edit.text(),
            self.origin_edit.text(),
            self.published_year_edit.text(),
            self.category_edit.text()
        ]
class EditDialog_Order(QDialog):

    def __init__(self, order_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Order Information")
        self.setModal(True)

        self.order_data = order_data if order_data is not None else ["", "", 0]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.order_id_edit = QLineEdit(self.order_data[0])
        self.book_id_edit = QLineEdit(self.order_data[1])
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setValue(int(self.order_data[2]))

        layout.addRow("Order ID:", self.order_id_edit)
        layout.addRow("Book ID:", self.book_id_edit)
        layout.addRow("Quantity:", self.quantity_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.order_id_edit.text(),
            self.book_id_edit.text(),
            self.quantity_edit.value()
        ]
class EditDialog_Orderline(QDialog):
    def __init__(self, orderline_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Orderline Information")
        self.setModal(True)

        self.orderline_data = orderline_data if orderline_data is not None else ["", "", QDateTime.currentDateTime(), QDateTime.currentDateTime().date(), QDateTime.currentDateTime().date(), "", "", QDateTime.currentDateTime().date(), "", ""]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.orderline_id_edit = QLineEdit(self.orderline_data[0])
        self.student_id_edit = QLineEdit(self.orderline_data[1])
        self.order_time_edit = QDateEdit(self.orderline_data[2])
        self.order_time_edit.setCalendarPopup(True)
        self.expiration_date_edit = QDateEdit(self.orderline_data[3])
        self.expiration_date_edit.setCalendarPopup(True)
        self.deadline_edit = QDateEdit(self.orderline_data[4])
        self.deadline_edit.setCalendarPopup(True)
        self.extension_edit = QLineEdit(self.orderline_data[5])
        self.status_edit = QLineEdit(self.orderline_data[6])
        self.book_return_date_edit = QDateEdit(self.orderline_data[7])
        self.book_return_date_edit.setCalendarPopup(True)
        self.method_edit = QLineEdit(self.orderline_data[8])
        self.violation_edit = QLineEdit(self.orderline_data[9])

        layout.addRow("Orderline ID:", self.orderline_id_edit)
        layout.addRow("Student ID:", self.student_id_edit)
        layout.addRow("Order Time:", self.order_time_edit)
        layout.addRow("Expiration Date:", self.expiration_date_edit)
        layout.addRow("Deadline:", self.deadline_edit)
        layout.addRow("Extension:", self.extension_edit)
        layout.addRow("Status:", self.status_edit)
        layout.addRow("Book Return Date:", self.book_return_date_edit)
        layout.addRow("Method:", self.method_edit)
        layout.addRow("Violation:", self.violation_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.orderline_id_edit.text(),
            self.student_id_edit.text(),
            self.order_time_edit.date().toString("yyyy-MM-dd"),
            self.expiration_date_edit.date().toString("yyyy-MM-dd"),
            self.deadline_edit.date().toString("yyyy-MM-dd"),
            self.extension_edit.text(),
            self.status_edit.text(),
            self.book_return_date_edit.date().toString("yyyy-MM-dd"),
            self.method_edit.text(),
            self.violation_edit.text()
        ]
class EditDialog_Schedule(QDialog):
    def __init__(self, schedule_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Information")
        self.setModal(True)

        self.schedule_data = schedule_data if schedule_data is not None else ["", QDateTime.currentDateTime().date(), "", ""]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.timeshift_edit = QTimeEdit(QDateTime.currentDateTime().time())
        self.timeshift_edit.setDisplayFormat("HH:mm:ss")
        self.date_edit = QDateEdit(self.schedule_data[1])
        self.date_edit.setCalendarPopup(True)
        self.librarian_id_edit = QLineEdit(self.schedule_data[2])
        self.room_id_edit = QLineEdit(self.schedule_data[3])

        layout.addRow("Timeshift:", self.timeshift_edit)
        layout.addRow("Date:", self.date_edit)
        layout.addRow("Librarian ID:", self.librarian_id_edit)
        layout.addRow("Room ID:", self.room_id_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.timeshift_edit.time().toString("HH:mm:ss"),
            self.date_edit.date().toString("yyyy-MM-dd"),
            self.librarian_id_edit.text(),
            self.room_id_edit.text()
        ]
class EditDialog_archiving(QDialog):
    def __init__(self, book_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book Information")
        self.setModal(True)

        self.book_data = book_data if book_data is not None else ["", "", 0, 0, 0, 0]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.room_id_edit = QLineEdit(self.book_data[0])
        self.book_id_edit = QLineEdit(self.book_data[1])
        self.stock_edit = QLineEdit(str(self.book_data[2]))
        self.available_edit = QLineEdit(str(self.book_data[3]))
        self.in_order_edit = QLineEdit(str(self.book_data[4]))
        self.away_edit = QLineEdit(str(self.book_data[5]))

        layout.addRow("Room ID:", self.room_id_edit)
        layout.addRow("Book ID:", self.book_id_edit)
        layout.addRow("Stock:", self.stock_edit)
        layout.addRow("Available:", self.available_edit)
        layout.addRow("In Order:", self.in_order_edit)
        layout.addRow("Away:", self.away_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.room_id_edit.text(),
            self.book_id_edit.text(),
            int(self.stock_edit.text()),
            int(self.available_edit.text()),
            int(self.in_order_edit.text()),
            int(self.away_edit.text())
        ]
class EditDialog_Archive(QDialog):
    def __init__(self, room_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Room Information")
        self.setModal(True)

        self.room_data = room_data if room_data is not None else ["", ""]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.room_id_edit = QLineEdit(self.room_data[0])
        self.room_number_edit = QLineEdit(self.room_data[1])

        layout.addRow("Room ID:", self.room_id_edit)
        layout.addRow("Room Number:", self.room_number_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.room_id_edit.text(),
            self.room_number_edit.text()
        ]
class EditDialog_Student(QDialog):
    def __init__(self, student_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Student Information")
        self.setModal(True)

        self.student_data = student_data if student_data is not None else ["", "", "", "", "", "", ""]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.student_id_edit = QLineEdit(self.student_data[0])
        self.first_name_edit = QLineEdit(self.student_data[1])
        self.last_name_edit = QLineEdit(self.student_data[2])
        self.dob_edit = QLineEdit(self.student_data[3])
        self.gender_edit = QLineEdit(self.student_data[4])
        self.email_edit = QLineEdit(self.student_data[5])
        self.phone_number_edit = QLineEdit(self.student_data[6])

        layout.addRow("Student ID:", self.student_id_edit)
        layout.addRow("First Name:", self.first_name_edit)
        layout.addRow("Last Name:", self.last_name_edit)
        layout.addRow("Date of Birth:", self.dob_edit)
        layout.addRow("Gender:", self.gender_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Phone Number:", self.phone_number_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.student_id_edit.text(),
            self.first_name_edit.text(),
            self.last_name_edit.text(),
            self.dob_edit.text(),
            self.gender_edit.text(),
            self.email_edit.text(),
            self.phone_number_edit.text()
        ]
class EditDialog_Stock(QDialog):
    def __init__(self, stock_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Information")
        self.setModal(True)

        self.stock_data = stock_data if stock_data is not None else ["", None, None, 0]
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.book_id_edit = QLineEdit(self.stock_data[0])
        self.stock_in_date_edit = QDateEdit(self.stock_data[1] if self.stock_data[1] else QDateEdit())
        self.stock_out_date_edit = QDateEdit(self.stock_data[2] if self.stock_data[2] else QDateEdit())
        self.quantity_edit = QLineEdit(str(self.stock_data[3]))

        layout.addRow("Book ID:", self.book_id_edit)
        layout.addRow("Stock In Date:", self.stock_in_date_edit)
        layout.addRow("Stock Out Date:", self.stock_out_date_edit)
        layout.addRow("Quantity:", self.quantity_edit)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)

    def get_data(self):
        return [
            self.book_id_edit.text(),
            self.stock_in_date_edit.date().toString("yyyy-MM-dd"),
            self.stock_out_date_edit.date().toString("yyyy-MM-dd"),
            int(self.quantity_edit.text())
        ]
