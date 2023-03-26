import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.login_ui import Ui_Form
import json

class Login(QtWidgets.QWidget):
    def __init__(self, main):
        super(Login, self).__init__()
        self.main = main
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.show_regist)
        self.ui.pushButton.clicked.connect(self.do_login)

    # 跳转到注册页面
    def show_regist(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.main.login_ui.close()
        self.main.regist_ui.show()

    # 触发登录功能
    def do_login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        request_data = {"username":username, "password":password}
        request_data = json.dumps(request_data)
        # client socket
        login_result = self.main.client.login_request(request_data)
        # print(login_result)
        # 验证成功后跳转到主页面
        if login_result:
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.main.login_ui.close()
            self.main.index_ui.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Login("123")
    widget.show()
    sys.exit(app.exec())
