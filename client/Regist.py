import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.regist_ui import Ui_Form

class Regist(QtWidgets.QWidget):
    def __init__(self, main):
        super(Regist, self).__init__()
        self.main = main
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.show_login)
        self.ui.pushButton.clicked.connect(self.do_regist)

    def show_login(self):
        self.main.regist_ui.close()
        self.main.login_ui.show()

    def do_regist(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Regist("123")
    widget.show()
    sys.exit(app.exec())
