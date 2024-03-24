import sqlite3


def get_connection(db='emails.db'):
    conn = sqlite3.connect(db)
    return conn
