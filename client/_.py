import sys
import time
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, QThread, Qt, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginThread(QObject):
    finished = Signal(bool)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        # 模拟登录操作，这里用time.sleep()代替
        time.sleep(5)

        # 登录成功
        self.finished.emit(True)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        # 创建控件
        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        # 连接信号和槽
        self.login_button.clicked.connect(self.login)

    def login(self):
        # 禁用登录按钮，避免重复登录
        self.login_button.setEnabled(False)

        # 获取用户名和密码
        username = self.username_edit.text()
        password = self.password_edit.text()

        # 启动后台线程执行登录操作
        self.thread_pool = ThreadPoolExecutor()
        self.login_thread = LoginThread(username, password)
        self.login_thread.finished.connect(self.on_login_finished)
        self.thread_pool.submit(self.login_thread.run)

    def on_login_finished(self, success):
        # 启用登录按钮
        self.login_button.setEnabled(True)

        # 根据登录结果弹出消息框
        if success:
            QMessageBox.information(self, "Login", "Login successful!")
            self.accept()
        else:
            QMessageBox.warning(self, "Login", "Login failed!")

    def closeEvent(self, event: QCloseEvent):
        if self.thread_pool is not None:
            self.thread_pool.shutdown()
        event.accept()

def main():
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    login_dialog.exec_()
    sys.exit()

if __name__ == '__main__':
    main()
