from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery
from PyQt5 import QtGui



from MainWindow import Window

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng ký")
        self.setGeometry(550, 300, 500, 350)
        self.setFixedSize(500, 350)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.error_message = QLabel()
        self.error_message.setStyleSheet("color: red")
        self.loginWindow = LoginWindow()

        layout = QVBoxLayout()

        self.username_label = QLabel("Tên đăng nhập:")
        self.username_textbox = QLineEdit()
        self.password_label = QLabel("Mật khẩu:")
        self.password_textbox = QLineEdit()
        self.password_textbox.setText("Mật khẩu")
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.fullname_label = QLabel("Họ và tên:")
        self.fullname_textbox = QLineEdit()
        self.phone_label = QLabel("Số điện thoại:")
        self.phone_textbox = QLineEdit()
        self.email_label = QLabel("Địa chỉ email:")
        self.email_textbox = QLineEdit()
        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.register)
        font=QFont()
        font.setPointSize(12)
        self.username_label.setFont(font)
        self.username_textbox.setFont(font)
        self.password_label.setFont(font)
        self.password_textbox.setFont(font)
        self.fullname_label.setFont(font)
        self.fullname_textbox.setFont(font)
        self.phone_label.setFont(font)
        self.phone_textbox.setFont(font)
        self.email_label.setFont(font)
        self.email_textbox.setFont(font)
        self.register_button.setFont(font)

        self.setStyleSheet("background-color: qlineargradient(y1: 0, y2 : 1, stop: 0 #74b9ff, stop: 1 #6c5ce7); border-radius: 10px;")

        self.username_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.password_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.fullname_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.phone_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.email_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; height: 30px;")
        self.back_button = QPushButton("Quay lại")
        self.back_button.clicked.connect(self.BackToLogin)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("background-color: #d63031; color: white; height: 30px;")
        self.username_label.setStyleSheet("background-color: transparent")
        self.password_label.setStyleSheet("background-color: transparent")
        self.fullname_label.setStyleSheet("background-color: transparent")
        self.phone_label.setStyleSheet("background-color: transparent")
        self.email_label.setStyleSheet("background-color: transparent")
        self.error_message.setStyleSheet("background-color: transparent; font-size: 20px; color: yellow")

        grid = QGridLayout()
        grid.addWidget(self.username_label, 0, 0)
        grid.addWidget(self.username_textbox, 0, 1)
        grid.addWidget(self.password_label)
        grid.addWidget(self.password_textbox)
        grid.addWidget(self.fullname_label)
        grid.addWidget(self.fullname_textbox)
        grid.addWidget(self.phone_label)
        grid.addWidget(self.phone_textbox)
        grid.addWidget(self.email_label)
        grid.addWidget(self.email_textbox)
        layout.addLayout(grid)

        hbox = QHBoxLayout()
        hbox.addWidget(self.back_button)
        hbox.addWidget(self.register_button)
        layout.addLayout(hbox)
        layout.addWidget(self.error_message)

        self.setLayout(layout)

    def register(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()
        fullname = self.fullname_textbox.text()
        phone = self.phone_textbox.text()
        email = self.email_textbox.text()
        if username and password:
            if self.check_username_available(username):
                self.save_account(username, password, fullname, phone, email)
                messageBox = QMessageBox()
                messageBox.setText("Tài khoản đã được tạo thành công.")
                messageBox.setWindowIcon(QtGui.QIcon('logo.png'))
                messageBox.setStandardButtons(QMessageBox.Ok)
                messageBox.setIcon(QMessageBox.Information)
                messageBox.setWindowTitle("Thông báo")
                messageBox.exec()
                self.BackToLogin()
            else:
                self.error_message.setText("Tên đăng nhập đã tồn tại.")
        else:
            self.error_message.setText("Tên đăng nhập và mật khẩu không thể bỏ trống!")

    def check_username_available(self, username):
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM accounts WHERE username = ?")
        query.bindValue(0, username)
        query.exec_()
        query.next()
        return query.value(0) == 0

    def save_account(self, username, password, fullname, phone, email):
        query = QSqlQuery()
        query.prepare("INSERT INTO accounts (username, password, fullname, phone, email) VALUES (?, ?, ?, ?, ?)")
        query.bindValue(0, username)
        query.bindValue(1, password)
        query.bindValue(2, fullname)
        query.bindValue(3, phone)
        query.bindValue(4, email)
        query.exec_()


    def BackToLogin(self):
        self.close()
        self.loginWindow = LoginWindow()
        self.loginWindow.show()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.setGeometry(550, 300, 500, 350)
        self.setFixedSize(500, 400)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        windowLayout = QVBoxLayout()
        frame = QFrame(self)
        frame.setStyleSheet("background-color: qlineargradient(y1: 0, y2 : 1, stop: 0 #74b9ff, stop: 1 #6c5ce7); border-radius: 10px;")
        windowLayout.addWidget(frame)
        layout = QVBoxLayout(frame)

        self.username_label = QLabel("Tên đăng nhập:")
        self.username_textbox = QLineEdit()
        self.password_label = QLabel("Mật khẩu:")
        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Đăng nhập")
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.show_register_window)
        self.error_message =QLabel()
        self.error_message.setStyleSheet("background-color: none; color: yellow; font-size: 20px;")

        self.login_button.setStyleSheet("background-color: #0033CC; color:white; margin-top: 30px; height: 50px;")
        self.setStyleSheet("background-color: #F0F0F0;")
        self.username_textbox.setStyleSheet("background-color: #FFFFFF; height: 40px; margin-top: 10px;")
        self.password_textbox.setStyleSheet("background-color: #FFFFFF; height: 40px;")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; height: 50px;")
        self.username_label.setStyleSheet("background-color: none")
        self.password_label.setStyleSheet("background-color: none")
        font = QFont()
        font.setPointSize(12)

        self.username_label.setFont(font)
        self.username_textbox.setFont(font)
        self.password_label.setFont(font)
        self.password_textbox.setFont(font)
        self.login_button.setFont(font)
        self.register_button.setFont(font)

        grid = QGridLayout()
        grid.setSpacing(30)
        grid.addWidget(self.username_label, 0, 0)
        grid.addWidget(self.username_textbox, 0, 1)
        grid.addWidget(self.password_label, 1, 0)
        grid.addWidget(self.password_textbox, 1, 1)
        layout.addLayout(grid)

        vbox = QVBoxLayout()
        vbox.setSpacing(30)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.register_button)
        vbox.addWidget(self.error_message)
        layout.addLayout(vbox)

        self.setLayout(windowLayout)

    def login(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()
        if username and password:
            if self.validate_login(username, password):
                QMessageBox.information(self, "Thành công", "Đăng nhập thành công.")
                self.close()
                self.window = Window(username)
                self.window.show()
            else:
                self.error_message.setText("Tên người dùng hoặc mật khẩu không đúng.")
        else:
            self.error_message.setText("Hãy điền vào tất cả các trường.")

    def show_register_window(self):
        self.close()
        self.register_window = RegisterWindow()
        self.register_window.show()

    def validate_login(self, username, password):
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM accounts WHERE username = ? AND password = ?")
        query.bindValue(0, username)
        query.bindValue(1, password)
        query.exec_()
        query.next()
        return query.value(0) == 1