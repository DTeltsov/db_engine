import json
import os
from pydoc import locate
from typing import List
from pathlib import Path


class Column:
    def __init__(self, name: str, attribute: str, is_null: bool):
        self.column_name = name
        self.column_attr = attribute
        self.is_null = is_null


class Table:
    def __init__(
        self,
        name: str,
        tab_columns: List[Column] = None,
        tab_rows: List[list] = None
    ):
        self.table_name = name

        if tab_columns:
            self.columns = tab_columns
        else:
            self.columns = []

        if tab_rows:
            self.rows = tab_rows
        else:
            self.rows = []

    def rename_table(self, table_name: str = None):
        if table_name:
            self.table_name = table_name

    def get_column(self, column_name: str):
        for column in self.columns:
            if column.column_name == column_name:
                return column

    def add_column(self, column_name: str, attr: str, is_null: bool):
        if self.get_column(column_name):
            print('There is alredy column with name {0} in table {1}'.format(
                column_name,
                self.table_name
                )
            )
            return False
        self.columns.append(Column(column_name, attr, is_null))

    def add_row(self, row: dict):
        values = []
        for key, value in row.items():
            column = self.get_column(key)
            if ((type(value) != locate(column.column_attr)) and
                    (not value and not column.is_null)):
                print(
                    '{0} - wrong type for column {1}. Must be {2}'.format(
                        value,
                        column.column_name,
                        column.column_attr
                        )
                    )
                break
            elif not value and not column.is_null:
                print(
                    'Column {} can not be Null'.format(
                        column.column_name
                        )
                    )
                break
            else:
                values.append(value)
        self.rows.append(values)

    def get_columns(self):
        return self.columns


class DB:
    def __init__(self, name: str, tables: Table = None):
        self.name = name

        if tables:
            self.tables = tables
        else:
            self.tables = []


class DBManager:
    def __init__(self):
        self.db = None
        self.location = None

    def __load_columns(self, columns: List[Column]):
        res_columns = []
        for column in columns:
            res_columns.append(
                Column(
                    column['column_name'],
                    column['column_attr'],
                    column['is_null']
                )
            )
        return res_columns

    def __load_tables(self, tables: List[Table]):
        res_tables = []
        for table in tables:
            columns = self.__load_columns(table['columns'])
            res_tables.append(
                Table(table['table_name'], columns, table['rows'])
            )
        return res_tables

    def get_table(self, table_name: str):
        for table in self.db.tables:
            if table.table_name == table_name:
                return table

    def add_table(self, table_name: str):
        if self.get_table(table_name):
            print('There is alredy table with name {}'.format(table_name))
            return False
        self.db.tables.append(Table(table_name))

    def delete_table(self, table_name: str):
        table = self.get_table(table_name)
        self.db.tables.remove(table)

    def __get_db_data(self):
        json_data = {'db_name': self.db.name}
        json_data['tables'] = []
        for table in self.db.tables:
            table_dict = {
                'table_name': table.table_name,
                'columns': [column.__dict__ for column in table.columns],
                'rows': table.rows
            }
            json_data['tables'].append(table_dict)
        return json_data

    def get_tables(self):
        return self.db.tables

    def create_db(
        self,
        db_name: str,
        location: str = os.path.abspath(os.getcwd())
    ):
        self.db = DB(db_name)
        self.location = os.path.expanduser(
                os.path.join(location, (self.db.name + '.json'))
            )
        try:
            json_data = self.__get_db_data()
            json.dump(json_data, open(self.location, "w+"))
        except Exception as e:
            print(e)

    def load_db(self, location: str):
        location = Path(location)
        if os.path.exists(location):
            json_data = json.load(open(location))
            tables = self.__load_tables(json_data['tables'])
            self.db = DB(json_data['db_name'], tables)
            self.location = location
        else:
            print('There is no db. Please enter valid path')

    def save_db(self):
        try:
            json_data = self.__get_db_data()
            json.dump(json_data, open(self.location, "w+"))
        except Exception as e:
            print(e)

    def delete_db(self):
        os.remove(self.location)


# db = DBManager()
# db.create_db('new_db')
# db.load_db('D:\\Дз\\IT\\new_db.json')
# db.add_table('User')
# table = db.get_table('User')
# table.add_column('first_name', 'str', False)
# table.add_column('last_name', 'str', False)
# table.add_column('phone', 'int', True)
# db.add_table('Company')
# table = db.get_table('Company')
# table.add_column('name', 'int', True)
# db.save_db()
# table = db.get_table('User')
# table.add_row({'first_name': 'Jake', 'last_name': 'Dog', 'phone': None})
# table.add_row({'first_name': 'Dima', 'last_name': 'Teltsov', 'phone': 12345})
# db.save_db()
# table = db.get_table('Company')
# table.rename_table('Corp')
# db.save_db()
