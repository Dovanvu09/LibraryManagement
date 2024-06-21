
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QLineEdit, QFormLayout, QGroupBox, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import sys
import psycopg2
from Home_admin import admin_home
from Home_user import HomeWindow_user

# style_sheet = """
# QWidget{
#     background-color: #C92108;
# }
# QWidget#Tabs{
#     background-color: #FCEBCD;
#     border-radius: 4px;    
# }
# QWidget#ImageBorder{
#     background-color: #FCF9F3;
#     border-width: 2px;
#     border-style: solid;
#     border-color: #FABB4C;
# }
# QWidget#Side{
#     background-color: #EFD096;
#     border-radius: 4px;
# }
# QLabel{
#     background-color: #EFD096;
#     border-width: 2px;
#     border-style: solid;
#     border-radius: 4px;
#     border-color: #EFD096;
# }
# QLabel#Header{
#     background-color: #EFD096;
#     border-width: 2px;
#     border-style: solid;
#     border-color: #EFD096;
#     padding-left: 10px;
#     color: #961A07;
# }
# QLabel#ImageInfo{
#     background-color: #FCF9F3;
#     border-radius: 4px;
# }
# QGroupBox{
#     background-color: #FCEBCD;
#     border-radius: 4px;
# }
# QRadioButton{
#     background-color: #FCF9F3;
# }
# QPushButton{
#     background-color: #C92108;
#     border-radius: 4px;
#     padding: 6px;
#     color: #FFFFFF;
# }
# QPushButton:pressed{
#     background-color: #C86354;
#     border-radius: 4px;
#     padding: 6px;
#     color: #DFD8D7;
# }
# """

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("タクアンブウ図書館")
        self.setupTabAndLayout()
        self.show()

    def setupTabAndLayout(self):
        layout = QVBoxLayout()

        self.avt_label = QLabel()
        self.avt_label.resize(70, 70)
        avt_path = "D:\\test\\PyQT\\user2.jpg"
        pixmap = QPixmap(avt_path)
        self.avt_label.setPixmap(pixmap.scaled(self.avt_label.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                               Qt.TransformationMode.SmoothTransformation))

        username_layout = QHBoxLayout()
        username_widget = QWidget()
        self.username_label = QLabel("Email:        ")
        self.username_label.setFont(QFont("Arial", 12))
        self.username_input = QLineEdit()
        self.username_input.setFixedSize(200, 30)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)

        password_widget = QWidget()
        password_layout = QHBoxLayout()
        self.password_label = QLabel("Password: ")
        self.password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit()
        self.password_input.setFixedSize(200, 30)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)

        username_widget.setLayout(username_layout)
        password_widget.setLayout(password_layout)

        self.login_button = QPushButton("Login")
        self.login_button.setFixedSize(100, 30)
        self.login_button.clicked.connect(self.login)

        layout.addStretch(1)
        layout.addWidget(self.avt_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(username_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(password_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addStretch(2)
        self.setLayout(layout)

    def login(self):
        email = self.username_input.text()
        password = self.password_input.text()
        if self.check_user_pass(email, password):
            self.user_info = self.get_user_info(email)
            if self.check_if_librarian(email):
                self.open_admin_interface()
            else:
                self.open_user_interface()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Please try again.")
    

    def check_user_pass(self, email, password):
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
            cursor.execute("SELECT email, password FROM account WHERE email = %s AND password = %s", (email, password))
            result = cursor.fetchone()
            return result is not None
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    def check_if_librarian(self, email):
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
            cursor.execute("SELECT email FROM librarian WHERE email = %s", (email,))
            result = cursor.fetchone()
            return result is not None
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_user_info(self, email):
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

            # Truy vấn thông tin từ bảng student
            cursor.execute("""
                SELECT email, first_name, last_name, dob, gender, email, phone_number 
                FROM student 
                WHERE email = %s
            """, (email,))
            result = cursor.fetchone()

            if result:
                return {
                    'email': result[0],
                    'first_name': result[1],
                    'last_name': result[2],
                    'dob': result[3],
                    'gender': result[4],
                    'phone_number': result[5]
                }
            else:
                # Nếu không tìm thấy trong bảng student, truy vấn thông tin từ bảng librarian
                cursor.execute("""
                    SELECT email, first_name, last_name, dob, gender, email, phone_number 
                    FROM librarian 
                    WHERE email = %s
                """, (email,))
                result = cursor.fetchone()
                if result:
                    return {
                        'email': result[0],
                        'first_name': result[1],
                        'last_name': result[2],
                        'dob': result[3],
                        'gender': result[4],
                        'phone_number': result[5]
                    }
                else:
                    return None
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error)
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()
    def open_admin_interface(self):
        self.admin_window = admin_home()
        self.admin_window.show()
        self.close()

    def open_user_interface(self):
        self.user_window = HomeWindow_user(self.user_info)
        self.user_window.show()
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(style_sheet)
    window = LoginWindow()
    sys.exit(app.exec())