from .new_column_ui import Ui_Dialog
from PyQt5 import QtWidgets


class NewColumnDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

    def get_results(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            data = {}
            try:
                data['name'] = self.table_name.text()
                data['attr'] = self.table_attr.currentText()
                data['is_null'] = bool(self.table_is_null.currentText())
                return data
            except AttributeError:
                pass
        else:
            return None
