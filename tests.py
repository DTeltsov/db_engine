from gui.load_database.load_database import LoadDatabaseDialog
from app import MainWindow
from db.db import Table, DBManager
from db.exceptions import InvalidValueError, InvalidUnionError
import unittest
from unittest import mock
import sys
from PyQt5 import QtWidgets


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    if args[0] == 'http://localhost:8000/api/dbs':
        return MockResponse({"data": 'Everything is fine'}, 200)
    elif args[0] == 'http://localhost:8000/api/db/new_db':
        return MockResponse(
            {
                "data": {
                    "db_name": "new_db",
                    "tables": [
                        {
                            "table_name": "Test"
                        }
                    ]
                },
                "links": {
                    "db_tables": [
                        {
                            "self": {
                                "href": "http://localhost:8000/api/db/new_db/table/Test"
                            }
                        }
                    ]
                }
                },
            200
        )


def mocked_requests_delete(*args, **kwargs):
    if args[0] == 'http://localhost:8000/api/db/new_db/Test/row/0':
        return MockResponse({'msg': 'Deleted'}, 200)


def mocked_selected(*args, **kwargs):
    return 0


class LoadDialogMethods(unittest.TestCase):
    def test_data_formating(self):
        w = LoadDatabaseDialog()
        data = w.format_data([{'name': 'test'}], 'Local')
        self.assertListEqual(data, [[{'db': 'test', 'db_type': 'Local'}, 'test-Local']])

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_dbs_get(self, mock_get):
        w = LoadDatabaseDialog()
        data = w.load_remote_db_paths()
        self.assertEqual(data, 'Everything is fine')


class MainWindowMethods(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_db_get(self, mock_get):
        w = MainWindow()
        w.db_type = 'Remote'
        w.db = 'new_db'
        data = w.get_tables()
        self.assertEqual(data[0][1], 'Test')

    @mock.patch('requests.delete', side_effect=mocked_requests_delete)
    @mock.patch('PyQt5.QtWidgets.QTableWidget.currentRow', side_effect=mocked_selected)
    def test_row_delete(self, mock_delete, mock_select):
        w = MainWindow()
        w.db_type = 'Remote'
        w.db = 'new_db'
        w.table = 'http://localhost:8000/api/db/new_db/Test'
        data = w.delete_row()
        self.assertEqual(data, 200)


class DBTableMethods(unittest.TestCase):
    def test_color_validation(self):
        t = Table('test')
        t.add_column('test_color', 'color', True, None)
        column = t.get_column('test_color')
        with self.assertRaises(InvalidValueError):
            t.validate_value(column, [1, 2])

    def test_color_colorInvl_validation(self):
        t = Table('test')
        t.add_column('test_color', 'colorInvl', True, None)
        column = t.get_column('test_color')
        with self.assertRaises(InvalidValueError):
            t.validate_value(column, [1, 2, 3])

    def test_union(self):
        d = DBManager()
        d.add_table('test1')
        t1 = d.get_table('test1')
        t1.add_column('color', 'color', True, None)
        t1.add_column('age', 'int', True, None)
        d.add_table('test2')
        t2 = d.get_table('test2')
        t2.add_column('color', 'color', True, None)
        t2.add_column('age', 'int', True, None)
        t2.add_column('name', 'str', True, None)
        with self.assertRaises(InvalidUnionError):
            d.union_tables('test1', 'test2')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    unittest.main()
