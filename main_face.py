import sys
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from main import RasaChoice


class Main_face(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_face.ui', self)
        #загружаем интерфейс
        self.Soldier_choice.clicked.connect(self.soldiers)
    
    def soldiers(self):
        sold = RasaChoice()
        sold.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main_face()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())