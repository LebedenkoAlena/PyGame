import sys
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui, QtCore
from un import Ui_mainWindow
from Tile import Game


class Generate(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_1.clicked.connect(self.bt)
        self.pushButton_2.clicked.connect(self.bt)
        self.pushButton_3.clicked.connect(self.bt)
        self.pushButton_4.clicked.connect(self.bt)
        self.pushButton_5.clicked.connect(self.bt)
        self.pushButton_6.clicked.connect(self.bt)
        self.pushButton_7.clicked.connect(self.bt)
        self.pushButton_8.clicked.connect(self.bt)
        self.pushButton_9.clicked.connect(self.bt)
        self.pushButton_10.clicked.connect(self.bt)
        self.pushButton_11.clicked.connect(self.bt)
        self.pushButton_12.clicked.connect(self.bt)
        self.pushButton_13.clicked.connect(self.bt)
        self.pushButton_14.clicked.connect(self.bt)
        self.pushButton_15.clicked.connect(self.bt)
        self.pushButton_16.clicked.connect(self.bt)
        self.pushButton_17.clicked.connect(self.bt)
        self.pushButton_18.clicked.connect(self.bt)
        self.pushButton_19.clicked.connect(self.bt)
        self.pushButton_20.clicked.connect(self.bt)
        self.pushButton_21.clicked.connect(self.bt)
        self.pushButton_22.clicked.connect(self.bt)
        self.pushButton_23.clicked.connect(self.bt)
        self.pushButton_24.clicked.connect(self.bt)
        self.pushButton_25.clicked.connect(self.bt)
        self.pushButton_26.clicked.connect(self.bt)
        self.pushButton_27.clicked.connect(self.bt)
        self.pushButton_28.clicked.connect(self.bt)
        self.pushButton_29.clicked.connect(self.bt)
        self.pushButton_30.clicked.connect(self.run)


    def run(self):
        self.init_pygame()

    def bt(self):
        print(self.sender().text())

    def init_pygame(self):
        self.game = Game()
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(10)

    def pygame_loop(self):
        if self.game.loop(self):
            self.timer.stop()
            self.timer.disconnect()
            pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Generate()
    ex.show()
    sys.exit(app.exec_())
