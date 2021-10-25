import sys, base64, requests
import urllib.request
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from chocer import RasaChoice
from databaser import Dater

version = 0.1
dbversion = 0.1


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\menuer.ui', self)
        # Стандартная используемая база данных
        self.std_db = "off_units.sqlite"
        self.Soldier_choice.clicked.connect(self.soldiers)
        self.dater.clicked.connect(self.databases)
        self.pushButton.clicked.connect(self.settings)
    
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
        self.Update.clicked.connect(self.FindUpdate)
        self.dbUpdate.clicked.connect(self.dbUpdateOnline)
        # Я Никиата, нужно добавить сюда проверку баз данных!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def FindUpdate(self):
        global version
        global dbversion
        req = requests.get("https://api.github.com/repos/verdenkaa/WarhammerDataSupport/contents/soursecontrol.txt")
        self.updateBar.setValue(20)
        if req.status_code == requests.codes.ok:
            req = req.json()
            self.updateBar.setValue(30)
            content = base64.b64decode(req['content']).decode("utf-8").split()
            self.updateBar.setValue(70)
            if float(content[0]) > version:
                self.urlUpdate.setText("<a href='https://github.com/verdenkaa/WarhammerDataSupport'> Версия устарела, обновите приложение </a>")
                self.urlUpdate.setOpenExternalLinks(True)
                self.urlUpdate.setStyleSheet("color: red")
                self.updateBar.setValue(100)
            elif float(content[1]) > dbversion:
                self.urlUpdate.setText("Обновите базу данных")
                self.urlUpdate.setStyleSheet("color: red")
                self.updateBar.setValue(100)
            else:
                self.urlUpdate.setText("У вас актуальная версия")
                self.urlUpdate.setStyleSheet("color: lightgreen")
                self.updateBar.setValue(100)
        else:
            self.updateBar.setValue(0)
            self.urlUpdate.setText("Технические шоколадки, проверьте интернет")

    def dbUpdateOnline(self):
        req = requests.get("https://api.github.com/repos/verdenkaa/WarhammerDataSupport/contents/textbase.txt")
        urllib.request.urlretrieve(req, "db/notimedb.db")
        if req.status_code == requests.codes.ok and False:
            req = req.json()
            self.updateBar.setValue(30)
            content = base64.b64decode(req['content'])
            a = open("test.db", "w")
            a.writelines(str(content))
            print("qwerty")
        else:
            print("No")



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