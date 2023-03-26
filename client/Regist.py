import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.regist_ui import Ui_Form
import json

class Regist(QtWidgets.QWidget):
    def __init__(self, main):
        super(Regist, self).__init__()
        self.main = main
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.show_login)
        self.ui.pushButton.clicked.connect(self.do_regist)

    # 返回登录页面
    def show_login(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.main.regist_ui.close()
        self.main.login_ui.show()

    # 触发注册功能
    def do_regist(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        request_data = {"username": username, "password": password}
        request_data = json.dumps(request_data)
        # client socket
        regist_result = self.main.client.regist_request(request_data)
        if regist_result:
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.main.regist_ui.close()
            self.main.login_ui.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Regist("123")
    widget.show()
    sys.exit(app.exec())
