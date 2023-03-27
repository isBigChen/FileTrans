import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ui.index_ui import Ui_MainWindow
import ast

class Index(QtWidgets.QMainWindow):
    def __init__(self, main):
        super(Index, self).__init__()
        self.main = main
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.do_require_filelist)
        self.ui.pushButton_2.clicked.connect(self.do_download_file)

    # 请求下载文件
    def do_download_file(self):
        cur_file = self.ui.listWidget.currentItem().text()
        # print(cur_file)
        self.main.client.download_file(cur_file)

    # 请求文件列表
    def do_require_filelist(self):
        res = self.main.client.require_filelist()
        res = ast.literal_eval(res)
        for item in res:
            self.ui.listWidget.addItem(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Index("123")
    widget.show()
    sys.exit(app.exec())
