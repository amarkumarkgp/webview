import os
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)
    return conn


def get_connection(db_name):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    database = os.path.join(base_dir, db_name)
    # create a database connection
    conn = create_connection(database)
    return conn



