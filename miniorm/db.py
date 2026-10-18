import sqlite3

_connection = None


def connect(path="orm.db"):
    global _connection
    _connection = sqlite3.connect(path)

    return _connection


def get_connection():
    if _connection is None:
        connect()
    return _connection


def close_connection():
    global _connection

    if _connection is not None:
        _connection.close()
        _connection = None
