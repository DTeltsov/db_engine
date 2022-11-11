from gui.load_database.load_database import LoadDatabaseDialog
from gui.view_database.view_database_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from db.db import DBManager
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.actionLoad.triggered.connect(self.load_database)

    def create_database(self):
        pass

    def load_database(self):
        w = LoadDatabaseDialog()
        result = w.get_results()
        print(result)
        if result['type'] == 'Local':
            self.db = DBManager()
            self.db.load_db(result['db'] + '.json')
        elif result['type'] == 'Remote':
            print('lol')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
