from .create_database_ui import Ui_Dialog
from PyQt5 import QtWidgets


class CreateDatabaseDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

    def get_results(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            data = {}
            try:
                data['db'] = self.name_editline.text()
                data['db_type'] = self.location_combobox.currentText()
                return data
            except AttributeError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText('Please select record')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            return None
