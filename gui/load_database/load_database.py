from .load_database_ui import Ui_Dialog
from PyQt5 import QtWidgets
import requests as r
import json
import os


class LoadDatabaseDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.__populate_db_list()

        self.database_list.itemClicked.connect(self.__selected_item)

    def __selected_item(self, item):
        self.selected = item.value

    def __load_local_db_paths(self):
        path = os.path.join('gui', 'db_paths.json')
        if os.path.exists(path):
            json_data = json.load(open(path))
        else:
            path = os.path.expanduser(path)
            json_data = {'dbs': []}
            json.dump(json_data, open(path, "w+"))
        return json_data['dbs']

    def __load_remote_db_paths(self):
        url = 'http://localhost:8000/api/dbs'
        response = r.get(url)
        if response.status_code == 200:
            json_data = response.json()
            dbs = json_data['data']
            return dbs

    def __format_data(self, data, db_type):
        result = []

        for item in data:
            label = item['name']
            record = [{'db': label, 'db_type': db_type}, label + '-' + db_type]
            result.append(record)

        return result

    def __populate_db_list(self):
        local_dbs = self.__load_local_db_paths()
        remote_dbs = self.__load_remote_db_paths()

        local_dbs = self.__format_data(local_dbs, 'Local')
        remote_dbs = self.__format_data(remote_dbs, 'Remote')

        for db in local_dbs:
            item = QtWidgets.QListWidgetItem(db[1])
            item.value = db[0]
            self.database_list.addItem(item)

        for db in remote_dbs:
            item = QtWidgets.QListWidgetItem(db[1])
            item.value = db[0]
            self.database_list.addItem(item)

    def get_results(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            try:
                data = self.selected
                return data
            except AttributeError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText('Please select record')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            return None
