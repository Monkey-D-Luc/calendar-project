from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Login import LoginWindow
import sys


styleSheet = '''
#Drop{
    color: white;

}
#Drop:hover{
    background-color: #636e72;
}
#MenuD{
    background-color: black;
    color: white;
    font-size: 30px;
}
#MenuD:selected{
    background-color: #636e72;
}
#SAWindow{
    background-image: url(bg.png);
}
#AccoutInfoBtn{
    font-size: 20px; height: 40px; 
    width: 200px; 
    margin-right: 100px;
    margin-left: 50px;
    color: black;
    background-color: #ffeaa7;
}
#CPTextBox{
    height: 30px;
    margin-bottom: 30px;
}
#CPLabel{
    margin-bottom: 30px;
}
#CPBtn{
    height: 40px;
    font-size: 30px;
}

'''





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)

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
