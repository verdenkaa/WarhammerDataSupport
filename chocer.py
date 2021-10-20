import sys
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class RasaChoice(QMainWindow):
    def __init__(self, forback, std_db):
        super().__init__()
        uic.loadUi('ui/choser.ui', self)
        self.forback = forback
        self.std_db = std_db
        # Создание нужных для работы переменных со стартовыми значениями
        self.rases = ["marines", "necrons", "bubonic", "orcs"]
        self.StartUnit = [0, 6, 6, 13, 13, 100, 20, 100, 0]
        # Подключение защиты от дурака, доступен ввод только чисел в диапазоне от 0 до 999
        self.lineEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_2.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_3.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_4.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_5.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_6.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_7.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_8.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_9.setValidator(QtGui.QIntValidator(0, 999))
        self.lineEdit_10.setValidator(QtGui.QIntValidator(0, 999))
        # Подключение функционала кнопок и чекеров
        self.pushButton_2.clicked.connect(self.helper)
        self.pushButton_3.clicked.connect(self.backtomenu)
        self.pushButton.clicked.connect(self.startsorting)
        self.checkBox.stateChanged.connect(lambda: self.addrace(self.checkBox, "marines", 0))
        self.checkBox_2.stateChanged.connect(lambda: self.addrace(self.checkBox_2, "necrons", 1))
        self.checkBox_3.stateChanged.connect(lambda: self.addrace(self.checkBox_3, "bubonic", 2))
        self.checkBox_4.stateChanged.connect(lambda: self.addrace(self.checkBox_4, "orcs", 3))
        
    def helper(self):
        # Функция для вызова окна помощи
        self.helpwindow = Helper()
        self.helpwindow.setWindowTitle('Warhammer Data Support')
        self.helpwindow.setWindowIcon(QIcon('ui\images\icon.png'))
        self.helpwindow.show()

    def addrace(self, checker, rase, number):
        # Добавлене и удаление разных рас в учет при сортировке
        if checker.isChecked():
            self.rases[number] = rase
        else:
            self.rases[number] = "NoneRacePleaceInore"

    def backtomenu(self):
        self.hide()
        self.forback.setWindowTitle('Warhammer Data Support')
        self.forback.setWindowIcon(QIcon('ui\images\icon.png'))
        self.forback.show()

    def startsorting(self):
        print(self.rases)

class Helper(QMainWindow):
    # Класс окна помощи
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\help.ui', self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)