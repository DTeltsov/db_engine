from .new_table_ui import Ui_new_column
from PyQt5 import QtWidgets


class NewTableDialog(QtWidgets.QDialog, Ui_new_column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

    def get_results(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            data = {}
            try:
                data['name'] = self.table_name.text()
                return data
            except AttributeError:
                pass
        else:
            return None
