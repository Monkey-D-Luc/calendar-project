import sqlite3

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout,QLabel, QLineEdit
from PyQt5.QtGui import QFont

class ExtraWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(1020, 800)
        self.move(300, 0)
        self.parent = parent
        self.back_btn = QPushButton("Quay lại", self)
        self.back_btn.clicked.connect(self.BackToParent)
    
    def BackToParent(self):
        self.parent.show()
        self.hide()

    # def closeEvent(self, event):
    #     self.parent.close()

class AccoutInfoWindow(ExtraWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.contentBox = QWidget()
        self.setCentralWidget(self.contentBox)
        self.contentBox.setFixedSize(800, 800)
        # self.contentBox.move(500, 500)
        grid = QGridLayout()
        self.back_btn.setStyleSheet("font-size: 20px; height: 25px; width: 100px; margin-right: 100px")
        grid.addWidget(self.back_btn, 0, 0)
        self.username_label = QLabel("Tên đăng nhập:")
        self.username_textbox = QLineEdit()
        self.password_label = QLabel("Mật khẩu:")
        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.fullname_label = QLabel("Họ và tên:")
        self.fullname_textbox = QLineEdit()
        self.phone_label = QLabel("Số điện thoại:")
        self.phone_textbox = QLineEdit()
        self.email_label = QLabel("Địa chỉ email:")
        self.email_textbox = QLineEdit()
        self.register_button = QPushButton("Đăng ký")
        #self.register_button.clicked.connect(self.register)
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

        self.setStyleSheet("background-color: qlineargradient(y1: 0, y2 : 1, stop: 0 #74b9ff, stop: 1 #6c5ce7);")

        self.username_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.password_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.fullname_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.phone_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.email_textbox.setStyleSheet("background-color: white; height: 30px; margin-bottom: 10px;")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; height: 30px;")
        self.back_button = QPushButton("Quay lại")
        #self.back_button.clicked.connect(self.BackToLogin)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("background-color: #d63031; color: white; height: 30px;")
        self.username_label.setStyleSheet("background-color: transparent")
        self.password_label.setStyleSheet("background-color: transparent")
        self.fullname_label.setStyleSheet("background-color: transparent")
        self.phone_label.setStyleSheet("background-color: transparent")
        self.email_label.setStyleSheet("background-color: transparent")
        #self.error_message.setStyleSheet("background-color: transparent; font-size: 20px; color: yellow")
        
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        query = "SELECT * FROM accounts WHERE username = ?"
        row = (parent.GetUsername(),)
        results = cursor.execute(query, row).fetchall()
        
        self.username_textbox.setText(results[0][0])
        self.password_textbox.setText(results[0][1])
        self.fullname_textbox.setText(results[0][2])
        self.phone_textbox.setText(results[0][3])
        self.email_textbox.setText(results[0][4])
        self.username_textbox.setReadOnly(True)
        self.password_textbox.setReadOnly(True)

        grid.addWidget(self.username_label, 1, 3)
        grid.addWidget(self.username_textbox, 1, 4)
        grid.addWidget(self.password_label,2, 3)
        grid.addWidget(self.password_textbox,2, 4)
        grid.addWidget(self.fullname_label, 3, 3)
        grid.addWidget(self.fullname_textbox, 3, 4)
        grid.addWidget(self.phone_label, 4, 3)
        grid.addWidget(self.phone_textbox, 4, 4)
        grid.addWidget(self.email_label, 5, 3)
        grid.addWidget(self.email_textbox, 5, 4)

        self.contentBox.setLayout(grid)

class PlanWindow(ExtraWindow):
    def __init__(self, parent):
        super().__init__(parent)