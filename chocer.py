import sys, sqlite3
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from databaser import Dater



class RasaChoice(QMainWindow):
    def __init__(self, forback):
        super().__init__()
        uic.loadUi('ui/choser.ui', self)
        self.forback = forback
        # Создание нужных для работы переменных со стартовыми значениями
        self.rases = ["Astartes", "Necrons", "Bubonic", "Orcs"]
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

    def sort(self, datasheets):
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
        if self.PEdit.text() != "": self.StartUnit[0] = int(self.PEdit.text())
        if self.MEdit.text() != "": self.StartUnit[1] = int(self.MEdit.text())
        if self.WSEdit.text() != "": self.StartUnit[2] = int(self.WSEdit.text())
        if self.BSEdit.text() != "": self.StartUnit[3] = int(self.BSEdit.text())
        if self.SEdit.text() != "": self.StartUnit[4] = int(self.SEdit.text())
        if self.TEdit.text() != "": self.StartUnit[5] = int(self.TEdit.text())
        if self.WEdit.text() != "": self.StartUnit[6] = int(self.WEdit.text())
        if self.AEdit.text() != "": self.StartUnit[7] = int(self.AEdit.text())
        if self.LdEdit.text() != "": self.StartUnit[8] = int(self.LdEdit.text())
        if self.SvEdit.text() != "": self.StartUnit[9] = int(self.SvEdit.text())
        self.hide()
        self.con = sqlite3.connect("db/off_units.sqlite")
        self.cur = self.con.cursor()
        self.datasheets = self.cur.execute(f"""SELECT * FROM unit_datasheet WHERE rase IN {tuple(self.rases)}""").fetchall() #получаем данные в виде списка кортежей
        self.datasheets = self.sort(self.datasheets)
        print(self.datasheets)
        self.datas = Dater(self.forback, self.datasheets)
        self.datas.show()


class Helper(QMainWindow):
    # Класс окна помощи
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\help.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RasaChoice(RasaChoice)
    form.setWindowTitle('Warhammer Data Support')
    form.setWindowIcon(QIcon('ui\images\icon.png'))
    form.show()
    sys.exit(app.exec())