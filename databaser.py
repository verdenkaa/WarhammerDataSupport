import sys
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableView, QApplication, QMainWindow


class Dater(QMainWindow):
    def __init__(self, forback, std_db):
        super().__init__()
        uic.loadUi('ui\databaser.ui', self)
        self.forback = forback
        self.std_db = std_db
        # Подключаем выход обратно в меню
        self.pushButton.clicked.connect(self.back)
        # Подключаем стандартную базу данных
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f"db\{self.std_db}")
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('datasheet')
        model.select()
        self.tableView.setModel(model)
        # Меняем размер столбцов в зависимости от их длинны
        self.tableView.resizeColumnsToContents()

    def back(self):
        self.hide()
        self.forback.setWindowTitle('Warhammer Data Support')
        self.forback.setWindowIcon(QIcon('ui\images\icon.png'))
        self.forback.show()