import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.index_ui import Ui_MainWindow

class Index(QtWidgets.QMainWindow):
    def __init__(self, main):
        super(Index, self).__init__()
        self.main = main
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Index("123")
    widget.show()
    sys.exit(app.exec())
