#######
#
# 4th try

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Create a database connection to SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

    except Error as e:
        print(e)
    
    return conn

if __name__ == '__main__':

    folder = "/Users/GLU/Library/Mobile Documents/com~apple~CloudDocs/EG_Varia/Python/pysqlite-pg/"
    filename = "aquarium.db"
    fullname = folder + filename
    cursor = create_connection(fullname)

    rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    print(rows)

