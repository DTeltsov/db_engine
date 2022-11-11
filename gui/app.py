from start_window.start_window_ui import Ui_MainWindow
from load_database.load_database import LoadDatabaseDialog
from view_database.view_database import ViewDatabaseWindow
from PyQt5 import QtWidgets
# from db.db import DBManager
import sys


class StartWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.load_database_button.clicked.connect(self.load_database)

    def create_database(self):
        pass

    def load_database(self):
        w = LoadDatabaseDialog()
        result = w.get_results()
        print(result)
        if result['type'] == 'Local':
            # db = DBManager()
            # db.load_db(result['db'] + '.json')
            w = ViewDatabaseWindow()
            self.hide()
            w.show()
        elif result['type'] == 'Remote':
            print('lol')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = StartWindow()
    window.show()

    sys.exit(app.exec_())
