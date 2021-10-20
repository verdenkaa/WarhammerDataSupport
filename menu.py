import sys
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from chocer import RasaChoice
from databaser import Dater


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\menuer.ui', self)
        # Стандартная используемая база данных
        self.std_db = "off_units.sqlite"
        self.Soldier_choice.clicked.connect(self.soldiers)
        self.dater.clicked.connect(self.databases)
        self.pushButton.clicked.connect(self.settings)
        # Я Никиата, нужно добавить сюда проверку баз векрсии приложения!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def soldiers(self):
        self.hide()
        self.sold = RasaChoice(Menu(), self.std_db)
        self.sold.setWindowTitle('Warhammer Data Support')
        self.sold.setWindowIcon(QIcon('ui\images\icon.png'))
        self.sold.show()

    def databases(self):
        self.hide()
        self.daterwindow = Dater(Menu(), self.std_db)
        self.daterwindow.setWindowTitle('Warhammer Data Support')
        self.daterwindow.setWindowIcon(QIcon('ui\images\icon.png'))
        self.daterwindow.show()

    def settings(self):
        self.settingswindow = Settings()
        self.settingswindow.setWindowTitle('Warhammer Data Support Settings')
        self.settingswindow.setWindowIcon(QIcon('ui\images\settings.jpg'))
        self.settingswindow.show()


class Settings(QMainWindow):
    # Класс окна настроек
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\settings.ui', self)
        # Я Никиата, нужно добавить сюда проверку баз данных!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Menu()
    form.setWindowTitle('Warhammer Data Support')
    form.setWindowIcon(QIcon('ui\images\icon.png'))
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())