import sqlite3

from PyQt5 import QtGui
from PyQt5.QtWidgets import  QFormLayout, QListWidget, QMainWindow, QPushButton, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QScrollArea
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDate

class ExtraWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(1020, 800)
        self.move(300, 0)
        self.setWindowIcon(QIcon("logo.png"))
        self.parent = parent
        self.back_btn = QPushButton("Quay lại", self)
        self.back_btn.clicked.connect(self.BackToParent)
    
    def BackToParent(self):
        self.parent.show()
        self.hide()

    # def closeEvent(self, event):
    #     self.parent.close()

class AccountInfoWindow(ExtraWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Thông tin tài khoản")
        self.contentBox = QWidget()
        self.setCentralWidget(self.contentBox)
        self.contentBox.setFixedSize(850, 700)
        # self.contentBox.move(500, 500)
        grid = QGridLayout()

        self.change_password_btn = QPushButton("Đổi mật khẩu")
        self.save_btn = QPushButton("Lưu thông tin")
        self.change_password_btn.setObjectName("AccoutInfoBtn")
        self.save_btn.setObjectName("AccoutInfoBtn")
        self.back_btn.setObjectName("AccoutInfoBtn")
        self.save_btn.clicked.connect(self.SaveInfo)
        self.change_password_btn.clicked.connect(self.ChangePassword)
        grid.addWidget(self.back_btn, 0, 0)
        grid.addWidget(self.change_password_btn, 1, 0)
        grid.addWidget(self.save_btn, 2, 0)
        
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

        self.setObjectName("SAWindow")

        self.username_textbox.setStyleSheet("background-color: #ffeaa7; height: 30px; margin-bottom: 10px; color: black; font-size: 20px;")
        self.password_textbox.setStyleSheet("background-color: #ffeaa7; height: 30px; margin-bottom: 10px; color: black; font-size: 20px;")
        self.fullname_textbox.setStyleSheet("background-color: #ffeaa7; height: 30px; margin-bottom: 10px; color: black; font-size: 20px;")
        self.phone_textbox.setStyleSheet("background-color: #ffeaa7; height: 30px; margin-bottom: 10px; color: black; font-size: 20px;")
        self.email_textbox.setStyleSheet("background-color: #ffeaa7; height: 30px; margin-bottom: 10px; color: black; font-size: 20px;")
        
        self.username_label.setStyleSheet("background-color: transparent; color: white; margin-bottom: 10px; font-size: 20px;")
        self.password_label.setStyleSheet("background-color: transparent; color: white; margin-bottom: 10px; font-size: 20px;")
        self.fullname_label.setStyleSheet("background-color: transparent; color: white; margin-bottom: 10px; font-size: 20px;")
        self.phone_label.setStyleSheet("background-color: transparent; color: white; margin-bottom: 10px; font-size: 20px;")
        self.email_label.setStyleSheet("background-color: transparent; color: white; margin-bottom: 10px; font-size: 20px;")
        
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

        grid.addWidget(self.username_label, 0, 3)
        grid.addWidget(self.username_textbox, 0, 4)
        grid.addWidget(self.password_label, 1, 3)
        grid.addWidget(self.password_textbox, 1, 4)
        grid.addWidget(self.fullname_label, 2, 3)
        grid.addWidget(self.fullname_textbox, 2, 4)
        grid.addWidget(self.phone_label, 3, 3)
        grid.addWidget(self.phone_textbox, 3, 4)
        grid.addWidget(self.email_label, 4, 3)
        grid.addWidget(self.email_textbox, 4, 4)

        self.contentBox.setLayout(grid)

    def SaveInfo(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        fullname = self.fullname_textbox.text()
        phone = self.phone_textbox.text()
        email = self.email_textbox.text()
        query = "UPDATE accounts SET fullname = ?, phone = ?, email = ? WHERE username = ?"
        row = (fullname, phone, email, self.parent.GetUsername(),)
        cursor.execute(query, row)
        db.commit()
        QMessageBox.information(self.parent, "Thông báo", "Thay đổi đã được lưu")

    def ChangePassword(self):
        self.changeWindow = ChangePasswordWindow(self.parent.GetUsername())
        self.changeWindow.show()
        
class PlanWindow(ExtraWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Kế hoạch chung")
        self.setObjectName("PWindow")
        self.InitUI()

    def InitUI(self):
        self.addtasks_btn = QPushButton("Thêm kế hoạch", self)
        self.addtasks_btn.clicked.connect(self.OpenAddTasksWindow)

        self.back_btn.setObjectName("PBtn")
        self.addtasks_btn.setObjectName("PBtn")

        self.back_btn.move(50, 50)
        self.addtasks_btn.move(300, 50)
        self.back_btn.resize(150, 50)
        self.addtasks_btn.resize(150, 50)

        
        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(50, 200, 920, 550)
        scroll_area.horizontalScrollBar().setEnabled(False)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # data = [
        #     ("10 - 11 - 2023", ["Công nghệ phần mềm - Chương 1: Xác định yêu cầu", "Công nghệ phần mềm - Chương 2: Đặc tả", "Công nghệ phần mềm - Chương 3: Thiết kế"]),
        #     ("11 - 11 - 2023", ["Công nghệ phần mềm - Chương 4: Cài đặt", "Công nghệ phần mềm - Chương 5: tích hợp", "Công nghệ phần mềm - Chương 6: Bảo trì"]),
        #     ("12 - 11 - 2023", ["Công nghệ phần mềm - Chương 7: Thôi sử dụng","a","a","a","a","a","a","a","a","a","a","a","a","a"]),
        # ]

        data = self.fetch_data_from_database()

        for date, tasks in data:
            label = self.create_task_label(date, tasks)
            scroll_layout.addWidget(label)

        scroll_area.setWidget(scroll_content)

    def OpenAddTasksWindow(self):
        self.hide()
        self.addTasksWindow = AddTasksWindow(self)
        self.addTasksWindow.show()

    def create_task_label(self, date, tasks):
        label = QLabel()
        font = QFont("Arial", 14)  # Chọn phông chữ và kích thước lớn hơn

        text = f"<h3 style='background-color: lightblue; width: 920px;'><span style='background-color: lightblue; color: black'>____________{date}________________________________________________</span></h3><ul style='font-size: 20px'>"
        i = 0
        for task in tasks:
            if i % 2 != 0:
                text += f"<li style='background-color: #fdcb6e;'>_____________{task}________________________________________________________________</li>"
            else:
                text += f"<li style='background-color: #ffeaa7;'>_____________{task}________________________________________________________________</li>"
            i += 1
        text += "</ul>"

        label.setText(text)
        label.setFont(font)  # Đặt phông chữ cho label
        label.resize(700, 50)
        return label

    def fetch_data_from_database(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Truy vấn dữ liệu từ bảng plans
        cursor.execute("SELECT date, task FROM plans ORDER BY stt")
        rows = cursor.fetchall()

        connection.close()

        data = {}
        for date, task in rows:
            if date not in data:
                data[date] = []
            data[date].append(task)

        result = [(date, tasks) for date, tasks in data.items()]
        return result




class ChangePasswordWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.InitUI()

    def InitUI(self):
        self.move(500, 300)
        self.setFixedSize(500, 300)
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Thay đổi mật khẩu")
        layout = QGridLayout()
        self.old_password_label = QLabel("Mật khẩu cũ: ")
        self.new_password_label = QLabel("Mật khẩu mới")
        self.retype_label = QLabel("Nhập lại mật khẩu: ")
        self.old_password_textbox = QLineEdit()
        self.new_password_textbox = QLineEdit()
        self.retype_textbox = QLineEdit()

        self.old_password_textbox.setEchoMode(QLineEdit.Password)
        self.new_password_textbox.setEchoMode(QLineEdit.Password)
        self.retype_textbox.setEchoMode(QLineEdit.Password)

        self.old_password_label.setObjectName("CPLabel")
        self.new_password_label.setObjectName("CPLabel")
        self.retype_label.setObjectName("CPLabel")
        self.old_password_textbox.setObjectName("CPTextBox")
        self.new_password_textbox.setObjectName("CPTextBox")
        self.retype_textbox.setObjectName("CPTextBox")

        self.error_message = QLabel()
        self.error_message.setStyleSheet("color: red;")

        self.cancel_btn = QPushButton("Huỷ")
        self.confirm_btn = QPushButton("Xác nhận")

        self.cancel_btn.setFixedSize(120, 40)
        self.confirm_btn.setFixedSize(120, 40)
        self.cancel_btn.setObjectName("QPBtn")
        self.confirm_btn.setObjectName("QPBtn")

        self.cancel_btn.clicked.connect(self.close)
        self.confirm_btn.clicked.connect(self.SaveChange)
        

        font = QFont("Arial", 10)
        
        self.old_password_label.setFont(font)
        self.new_password_label.setFont(font)
        self.retype_label.setFont(font)
        self.cancel_btn.setFont(font)
        self.confirm_btn.setFont(font)
        self.error_message.setFont(font)


        hbox = QHBoxLayout()
        hbox.addWidget(self.cancel_btn, 0, Qt.AlignRight)
        hbox.addWidget(self.confirm_btn, 0, Qt.AlignRight)

        layout.addWidget(self.old_password_label, 0, 0)
        layout.addWidget(self.old_password_textbox, 0, 1)
        layout.addWidget(self.new_password_label, 1, 0)
        layout.addWidget(self.new_password_textbox, 1, 1)
        layout.addWidget(self.retype_label, 2, 0)
        layout.addWidget(self.retype_textbox, 2, 1)
        layout.addWidget(self.error_message,3, 1, Qt.AlignRight)
        layout.addLayout(hbox, 4, 1)
        
        self.setLayout(layout)
    
    def SaveChange(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        oldPassword = self.old_password_textbox.text()
        newPassword = self.new_password_textbox.text()
        retypePassword = self.retype_textbox.text()

        if oldPassword and newPassword and retypePassword:
            query = "SELECT password FROM accounts WHERE username = ?"
            row = (self.username)
            oldPasswordInDB = cursor.execute(query, row).fetchone()[0]
            if oldPassword != oldPasswordInDB:
                self.error_message.setText("Mật khẩu cũ không chính xác!")
            elif retypePassword == newPassword:
                query = "UPDATE accounts SET password = ? WHERE username = ?"
                row = (newPassword, self.username)
                cursor.execute(query, row)
                db.commit()
                QMessageBox.information(self, "Thành công", "Thay đổi mật khẩu thành công")
                self.close()
            else:
                self.error_message.setText("Mật khẩu không trùng khớp!")
        else:
            self.error_message.setText("Hãy nhập đầy đủ các trường")

class AddTasksWindow(QMainWindow):
    def __init__(self, previusWindow):
        super().__init__()
        self.setWindowTitle("Add Tasks")
        self.setGeometry(100, 100, 400, 400)

        self.previusWindow = previusWindow
        
        # Database connection
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        
        self.initUI()
    
    def initUI(self):
        # Date input fields
        date_label = QLabel("Ngày:")
        self.day_input = QLineEdit()
        self.month_input = QLineEdit()
        self.year_input = QLineEdit()
        
        # Task list
        self.task_list = QListWidget()
        
        # Add Task button
        add_task_button = QPushButton("Hiện nhiệm vụ")
        add_task_button.clicked.connect(self.add_task)
        
        # Delete Task button
        delete_task_button = QPushButton("Xoá nhiệm vu")
        delete_task_button.clicked.connect(self.delete_task)
        
        # New Task input field
        new_task_label = QLabel("Nhiệm vụ mới:")
        self.new_task_input = QLineEdit()
        
        # Add New Task button
        add_new_task_button = QPushButton("Thêm")
        add_new_task_button.clicked.connect(self.add_new_task)
        
        # Layout
        form_layout = QFormLayout()
        form_layout.addRow(date_label, self.day_input)
        form_layout.addRow(QLabel("Tháng:"), self.month_input)
        form_layout.addRow(QLabel("Năm:"), self.year_input)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(add_task_button)
        hbox1.addWidget(delete_task_button)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(new_task_label)
        hbox2.addWidget(self.new_task_input)
        
        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        vbox.addWidget(self.task_list)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(add_new_task_button)
        
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def add_task(self):
        day = self.day_input.text()
        month = self.month_input.text()
        year = self.year_input.text()
        selected_date = f"{day}-{month}-{year}"
        
        # Fetch tasks for the selected date
        self.cursor.execute("SELECT task FROM plans WHERE date=?", (selected_date,))
        tasks = self.cursor.fetchall()
        
        self.task_list.clear()
        for task in tasks:
            self.task_list.addItem(task[0])
    
    def delete_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            task_to_delete = selected_task.text()
            
            # Delete the selected task
            self.cursor.execute("DELETE FROM plans WHERE task=?", (task_to_delete,))
            self.conn.commit()
            self.add_task()  # Refresh task list
    
    def add_new_task(self):
        day = self.day_input.text()
        month = self.month_input.text()
        year = self.year_input.text()
        selected_date = QDate(int(year), int(month), int(day))
        
        new_task = self.new_task_input.text()
        
        if day and month and year and new_task:
            # Calculate 'stt' based on the selected date
            #selected_date = datetime.strptime(selected_date, "%d-%m-%y")
            reference_date = QDate(2020, 1, 1)
            stt = reference_date.daysTo(selected_date)
            selected_date = f"{day}-{month}-{year}"
            
            # Insert the new task into the database
            self.cursor.execute("INSERT INTO plans (stt, date, task) VALUES (?, ?, ?)", (stt, selected_date, new_task))
            self.conn.commit()
            self.new_task_input.clear()
            self.add_task()  # Refresh task list

    def closeEvent(self, event):
        self.previusWindow.InitUI()
        self.previusWindow.show()