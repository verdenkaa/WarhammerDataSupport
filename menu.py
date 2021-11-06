import sys, base64, requests
import os, wget, subprocess, logging
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from chocer import RasaChoice
from databaser import Dater
from army import Armier

version = 0.2
dbversion = 0.1


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\menuer.ui', self)
        self.Soldier_choice.clicked.connect(self.soldiers)
        self.dater.clicked.connect(self.databases)
        self.pushButton.clicked.connect(self.settings)
        self.Create_army.clicked.connect(self.army_list)
        logging.basicConfig(filename = "logs.log", format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    
    def soldiers(self):
        self.hide()
        self.sold = RasaChoice(Menu())
        self.sold.setWindowTitle('Warhammer Data Support')
        self.sold.setWindowIcon(QIcon('ui\images\icon.png'))
        self.sold.show()

    def databases(self):
        self.hide()
        self.daterwindow = Dater(Menu())
        self.daterwindow.setWindowTitle('Warhammer Data Support')
        self.daterwindow.setWindowIcon(QIcon('ui\images\icon.png'))
        self.daterwindow.show()

    def settings(self):
        self.settingswindow = Settings()
        self.settingswindow.setWindowTitle('Warhammer Data Support Settings')
        self.settingswindow.setWindowIcon(QIcon('ui\images\settings.jpg'))
        self.settingswindow.show()
    
    def army_list(self):
        self.hide()
        self.daterwindow = Armier(Menu())
        self.daterwindow.setWindowTitle('Warhammer Data Support')
        self.daterwindow.setWindowIcon(QIcon('ui\images\icon.png'))
        self.daterwindow.show()


class Settings(QMainWindow):
    # Класс окна настроек
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\settings.ui', self)
        self.Update.clicked.connect(self.FindUpdate)
        self.dbUpdate.clicked.connect(self.dbUpdateOnline)

    def FindUpdate(self):
        global version
        global dbversion
        try:
            # Считываем значения с облака
            req = requests.get("https://api.github.com/repos/verdenkaa/WarhammerDataSupport/contents/soursecontrol.txt")
            self.updateBar.setValue(20)
            # Проверяем данные на наличие ошибок
            if req.status_code == requests.codes.ok:
                req = req.json()
                self.updateBar.setValue(30)
                # Декодируем
                content = base64.b64decode(req['content']).decode("utf-8").split()
                self.updateBar.setValue(70)
                # Если версия больше
                if float(content[0]) > version:
                    self.urlUpdate.setText("<a href='https://github.com/verdenkaa/WarhammerDataSupport'> Версия устарела, обновите приложение </a>")
                    self.urlUpdate.setOpenExternalLinks(True)
                    self.urlUpdate.setStyleSheet("color: red")
                    self.updateBar.setValue(100)
                # Если версия базы больше
                elif float(content[1]) > dbversion:
                    self.urlUpdate.setText("Обновите базу данных")
                    self.urlUpdate.setStyleSheet("color: red")
                    self.updateBar.setValue(100)
                # иначе если актуальная версия
                else:
                    self.urlUpdate.setText("У вас актуальная версия")
                    self.urlUpdate.setStyleSheet("color: lightgreen")
                    self.updateBar.setValue(100)
            # Здесь отлавливаем возможную ошибку в значениях 
            else:
                logging.error('Ошибка на стороне контроля версий, скачайте последнюю версию приложения, или обратитесь напрямую к разработчикам если ошибку долго не фиксят')
                self.updateBar.setValue(0)
                self.urlUpdate.setText("Что-то не так, серьезная ошибка контроля версий, переустановите приложение")
        except:
            logging.error('Был плохой интернет при обновлении приложения')
            self.updateBar.setValue(0)
            self.urlUpdate.setText("Технические шоколадки, проверьте интернет")

    def dbUpdateOnline(self):
        try:
            self.dbUpdateBar.setValue(20)
            subprocess.check_call(["ping", "github.com"]) #Проверка подключения к сети и возможность доступа к github
            # Переменная сылка на базу данных
            url = "https://github.com/verdenkaa/WarhammerDataSupport/blob/main/db/off_units.sqlite?raw=true"
            self.dbUpdateBar.setValue(30)
            # Проверка на наличие файла, может отсутствовать в ходе обновления без интернета или удаления его ручками
            if os.path.exists("db/off_units.sqlite"):
                os.remove("db/off_units.sqlite")
            self.dbUpdateBar.setValue(50)
            # Качаем последнюю версию с облака
            wget.download(url, "db/off_units.sqlite")
            self.dbUpdateBar.setValue(100)
        except subprocess.CalledProcessError:
            # Отлов плохого соединения или его отсутствия
            logging.error('Был плохой интернет при обноввлении базы данных, или что-то другое. Ваш выход - переустановка')
            self.dbUpdateBar.setValue(0)
            self.urlUpdate.setStyleSheet("color: red")
            self.urlUpdate.setText("Технические шоколадки, проверьте интернет")



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