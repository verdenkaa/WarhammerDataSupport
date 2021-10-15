import sys
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from chocer import RasaChoice


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menuer.ui', self)
        #загружаем интерфейс
        self.Soldier_choice.clicked.connect(self.soldiers)
    
    def soldiers(self):
        self.hide()
        sold = RasaChoice(Menu())
        sold.setWindowTitle('Warhammer Data Support')
        sold.setWindowIcon(QIcon('images/icon.png'))
        sold.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Menu()
    form.setWindowTitle('Warhammer Data Support')
    form.setWindowIcon(QIcon('images/icon.png'))
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())