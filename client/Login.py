import sys
import time
from PySide6 import QtCore, QtWidgets
from ui.login_ui import Ui_Form
import json
from concurrent.futures import ThreadPoolExecutor


# 登录多线程
class LoginThread(QtCore.QObject):
    finished = QtCore.Signal(bool)

    def __init__(self, client, data):
        super().__init__()
        self.client = client
        self.data = data

    def run(self):
        login_result = self.client.login_request(self.data)
        if login_result:
            self.finished.emit(True)
        else:
            self.finished.emit(False)


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
        # 禁用登录按钮，避免重复登录
        self.ui.pushButton.setEnabled(False)
        # 获取数据
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        request_data = {"username":username, "password":password}
        request_data = json.dumps(request_data)
        # 启动后台线程执行登录操作
        self.thread_pool = ThreadPoolExecutor()
        self.login_thread = LoginThread(self.main.client, request_data)
        self.login_thread.finished.connect(self.do_login_finished)
        self.thread_pool.submit(self.login_thread.run)

    # 登录多线程返回触发
    def do_login_finished(self, result):
        if result:
            QtWidgets.QMessageBox.information(self, 'information', 'login success')
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.main.login_ui.close()
            self.main.index_ui.show()
        else:
            QtWidgets.QMessageBox.warning(self, 'warning', 'user or password uncorrect')
        self.ui.pushButton.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Login("")
    widget.show()
    sys.exit(app.exec())
