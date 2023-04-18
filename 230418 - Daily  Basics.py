######
#
# Daily SQLite Grind

import sqlite3
from sqlite3 import Error

from openpyxl import load_workbook

from datetime import date, datetime, timedelta
from random import randint

#####################################
# Basic date manipulation exercises
#
# 

today = date.today()
print(f"Today is: {today.strftime('%A %B %d, the %jth day of %Y')}")

####################################
# Getting names from an excel file
#

try: 
    workbook = load_workbook(filename="FirstLastNames.xlsx")
    sheets = workbook.sheetnames
    print(sheets)

    lastnames = []
    firstnames = []

    sheet = workbook["Surnames"]
    for cell in sheet["A"]:
        lastnames.append(cell.value)
    lastnames.sort()
    
    sheet = workbook["Firstnames"]
    for row in sheet.iter_rows():
       firstnames.append((row[0].value, row[1].value))
    firstnames.sort()
 
except Error as err:
    print(f"Error Reading first/last name dataset: {err}")

###############################
# DB processing
#

# Create DB filename
filename = "UselessDB" + today.strftime("%y%m%d")+".db"

# open DB connection

try: 
    conn = sqlite3.Connection(filename)

except Error as err:
    print(err)

# Create cursor into DB
cursor = conn.cursor()

# Check if tables were created already 
tables = cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table'").fetchall()

# if the people table does not exist, create it.

if tables == [] or ('people' not in tables[0]):
    cursor.execute("""
                    CREATE TABLE people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first CHAR(30),
                    last CHAR(30),
                    birthday DATE,
                    gender CHAR(1)
                    )
                    """)

# Add 1000 records to the people table.

for i in range(1,1000):
    firstnameID = randint(0,len(firstnames)-1)
    lastnameID = randint(0,len(lastnames)-1)
    cursor.execute(f"INSERT INTO people (first, last, birthday, gender) VALUES(?,?,?,?)", 
                    (firstnames[firstnameID][0], 
                     lastnames[lastnameID], 
                     date.today()-timedelta(randint(0,365*80)),
                     firstnames[firstnameID][1]
                    ))
    conn.commit()


conn.close()