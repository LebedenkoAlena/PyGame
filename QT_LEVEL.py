import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, QtCore
from un import Ui_mainWindow


class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
