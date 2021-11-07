import sqlite3, logging
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMainWindow
from databaser import Dater


class RasaChoice(QMainWindow):
    def __init__(self, forback):
        super().__init__()
        logging.basicConfig(filename = "logs.log", format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
        try:
            uic.loadUi('ui/choser.ui', self)
        except:
            logging.error('Отсутствует choser.ui')
        self.forback = forback
        # Создание нужных для работы переменных со стартовыми значениями
        self.rases = ["Astartes", "Necrons", "Bubonic", "Orks"]
        self.StartUnit = [10000, 0, 6, 6, 0, 0, 0, 0, 0, 6]
        # Подключение защиты от дурака, доступен ввод только чисел в диапазоне от 0 до 999
        self.PEdit.setValidator(QtGui.QIntValidator(0, 9999))
        self.MEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.WSEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.BSEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.SEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.TEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.WEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.AEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.LdEdit.setValidator(QtGui.QIntValidator(0, 999))
        self.SvEdit.setValidator(QtGui.QIntValidator(0, 999))
        # Подключение функционала кнопок и чекеров
        self.pushButton_2.clicked.connect(self.helper)
        self.pushButton_3.clicked.connect(self.backtomenu)
        self.pushButton.clicked.connect(self.startsorting)
        self.checkBox.stateChanged.connect(lambda: self.addrace(self.checkBox, "Astartes", 0))
        self.checkBox_2.stateChanged.connect(lambda: self.addrace(self.checkBox_2, "Necrons", 1))
        self.checkBox_3.stateChanged.connect(lambda: self.addrace(self.checkBox_3, "Bubonic", 2))
        self.checkBox_4.stateChanged.connect(lambda: self.addrace(self.checkBox_4, "Orks", 3))

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
        self.con.close()
        self.forback.setWindowTitle('Warhammer Data Support')
        self.forback.setWindowIcon(QIcon('ui\images\icon.png'))
        self.forback.show()

    def sort(self, datasheets):
        # Функция сортировки списка кортежей
        NonTime = []
        for i in datasheets:
            t = True
            for j in range(4, 14):
                if j in (4, 6, 7, 13):
                    if i[j] > self.StartUnit[j - 4]:
                        t = False
                        break
                else:
                    if i[j] < self.StartUnit[j - 4]:
                        t = False
                        break
            if t:
                NonTime.append(i)
        return NonTime

    def startsorting(self):
        # Счтываем значение если были изменения в вводе
        if self.PEdit.text() != "":
            self.StartUnit[0] = int(self.PEdit.text())
        if self.MEdit.text() != "":
            self.StartUnit[1] = int(self.MEdit.text())
        if self.WSEdit.text() != "":
            self.StartUnit[2] = int(self.WSEdit.text())
        if self.BSEdit.text() != "":
            self.StartUnit[3] = int(self.BSEdit.text())
        if self.SEdit.text() != "":
            self.StartUnit[4] = int(self.SEdit.text())
        if self.TEdit.text() != "":
            self.StartUnit[5] = int(self.TEdit.text())
        if self.WEdit.text() != "":
            self.StartUnit[6] = int(self.WEdit.text())
        if self.AEdit.text() != "":
            self.StartUnit[7] = int(self.AEdit.text())
        if self.LdEdit.text() != "":
            self.StartUnit[8] = int(self.LdEdit.text())
        if self.SvEdit.text() != "":
            self.StartUnit[9] = int(self.SvEdit.text())
        self.hide()
        # Подключаем бд
        try:
            self.con = sqlite3.connect("db/off_units.sqlite")
        except:
            logging.error('Отсутствует off_units.sqlite')
        self.cur = self.con.cursor()
        print(self.rases)
        self.datasheets = self.cur.execute(f"""SELECT * FROM unit_datasheet WHERE rase IN {tuple(self.rases)}""").fetchall()  # получаем данные в виде списка кортежей
        self.datasheets = self.sort(self.datasheets)
        self.datas = Dater(self.forback, self.datasheets)  # И закидываем в переменную по умолчаню
        self.datas.show()
        self.con.close()


class Helper(QMainWindow):
    # Класс окна помощи
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi('ui\help.ui', self)
        except:
            logging.error("Отсутстыует help.ui, вот зачем было удалять помощь, теперь ручками")
        self.label.setText("""Тут вы можете выбрать характеристики и фракцию
будующих юнитов вашей армии.
Можно оставить поля пустыми, тогда они будут оставлены по умолчанию.
Ознакомится со всеми характеристиками можно в офицальной
книге правил от Games Workshop, или на сайте Вахапедии.""")
