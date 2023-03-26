import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.login_ui import Ui_Form


class Login(QtWidgets.QWidget):
    def __init__(self, main):
        super(Login, self).__init__()
        self.main = main
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.show_regist)
        self.ui.pushButton.clicked.connect(self.do_login)

    def show_regist(self):
        self.main.login_ui.close()
        self.main.regist_ui.show()

    def do_login(self):
        if True:
            self.main.login_ui.close()
            self.main.index_ui.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Login("123")
    widget.show()
    sys.exit(app.exec())
