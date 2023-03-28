import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.regist_ui import Ui_Form
import json
from concurrent.futures import ThreadPoolExecutor


# 注册多线程
class RegistThread(QtCore.QObject):
    finished = QtCore.Signal(bool)

    def __init__(self, client, data):
        super().__init__()
        self.client = client
        self.data = data

    def run(self):
        regist_result = self.client.regist_request(self.data)
        if regist_result:
            self.finished.emit(True)
        else:
            self.finished.emit(False)


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
        # 启动后台线程执行登录操作
        self.thread_pool = ThreadPoolExecutor()
        self.regist_thread = RegistThread(self.main.client, request_data)
        self.regist_thread.finished.connect(self.do_regist_finished)
        self.thread_pool.submit(self.regist_thread.run)

    # 登录多线程返回触发
    def do_regist_finished(self, result):
        if result:
            QtWidgets.QMessageBox.information(self, 'information', 'regist success')
        else:
            QtWidgets.QMessageBox.information(self, 'information', 'regist failed')
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.main.regist_ui.close()
        self.main.login_ui.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Regist("123")
    widget.show()
    sys.exit(app.exec())
