import _sqlite3
from flask import g

from application import app

DATABASE = './data/censoescolar.db'


def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = _sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()