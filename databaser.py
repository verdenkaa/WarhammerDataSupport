import sys
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QApplication


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('databaser.ui', self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('films_db.sqlite')
        db.open()