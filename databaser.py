from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLabel, QPushButton, QInputDialog
import sqlite3, logging


class Dater(QMainWindow):
    def __init__(self, forback, stddb=False):
        super().__init__()
        logging.basicConfig(filename = "logs.log", format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
        try:
            uic.loadUi('ui\databaser.ui', self)
        except:
            logging.error("Отсутствует databaser.ui")
        # Если база-тригер была изменена, считываем всю базу
        try:
            self.con = sqlite3.connect("db\off_units.sqlite") #подключаем БД
        except:
            logging.error("Отсутствует off_units.sqlite")
        if not stddb:    
            # Создание курсора
            self.cur = self.con.cursor()
            self.datasheets = self.cur.execute("""SELECT * FROM unit_datasheet
                WHERE name != '  '""").fetchall() #получаем данные в виде списка кортежей
            # Подключаем выход обратно в меню
        else:
            # Иначе подключаем готовую считаную и отсортированую базу в списке кортежей
            self.datasheets = stddb

        self.forback = forback
        self.table_creator()
        self.pushButton.clicked.connect(self.back)

        self.pushButton_2.clicked.connect(self.helper)

        self.clear_list_button.clicked.connect(self.clear_army_list)



    def table_creator(self):
        self.tables.setColumnCount(16)     # Устанавливаем нужное кол-во колонок
        self.tables.setRowCount(len(self.datasheets))        # и количество элементов в таблице

        # Устанавливаем заголовки таблицы
        self.tables.setHorizontalHeaderLabels(['Name', 'Type', 'Rase', 'Power', 'Points', 'Move', 'Weapon Skill', 'Ballistic Skill', 'Strength', 'Toughness', 'Wound', 'Attacs', 'Leadership', 'Save', 'Look', 'Add to my army list'])

        # заполняем столбцы
        self.button_list = [QPushButton('Добавить в список моей армии', self) for i in range(len(self.datasheets))]
        for i in range(len(self.datasheets)):
            for j in range(len(self.datasheets[i])):
                if self.datasheets[i][j] == self.datasheets[i][14]:  #проверка на 14 элемент, там должно быть изображение
                    image = QLabel(self)
                    pix = QPixmap('Unit_image/' + str(self.datasheets[i][j])) #Из списка с данными sql мы берем имя картинки
                    _size = QSize(200, 100)
                    image.setPixmap(pix.scaled(_size, Qt.KeepAspectRatio)) #подгоняем размер
                    self.tables.setCellWidget(i, j, image) #вставляем widget в таблицу
                elif self.datasheets[i][j] == self.datasheets[i][15]:  #проверка на 15 элемент, там должна быть кнопка
                    self.tables.setCellWidget(i, j, self.button_list[i]) #вставляем widget в таблицу
                    self.conn(self.button_list[i], self.datasheets[i][0], self.datasheets[i][2]) #вызываем функцию conn в которой назначим кнопке определённое действие
                else:
                    self.tables.setItem(i, j, QTableWidgetItem(str(self.datasheets[i][j]))) #меняем в ячейке таблички значения на данные из sql

        # делаем ресайз колонок по содержимому
        self.tables.resizeColumnsToContents()
        self.con.close()

    def conn(self, a, unit_name, rase):
        a.clicked.connect(lambda: self.add_unit(unit_name, rase)) #если этого не сделать, передаваться значения будут только из последней кнопки

    def add_unit(self, unit_name, rase):
        c = 'army_list/' + str(rase) + '.txt' #создаем путь текстового файла с определённым названием
        d = open(c, mode = "a+") #открываем файл
        data = d.read().split('\n')
        data.append(unit_name) #добавляем имя юнита
        d.write('\n'.join(data))
        d.close()

    def clear_army_list(self):
        f, ok_pressed = QInputDialog.getItem(
            self, "Выберите файл для очистки", "Выберите файл для очистки",
            ("Astartes.txt", "Necrons.txt", "Bubonic.txt", "Orcs.txt"), 1, False) #Диалоговое окно для выбора файла
        c = 'army_list/' + f
        d = open(c, mode = "w")
        d.write('') #очищаем файл
        d.close

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
        try:
            uic.loadUi('ui\help.ui', self)
        except:
            logging.error("Отсутстыует help.ui, вот зачем было удалять помощь, теперь ручками")
        self.label.setText("""Тут все юниты, есть их характеристики.
Кнопка добавить в армию позволяет добавить юнита в вашу
виртальную локальную армию.
Армии не стриаются после выхода, что-бы очистить всю
армию нужно воспользоваться соответсвующей функцией снизу.
Юниты упорядочены в случайном порядке, положение не влияет на силу """)
