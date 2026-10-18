import sqlite3

_connection = None


def connection():
    connection = sqlite.connect("orm.db")
