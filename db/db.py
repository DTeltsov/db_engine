import json
import os
from pydoc import locate
from typing import List
from pathlib import Path
import numpy as np
from .exceptions import (
    InvalidValueError,
    AlredyExistsError,
    NotFoundError,
    IsNullColumnError,
    InvalidUnionError
)


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

    @staticmethod
    def validate_value(column, value):
        if column.column_attr not in ['color', 'colorInvl']:
            if ((type(value) != locate(column.column_attr)) or
                    (not value and not column.is_null)):
                raise InvalidValueError(value)
        else:
            value = np.array(value)
            if value.shape[0] != 3:
                raise InvalidValueError(list(value))
            elif value.ndim == 1 and column.column_attr == 'colorInvl':
                raise InvalidValueError(list(value))
            elif value.ndim == 2 and column.column_attr == 'color':
                raise InvalidValueError(list(value))
            elif any(i > 255 or i < 0 for i in value):
                raise InvalidValueError(list(value))

    def update_table(self, table_name: str = None):
        if table_name:
            self.table_name = table_name

    def get_columns(self):
        return self.columns

    def get_column(self, column_name: str):
        for column in self.columns:
            if column.column_name == column_name:
                return column
        raise NotFoundError(column_name)

    def add_column(
        self,
        column_name: str,
        attr: str,
        is_null: bool,
        default_value
    ):
        try:
            self.get_column(column_name)
            raise AlredyExistsError(column_name)
        except NotFoundError:
            if not is_null and self.rows and not default_value:
                raise IsNullColumnError
            elif not is_null and self.rows and default_value:
                column = Column(column_name, attr, is_null)
                self.columns.append(column)
                for row in self.get_rows():
                    self.validate_value(column, default_value)
                    row.append(default_value)
            elif ((not is_null and not self.rows) or
                    is_null):
                column = Column(column_name, attr, is_null)
                self.columns.append(column)

    def delete_column(self, column_name: str):
        column = self.get_column(column_name)
        column_index = self.columns.index(column)
        self.columns.remove(column)
        for row in self.rows:
            try:
                del row[column_index]
            except IndexError:
                pass
            if not row:
                self.rows.remove(row)

    def update_column(self, column_name, name, attr, is_null):
        column = self.get_column(column_name)
        column.column_name = name
        column.column_attr = attr
        column.is_null = is_null

    def get_rows(self):
        return self.rows

    def get_row(self, row_index):
        try:
            return self.rows[row_index]
        except IndexError:
            raise NotFoundError(row_index)

    def add_row(self, row: dict):
        values = []
        for key, value in row.items():
            column = self.get_column(key)
            if not column:
                raise NotFoundError(column)
            self.validate_value(column, value)
            values.append(value)
        self.rows.append(values)

    def delete_row(self, row_index):
        row = self.get_row(row_index)
        self.rows.remove(row)

    def update_row(self, row_index, row):
        values = []
        for key, value in row.items():
            column = self.get_column(key)
            if not column:
                raise NotFoundError(column)
            self.validate_value(column, value)
            values.append(value)
        self.rows[row_index] = values


class DB:
    def __init__(self, name: str, tables: Table = None):
        self.name = name

        if tables:
            self.tables = tables
        else:
            self.tables = []


class DBManager:
    def __init__(self):
        self.db = DB('')
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
        raise NotFoundError(table_name)

    def add_table(self, table_name: str):
        try:
            self.get_table(table_name)
            raise AlredyExistsError(table_name)
        except NotFoundError:
            table = Table(table_name)
            self.db.tables.append(table)
            return table

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

    def union_tables(self, table_name1, table_name2):
        table1 = self.get_table(table_name1)
        table2 = self.get_table(table_name2)
        if len(table1.columns) == len(table2.columns):
            result_columns = table1.columns
            result_rows = table1.rows + table2.rows
            result_table = Table('result', result_columns, result_rows)
            return result_table
        else:
            raise InvalidUnionError

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
            return self.db
        except Exception as e:
            return e

    def load_db(self, location: str):
        location = Path(location)
        if os.path.exists(location):
            json_data = json.load(open(location))
            tables = self.__load_tables(json_data['tables'])
            self.db = DB(json_data['db_name'], tables)
            self.location = location
        else:
            raise NotFoundError(str(location).replace('.json', ''))

    def save_db(self):
        try:
            json_data = self.__get_db_data()
            json.dump(json_data, open(self.location, "w+"))
        except Exception as e:
            print(e)

    def delete_db(self):
        os.remove(self.location)
