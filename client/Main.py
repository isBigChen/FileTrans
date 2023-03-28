import sys
from PySide6 import QtWidgets
from Index import Index
from Login import Login
from Regist import Regist
from Client import *

SERVER_IP = "192.168.218.129"
SERVER_PORT = 6666


class Main():
    def __init__(self):
        super(Main, self).__init__()

        # 初始化server_socket
        self.client = Client(SERVER_IP, SERVER_PORT)

        # 初始化页面集合
        self.login_ui = Login(self)
        self.regist_ui = Regist(self)
        self.index_ui = Index(self)

        # 显示登录页面
        self.login_ui.show()


if __name__ == "__main__":
    # 初始化app
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

    # 创建窗口，并执行
    main = Main()
    resutl = app.exec()

    # 退出之前析构
    del main
    sys.exit(resutl)