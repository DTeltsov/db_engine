from .view_database_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from .view_database_ui import Ui_MainWindow as UI_Database


class ViewDatabaseWindow(QtWidgets.QDialog, UI_Database):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
