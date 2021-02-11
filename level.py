import sys
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui, QtCore
from un import Ui_mainWindow

level_location = 'leval_1.txt'
numder = 0


class Generate(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # чтение файла с максимальным пройденным уровнем
        with open('levels_unblock.txt', mode='r') as block:
            levels = list(map(int, block.read().split()))
        # объявление кнопок и их функций
        for i in range(1, 17):
            if len(levels) == 0:
                self.pushButton_1.clicked.connect(self.bt)
            elif i <= levels[-1] + 1:
                exec(f'self.pushButton_{i}.clicked.connect(self.bt)')
            else:
                exec(f'self.pushButton_{i}.setEnabled(False)')

    # изменение значений глобальных переменных и закрытие  Qt-окна
    def bt(self):
        global level_location, numder
        numder = self.sender().text()
        level_location = f'leval_{self.sender().text()}.txt'
        self.close()

# функция возвращения значений (для использования их в основном игровом цикле)
def returning():
    return level_location, int(numder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Generate()
    ex.show()
    sys.exit(app.exec_())
