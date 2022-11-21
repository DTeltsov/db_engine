from gui.load_database.load_database import LoadDatabaseDialog
from gui.view_database.view_database_ui import Ui_MainWindow
from gui.create_database.create_database import CreateDatabaseDialog
from gui.new_column.new_column import NewColumnDialog
from gui.new_table.new_table import NewTableDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from db.db import DBManager
import sys
import requests as r
import os
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.actionLoad.triggered.connect(self.load_database)
        self.actionCreate_new.triggered.connect(self.create_database)
        self.actionSave.triggered.connect(self.save_db)

        self.table_list.itemClicked.connect(self.load_table)
        self.add_row_button.clicked.connect(self.add_row)
        self.delete_row_button.clicked.connect(self.delete_row)
        self.add_column_button.clicked.connect(self.add_column)
        self.delete_column_botton.clicked.connect(self.delete_column)
        self.delete_table_button.clicked.connect(self.delete_table)
        self.pushButton.clicked.connect(self.add_table)

    def __add_row(self):
        rows_count = self.data_table.rowCount() - 1
        data = {}
        for i in range(len(self.headers)):
            try:
                item = self.data_table.item(rows_count, i).text()
            except AttributeError:
                item = ''
            specs = self.headers[i].split('\n')
            if specs[1] == 'int':
                item = int(item)
            elif specs[1] == 'str':
                item = str(item)
            elif specs[1] == 'float':
                item = float(item)
            elif specs[1] == 'bool':
                item = bool(item)
            elif specs[1] in ['color', 'colorInvl']:
                try:
                    item = json.loads(item)
                except json.JSONDecodeError:
                    item = ''

            data[specs[0]] = item
        if self.db_type == 'Local':
            table = self.db.get_table(self.table)
            table.add_row(data)
        elif self.db_type == 'Remote':
            url = self.table + '/row'
            response = r.post(url, json=data)

    def delete_row(self):
        row = self.data_table.currentRow()
        if self.db_type == 'Local':
            table = self.db.get_table(self.table)
            table.delete_row(row)
        elif self.db_type == 'Remote':
            url = self.table + '/row/' + str(row)
            response = r.delete(url)
            return response.status_code

    def add_column(self):
        w = NewColumnDialog()
        data = w.get_results()
        if data:
            if self.db_type == 'Local':
                table = self.db.get_table(self.table)
                table.add_column(data['name'], data['attr'], data['is_null'], None)
            elif self.db_type == 'Remote':
                url = self.table + '/column'
                response = r.post(url, json=data)

    def delete_column(self):
        column = self.data_table.currentColumn()
        column_name = self.headers[column].split('\n')[0]
        if self.db_type == 'Local':
            table = self.db.get_table(self.table)
            table.delete_column(column_name)
        elif self.db_type == 'Remote':
            url = self.table + '/column/' + column_name
            response = r.delete(url)

    def add_table(self):
        w = NewTableDialog()
        data = w.get_results()
        if data:
            if self.db_type == 'Local':
                self.db.add_table(data['name'])
            elif self.db_type == 'Remote':
                url = 'http://localhost:8000/api/db/' + self.db + '/table'
                response = r.post(url, json=data)
            self.__populate_tables_list()

    def delete_table(self):
        if self.db_type == 'Local':
            self.db.delete_table(self.table)
        elif self.db_type == 'Remote':
            url = self.table
            response = r.delete(url)
        self.__populate_tables_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.__add_row()

    def add_row(self):
        rows_count = self.data_table.rowCount()
        self.data_table.insertRow(rows_count)

    def __populate_table(self, table):
        columns = table['columns']
        rows = [row['data'] for row in table['rows']]
        headers = []
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        self.headers = []
        for column in columns:
            column_specs = column['column_name'] + '\n' + column['column_attr'] + '\n' + str(column['is_null'])
            headers.append(column_specs)
            self.headers.append(column_specs)
            columns_count = self.data_table.columnCount()
            self.data_table.insertColumn(columns_count)
        self.data_table.setHorizontalHeaderLabels(headers)

        for row in rows:
            rows_count = self.data_table.rowCount()
            self.data_table.insertRow(rows_count)
            for i, value in enumerate(row):
                self.data_table.setItem(
                    rows_count,
                    i,
                    QtWidgets.QTableWidgetItem(str(value))
                )

    def __get_remote_table_info(self, table):
        url = table
        response = r.get(url)

        if response.status_code == 200:
            result = response.json()['data']

        return result

    def load_table(self, item):
        self.table = item.value
        if self.db_type == 'Local':
            table = self.db.get_table(item.value)
            table = {
                'table_name': table.table_name,
                'columns': [column.__dict__ for column in table.columns],
                'rows': [
                    {'pk': i, 'data': row} for i, row in enumerate(table.rows)
                ]
            }
        elif self.db_type == 'Remote':
            table = self.__get_remote_table_info(item.value)
        self.__populate_table(table)

    def __add_db_path(self, db_name):
        path = os.path.join('gui', 'db_paths.json')
        if os.path.exists(path):
            json_data = json.load(open(path))
            json_data['dbs'].append({'name': db_name})
            config_path = os.path.expanduser(path)
            json.dump(json_data, open(config_path, "w+"))
        else:
            json_data = {'dbs': [{'name': db_name}]}
            config_path = os.path.expanduser(path)
            json.dump(json_data, open(config_path, "w+"))

    def save_db(self):
        if self.db_type == 'Local':
            self.db.save_db()

    def create_database(self):
        w = CreateDatabaseDialog()
        result = w.get_results()
        if result:
            self.db_type = result['db_type']

            if self.db_type == 'Local':
                self.db = DBManager()
                self.db.create_db(result['db'])

                self.db = result['db']
                self.__add_db_path(self.db)
                self.__load_database()
            elif self.db_type == 'Remote':
                url = 'http://localhost:8000/api/db'
                response = r.post(url, json={'name': result['db']})

                if response.status_code == 201:
                    self.db = result['db']
                    self.__load_database()

    def get_tables(self):
        if self.db_type == 'Local':
            tables = self.db.get_tables()
            tables = [[table.table_name, table.table_name] for table in tables]
        elif self.db_type == 'Remote':
            url = 'http://localhost:8000/api/db/' + self.db
            response = r.get(url)

            if response.status_code == 200:
                tables_names = response.json()['data']['tables']
                tables_links = response.json()['links']['db_tables']

                tables = []
                for i in range(len(tables_names)):
                    tables.append([
                        tables_links[i]['self']['href'],
                        tables_names[i]['table_name']
                        ])
        return tables

    def __populate_tables_list(self):
        self.table_list.clear()
        tables = self.get_tables()

        for table in tables:
            item = QtWidgets.QListWidgetItem(table[1])
            item.value = table[0]
            self.table_list.addItem(item)

    def __load_database(self):
        if self.db_type == 'Local':
            path = self.db + '.json'
            self.db = DBManager()
            self.db.load_db(path)
            self.__populate_tables_list()
        elif self.db_type == 'Remote':
            self.__populate_tables_list()

    def load_database(self):
        w = LoadDatabaseDialog()
        result = w.get_results()
        if result:
            self.db_type = result['db_type']
            self.db = result['db']
            self.__load_database()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
