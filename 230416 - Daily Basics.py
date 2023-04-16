##################
# 2023/04/16
# Daily practice to memorize SQLite manipulation commands
#
# Super basic stuff. Practice makes perfect...

import sqlite3
from datetime import date

# construct a filename with today's date. 

today = date.today().strftime("%y%m%d")
filename = "UselessDB_" + today + ".db"

# Connect to the database. create the file.
connection = sqlite3.Connection(filename)
cursor = connection.cursor()

# Create 1st Table

cursor.execute("""CREATE TABLE games (
                        year INTEGER, 
                        venue TEXT, 
                        player1 TEXT, 
                        player2 TEXT)""")

# Insert values into table

cursor.execute("INSERT INTO games VALUES (2023, 'Home', 'Black', 'White') ")
cursor.execute("INSERT INTO games VALUES (2022, 'HQ', 'P1', 'P2') ")

# Commit the info to the DB. 
connection.commit()

# Read back values
rows = cursor.execute("SELECT year, venue, player1, player2 FROM games").fetchall()
print(rows)

connection.close()

