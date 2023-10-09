import sqlite3

from PyQt5.QtWidgets import QListWidgetItem, QMessageBox,QMainWindow,QLabel, QAction, QMenu, QPushButton
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5 import QtCore
from datetime import datetime

from ExtraWindow import AccountInfoWindow, PlanWindow

class Window(QMainWindow):
    def __init__(self, username):
        super(Window, self).__init__()
        loadUi("UI.ui", self)
        self.setFixedSize(1020, 800)
        self.move(300, 0)
        self.setWindowTitle("SeTTime")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.label = self.findChild(QLabel, "label")
        self.username = username
        
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)

        self.initMenu()
        self.plan_window = PlanWindow(self)
        self.accout_info_window = AccountInfoWindow(self)

        self.Notification()
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.Notification)
        self.timer.start()

    def GetUsername(self):
        return self.username

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
        messageBox.setText("Thay đổi đã được lưu.")
        messageBox.setWindowIcon(QtGui.QIcon('logo.png'))
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowTitle("Thông báo")
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

    def initMenu(self):
        # Tạo nút
        self.button = QPushButton( self)
        self.button.move(10, 20)
        self.button.setStyleSheet('border: 0px')
        self.button.setIcon(QIcon("menu.png"))
        self.button.setIconSize(QSize(50, 50))
        self.button.setObjectName("Drop")
        self.button.adjustSize()

        self.menu = Menu()
        self.menu.setObjectName("MenuD")

        action1 = QAction("Kế hoạch chung", self)
        action2 = QAction("Thông tin tài khoản", self)
        action1.triggered.connect(self.LoadPlanWindow)
        action2.triggered.connect(self.LoadAccoutInfoWindow)
        actions = {action1, action2}
        self.menu.addActions(actions)

        self.button.setMenu(self.menu)

    def LoadPlanWindow(self):
        self.hide()
        self.plan_window.show()


    def LoadAccoutInfoWindow(self):
        self.hide()
        self.accout_info_window.show()
        
    def Notification(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        now = datetime.now()
        time = now.strftime("%H:%M")
        date = now.strftime("%d-%m-%y")

        query = "SELECT date,timein,task FROM tasks WHERE username = ?"
        row = (self.username)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            if date==result[0] and time==result[1]:
                msg = QMessageBox()
                msg.setWindowTitle("Thông báo")
                msg.setWindowIcon(QtGui.QIcon('logo.png'))
                msg.setText(result[2])
                msg.setFixedSize(500,500)
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()

class Menu(QMenu):
    def __init__(self):
        super().__init__()
    
    def AddAction(self, actions):
        for action in actions:
            action.setObjectName("MenuD")
            self.addAction(action)
