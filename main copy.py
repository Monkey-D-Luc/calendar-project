import sqlite3

from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox,QMainWindow,QLabel,QTimeEdit
from PyQt5.QtCore import QTime,Qt
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QFont

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng ký")
        self.setGeometry(750, 400, 500, 350)
        self.error_message = QLabel()
        self.error_message.setStyleSheet("color: red")
        self.loginWindow = LoginWindow()

        layout = QVBoxLayout()

        self.username_label = QLabel("Tên người dùng:")
        self.username_textbox = QLineEdit()
        self.password_label = QLabel("Mật khẩu:")
        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.register)
        font=QFont()
        font.setPointSize(12)
        self.username_label.setFont(font)
        self.username_textbox.setFont(font)
        self.password_label.setFont(font)
        self.password_textbox.setFont(font)
        self.register_button.setFont(font)

        self.setStyleSheet("background-color: #F0F0F0;")
        self.username_textbox.setStyleSheet("background-color: #FFFFFF;")
        self.password_textbox.setStyleSheet("background-color: #FFFFFF:")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.back_button = QPushButton("Quay lại")
        self.back_button.clicked.connect(self.BackToLogin)

        layout.addWidget(self.back_button)
        layout.addWidget(self.username_label,alignment =Qt.AlignHCenter)
        layout.addWidget(self.username_textbox)
        layout.addWidget(self.password_label,alignment =Qt.AlignHCenter)
        layout.addWidget(self.password_textbox)
        layout.addWidget(self.register_button,alignment =Qt.AlignHCenter)
        layout.addWidget(self.error_message)

        self.setLayout(layout)

    def register(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()
        if username and password:
            if self.check_username_available(username):
                self.save_account(username, password)
                QMessageBox.information(self, "Thành công", "Tài khoản đã được tạo thành công.")
                self.close()
            else:
                self.error_message.setText("Tên người dùng đã tồn tại.")
        else:
            self.error_message.setText("Hãy điền vào tất cả các trường.")

    def check_username_available(self, username):
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM accounts WHERE username = ?")
        query.bindValue(0, username)
        query.exec_()
        query.next()
        return query.value(0) == 0

    def save_account(self, username, password):
        query = QSqlQuery()
        query.prepare("INSERT INTO accounts (username, password) VALUES (?, ?)")
        query.bindValue(0, username)
        query.bindValue(1, password)
        query.exec_()


    def BackToLogin(self):
        self.close()
        self.loginWindow = LoginWindow()
        self.loginWindow.show()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.setGeometry(750, 400, 500, 350)

        layout = QVBoxLayout()

        self.username_label = QLabel("Tên người dùng:")
        self.username_textbox = QLineEdit()
        self.password_label = QLabel("Mật khẩu:")
        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Đăng nhập")
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.show_register_window)
        self.error_message =QLabel()
        self.error_message.setStyleSheet("color:red")

        self.login_button.setStyleSheet("background-color: #0033CC; color:white;")
        self.setStyleSheet("background-color: #F0F0F0;")
        self.username_textbox.setStyleSheet("background-color: #FFFFFF;")
        self.password_textbox.setStyleSheet("background-color: #FFFFFF:")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white;")
        font = QFont()
        font.setPointSize(12)

        self.username_label.setFont(font)
        self.username_textbox.setFont(font)
        self.password_label.setFont(font)
        self.password_textbox.setFont(font)
        self.login_button.setFont(font)
        self.register_button.setFont(font)

        layout.addWidget(self.username_label,alignment =Qt.AlignHCenter)
        layout.addWidget(self.username_textbox)
        layout.addWidget(self.password_label,alignment =Qt.AlignHCenter)
        layout.addWidget(self.password_textbox)
        layout.addWidget(self.login_button,alignment =Qt.AlignHCenter)
        layout.addWidget(self.register_button,alignment =Qt.AlignHCenter)
        layout.addWidget(self.error_message)

        self.setLayout(layout)

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


class Window(QMainWindow):
    def __init__(self, username):
        super(Window, self).__init__()
        loadUi("UI.ui", self)
        self.setFixedSize(1020, 800)
        self.move(300, 0)

        self.label = self.findChild(QLabel, "label")

        self.username = username

        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)

    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate().strftime("%d-%m-%y")
        self.label_4.setText(dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.tasksListWidget.clear()

        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE date = ? AND username = ?"
        row = (date, self.username)
        results = cursor.execute(query, row).fetchall()

        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)


    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%d-%m-%y")

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ? AND username = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ? AND username = ?"
            row = (task, date, self.username)
            cursor.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%d-%m-%y")
        newTask = str(self.taskLineEdit.text())
        ti =str(self.timeIn.text())
        to =str(self.timeOut.text())
        query = "INSERT INTO tasks(task, completed, date, timein, timeout, username) VALUES (?,?,?,?,?,?)"
        row = (newTask, "NO", date,ti,to, self.username)
        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Kết nối tới cơ sở dữ liệu SQLite
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("data.db")
    if not database.open():
        QMessageBox.warning(None, "Lỗi", "Không thể kết nối tới cơ sở dữ liệu.")
        sys.exit(1)

    # Tạo bảng 'accounts' nếu chưa tồn tại
    create_query = QSqlQuery()
    create_query.exec_("CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, password TEXT)")

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
