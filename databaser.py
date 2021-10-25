import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QTableView, QApplication, QMainWindow, QApplication, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel
import sqlite3


class Dater(QMainWindow):
    def __init__(self, forback, std_db):
        super().__init__()
        uic.loadUi('ui\databaser.ui', self)
        self.con = sqlite3.connect("db\off_units.sqlite")       #подключаем БД
        # Создание курсора
        self.cur = self.con.cursor()
        self.datasheets = self.cur.execute("""SELECT * FROM unit_datasheet
            WHERE name != '  '""").fetchall() #получаем данные в виде списка кортежей
        self.table_creator()
        self.forback = forback
        self.std_db = std_db
        # Подключаем выход обратно в меню
        self.pushButton.clicked.connect(self.back)

        self.pushButton_2.clicked.connect(self.helper)

    def table_creator(self):
        self.tables.setColumnCount(15)     # Устанавливаем нужное кол-во колонок
        self.tables.setRowCount(len(self.datasheets))        # и количество элементов в таблице

        # Устанавливаем заголовки таблицы
        self.tables.setHorizontalHeaderLabels(['Name', 'Type', 'Rase', 'Power', 'Points', 'Move', 'Weapon Skill', 'Ballistic Skill', 'Strength', 'Toughness', 'Wound', 'Attacs', 'Leadership', 'Save', 'Look'])

        # заполняем столбцы
        for i in range(len(self.datasheets)):
            for j in range(len(self.datasheets[i])):
                if self.datasheets[i][j] != self.datasheets[i][-1]:
                    self.tables.setItem(i, j, QTableWidgetItem(str(self.datasheets[i][j])))
                else:
                    image = QLabel(self)
                    pix = QPixmap(str(self.datasheets[i][j]))
                    _size = QSize(200, 100) 
                    image.setPixmap(pix.scaled(_size, Qt.KeepAspectRatio))
                    self.tables.setCellWidget(i, j, image)


        # делаем ресайз колонок по содержимому
        self.tables.resizeColumnsToContents()

    def back(self):
        self.hide()
        self.forback.setWindowTitle('Warhammer Data Support')
        self.forback.setWindowIcon(QIcon('ui\images\icon.png'))
        self.forback.show()

    def helper(self):
        # Функция для вызова окна помощи
        self.helpwindow = Helper()
        self.helpwindow.setWindowTitle('Warhammer Data Support')
        self.helpwindow.setWindowIcon(QIcon('ui\images\icon.png'))
        self.helpwindow.show()



class Helper(QMainWindow):
    # Класс окна помощи
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\help.ui', self)
