from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLabel, QPushButton
import sqlite3


class Armier(QMainWindow):
    def __init__(self, forback):
        super().__init__()
        uic.loadUi('ui/army.ui', self)
        self.con = sqlite3.connect("db/off_units.sqlite")       #подключаем БД
        # Создание курсора
        self.cur = self.con.cursor()
        self.datasheets = self.cur.execute("""SELECT * FROM unit_datasheet
            WHERE name != '  '""").fetchall() #получаем данные в виде списка кортежей
        self.table_creator()
        self.forback = forback
        self.movearmy = (self.label,) # Список лэйблов доступных к перемещению на полу боя
        # Подключаем выход обратно в меню
        self.pushButton.clicked.connect(self.back)
        self.label.installEventFilter(self) # Добавляем к обьекту ивент
        self.HelpButton.clicked.connect(self.helper)

    def table_creator(self):
        self.tables.setColumnCount(16)     # Устанавливаем нужное кол-во колонок
        self.tables.setRowCount(len(self.datasheets))        # и количество элементов в таблице

        # Устанавливаем заголовки таблицы
        self.tables.setHorizontalHeaderLabels(['Name', 'Type', 'Rase', 'Power', 'Points', 'Move', 'Weapon Skill', 'Ballistic Skill', 'Strength', 'Toughness', 'Wound', 'Attacs', 'Leadership', 'Save', 'Look', 'Add to my army list'])

        # заполняем столбцы
        self.button_list = [QPushButton('Добавить в список моей армии', self) for i in range(len(self.datasheets))]
        for i in range(len(self.datasheets)):
            for j in range(len(self.datasheets[i])):
                if self.datasheets[i][j] == self.datasheets[i][-2]:  #проверка на 2 с конца элемент, там должно быть изображение
                    image = QLabel(self)
                    pix = QPixmap('Unit_image/' + str(self.datasheets[i][j])) #Из списка с данными sql мы берем имя картинки
                    _size = QSize(200, 100) 
                    image.setPixmap(pix.scaled(_size, Qt.KeepAspectRatio)) #подгоняем размер
                    self.tables.setCellWidget(i, j, image) #вставляем widget в таблицу
                elif self.datasheets[i][j] == self.datasheets[i][-1]:  #проверка на 1 с конца элемент, там должна быть кнопка
                    self.tables.setCellWidget(i, j, self.button_list[i]) #вставляем widget в таблицу
                    self.conn(self.button_list[i], self.datasheets[i][0], self.datasheets[i][2]) #вызываем функцию conn в которой назначим кнопке определённое действие
                else:
                    self.tables.setItem(i, j, QTableWidgetItem(str(self.datasheets[i][j]))) #меняем в ячейке таблички значения на данные из sql

        # делаем ресайз колонок по содержимому
        self.tables.resizeColumnsToContents()

    def conn(self, a, unit_name, rase):
        a.clicked.connect(lambda: self.add_unit(unit_name, rase)) #если этого не сделать, передаваться значения будут только из последней кнопки
    
    def add_unit(self, unit_name, rase):
        c = 'army_list/' + str(rase) + '.txt' #создаем путь текстового файла с определённым названием
        d = open(c, mode = "a+") #открываем файл
        data = d.read().split('\n')
        data.append(unit_name) #добавляем имя юнита
        d.write('\n'.join(data))
        d.close()
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

    def eventFilter(self, source, event):      
        #  Если обьект в разрешенном списке
        if source in self.movearmy:
            # Если мишью нажали на обьект
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.movingButton = source
                self.startPos = event.pos()
            # Если мышью двигают
            elif event.type() == QtCore.QEvent.MouseMove and self.movingButton:                
                self.movingButton.move(source.pos() + event.pos() - self.startPos)
        # В конце возвращаем False?? Почему он не принимает True известно только одному Богу Императору, но это не костыль а позвоночник
        return False
        #return super().eventFilter(source, event)  # Был еще екурсионный вариант, но ест больше памяти


class Helper(QMainWindow):
    # Класс окна помощи
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\help.ui', self)
