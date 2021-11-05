from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLabel, QPushButton, QInputDialog, QComboBox
import sqlite3, os


class Armier(QMainWindow):
    def __init__(self, forback):
        super().__init__()
        uic.loadUi('ui/army.ui', self)
        self.forback = forback
        self.movearmy = [] # Список лэйблов доступных к перемещению на полу боя
        # Подключаем выход обратно в меню
        self.rassa, ok_pressed = QInputDialog.getItem(
            self, "Выберите файл вашей армии", "Выберите файл вашей армии", 
            ("Astartes", "Necrons", "Bubonic", "Orcs"), 1, False)
        #Не переставляй из функции after_op_file ничего. Там не self, а обычные значения. Меняй сразу в функции
        self.pushButton.clicked.connect(self.back)
        self.HelpButton.clicked.connect(self.helper)

        self.after_op_file()  #все должно создаваться после выбора файла

    def after_op_file(self):
        self.con = sqlite3.connect("db/off_units.sqlite")       #подключаем БД
        # Создание курсора
        self.cur = self.con.cursor()

        
        self.movearmy = []
        file_name = 'army_list/' + self.rassa + '.txt'
        file = open(file_name, mode = "r")
        un_name = file.read().split('\n')

        for i in range(len(un_name)):
            if os.path.exists(f"ui/images/{un_name[i]}.png") and un_name[i] != "": #Если такой юнит есть в папке
                b = self.image = QLabel(self.groupBox)
                b.setPixmap(QPixmap(f"ui/images/{un_name[i]}.png")) # Назначаем изображение
                self.movearmy.append(b) # Добавляем в список разрешений
                b.installEventFilter(self) # Добавляем к обьекту ивент

        self.radioButton.toggled.connect(lambda: self.pole.setPixmap(QPixmap("ui/images/duimmap.png")))
        self.radioButton_2.toggled.connect(lambda: self.pole.setPixmap(QPixmap("ui/images/marsmap.jpg")))
        self.radioButton_3.toggled.connect(lambda: self.pole.setPixmap(QPixmap("ui/images/armageddonmap.jpg")))
        self.radioButton_4.toggled.connect(lambda: self.pole.setPixmap(QPixmap("ui/images/istvanmap.jpg")))
        self.radioButton_5.toggled.connect(lambda: self.pole.setPixmap(QPixmap("ui/images/kadiamap.jpg")))
        self.radioButton_6.toggled.connect(lambda: self.pole.setPixmap(QPixmap("ui/images/nurglemap.jpg")))

        print(self.movearmy)

        self.datasheets = []
        for i in un_name:
            j = self.cur.execute("""SELECT name, type, points, move, Image, Can_use_gun_id FROM unit_datasheet
                WHERE name = ?""", (i, )).fetchall() #получаем данные в виде списка кортежей
            if j != []: #проверка на наличие элементов
                j = [gg for gg in j[0]] #переводим кортеж в список
                if j[5] != None: #проверка на носимое юнитом оружие
                    j[5] = j[5].split() #номера оружий переводим в список
                    gun_har = [] #список вооружения в виде списка списков характеристик оружия
                    for p in j[5]:
                        px = self.cur.execute("""SELECT Gun_id, Gun_name, Range, Type, Number_of_attacks, strength, Armour_pirsing, Damage, Abilities, Points FROM unit_gun
                            WHERE Gun_id = ?""", (p, )).fetchall() #берем данные из таблицы вооружения
                        px = [gg for gg in px[0]] #переводим кортеж в список
                        if px != []: #проверка на наличие элементов
                            gun_har.append(px) #добавляем список характеристик в список вооружения
                    for p in range(len(j[5])): #проходим по всем элементам
                        strochka = str(gun_har[p][1]) + ', Дальность стрельбы: ' + str(gun_har[p][2]) + ', Тип: ' + str(gun_har[p][3]) + ', Количество выстрелов: ' + str(gun_har[p][4]) + ', Сила: ' + str(gun_har[p][5]) + ', Пробитие брони: ' + str(gun_har[p][6]) + ', Урон: ' + str(gun_har[p][7]) + ', Особенность: ' + str(gun_har[p][8]) + ', Стоимость в очках:' + str(gun_har[p][9])
                        #Передаем характеристики в виде строки
                        j[5][p] = [strochka, gun_har[p][9]] #заменяем значения на список со строкой характеристики и стоимостью вооружения в очках
                self.datasheets.append(j) #добавляем данные в переменную datasheets

        self.table_creator()

    def table_creator(self):
        self.tables.setColumnCount(6)     # Устанавливаем нужное кол-во колонок
        self.tables.setRowCount(len(self.datasheets))        # и количество элементов в таблице

        # Устанавливаем заголовки таблицы
        self.tables.setHorizontalHeaderLabels(['Name', 'Type', 'Points', 'Move', 'Look', 'Gun'])

        # заполняем столбцы
        for i in range(len(self.datasheets)):
            for j in range(len(self.datasheets[i])):
                if self.datasheets[i][j] == self.datasheets[i][4]:  #проверка на 4 элемент, там должно быть изображение
                    image = QLabel(self)
                    pix = QPixmap('Unit_image/' + str(self.datasheets[i][j])) #Из списка с данными sql мы берем имя картинки
                    _size = QSize(200, 100) 
                    image.setPixmap(pix.scaled(_size, Qt.KeepAspectRatio)) #подгоняем размер
                    self.tables.setCellWidget(i, j, image) #вставляем widget в таблицу
                elif self.datasheets[i][j] == self.datasheets[i][5]:
                    combo = QComboBox(self)
                    if self.datasheets[i][5] != None: #проверка на наличие вооружения
                        for p in range(len(self.datasheets[i][5])): #проходим по каждому оружию
                            combo.addItem(self.datasheets[i][5][p][0]) #добавляем вариант выбора
                    self.tables.setCellWidget(i, j, combo)
                else:
                    self.tables.setItem(i, j, QTableWidgetItem(str(self.datasheets[i][j]))) #меняем в ячейке таблички значения на данные из sql

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
