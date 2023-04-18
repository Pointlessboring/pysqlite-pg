#########
#
# Daily Python/SQLite grind
#

import sqlite3
from datetime import date, timedelta, datetime
from random import randint

# Create DB filename
filename = "UselessDB" + date.today().strftime("%y%m%d")+".db"

# open DB
try:
    conn = sqlite3.Connection(filename)

except Error as e: 
    print(f"Error connection to database: {e}")

# create cursor into DB
cursor = conn.cursor()

# check it table exist
tables = cursor.execute("SELECT name FROM sqlite_schema").fetchall()

if tables == [] or ('employees' not in tables[0]):
    cursor.execute("""
                    CREATE TABLE employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    position TEXT,
                    salary INTEGER,
                    startdate DATE,
                    enddate DATE
                    )
                    """)

for i in range(0,10):
    name = "First Last"
    position = "Job Title"
    salary = randint(50000, 100000)
    startdate = date.today() - timedelta(days=randint(1,10000))
    if randint(1,100) > 99:
        enddate = (datetime.today() - timedelta(days=randint(1,10000))).strftime("%Y-%m-%d")
    else: 
        enddate = 'NULL'
    cursor.execute("INSERT INTO employees (name, position, salary, startdate, enddate) VALUES(?,?,?,?,?)", (name, position, salary, startdate, enddate))
    conn.commit()

conn.close()