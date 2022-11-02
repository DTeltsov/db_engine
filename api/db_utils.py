from db.db import DBManager


def setup_db(app):
    db = DBManager()
    app['db'] = db