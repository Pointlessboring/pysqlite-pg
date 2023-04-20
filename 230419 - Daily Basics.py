###############################################################
# Daily grinding 
#
# sqlite, openpyxl, csv files...
#
# Using airbnb data from http://insideairbnb.com/get-the-data/
#
# Concept refresher: iterators 
#

import sqlite3
import csv
from datetime import date, datetime, timedelta

# Inital message. 
print(f"\nToday is {date.today().strftime('%A %B %d, the %jth day of %Y')}.\n")

# Create filename for daily temp DB file
filename = "Useless" + date.today().strftime("%y%m%d")+".db"

# Open DB connection
conn = sqlite3.Connection(filename)
cursor = conn.cursor()

# Check if listing table exist, otherwise create it
print("Validating if LISTING table exists in the database.")
tables = cursor.execute("SELECT name from sqlite_schema").fetchall()
print(tables)

if tables == [] or ('listing',) not in tables:      

    # importing csv file
    with open("NY-airbnb-listings.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # csv_reader is an iterator. Converted to a tuple of data to use it more freely.
        csvDB = tuple(csv_reader) 

    # Get csv file info: # of fields, header names, etc.
    fieldnames = csvDB[0]
    nbfields = len(fieldnames)
    fieldnamestring = "'" + "', '".join(fieldnames) + "'"

    sqlstring = "CREATE TABLE listing ("            # Beginning of SQL CREATE command
    for field in fieldnames:
        sqlstring += " " + field + " TEXT,"         # Add the various field to create
    
    sqlstring = sqlstring[:-1] + ")"                # Remove last comma and close the bracket
    cursor.execute(sqlstring)

    print("Creating LISTING table into the database.")

###############################################
# Populate the database with data from CSV file
#
# We create a SQLstring command and a variable holding the data to be insert

    print("Populating LISTING table into the database.")

    for row in csvDB[1:]:
        sqlstring = f"INSERT INTO listing ({fieldnamestring}) VALUES ({('?,'*nbfields)[:-1]})"
        cursor.execute(sqlstring, row)
    conn.commit()


# Check if calendar table exist, otherwise create it
print("Validating if CALENDAR table exists in the database.")
tables = cursor.execute("SELECT name from sqlite_schema WHERE type = 'TABLE' ").fetchall()


if tables == [] or ('calendar',) not in tables:      

    # importing csv file
    with open("NY-airbnb-calendar.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # csv_reader is an iterator. Converted to a tuple of data to use it more freely.
        csvDB = tuple(csv_reader) 

    # Get csv file info: # of fields, header names, etc.
    fieldnames = csvDB[0]
    nbfields = len(fieldnames)
    fieldnamestring = "'" + "', '".join(fieldnames) + "'"

    sqlstring = "CREATE TABLE calendar ("            # Beginning of SQL CREATE command
    for field in fieldnames:
        sqlstring += " " + field + " TEXT,"         # Add the various field to create
    
    sqlstring = sqlstring[:-1] + ")"                # Remove last comma and close the bracket
    cursor.execute(sqlstring)

    print("Creating CALENDAR table into the database.")

###############################################
# Populate the database with data from CSV file
#
# We create a SQLstring command and a variable holding the data to be insert

    print("Populating CALENDAR table into the database.")

    for row in csvDB[1:]:
        sqlstring = f"INSERT INTO calendar ({fieldnamestring}) VALUES ({('?,'*nbfields)[:-1]})"
        cursor.execute(sqlstring, row)
    conn.commit()

#########
#
# Next steps... Perform data treatment here... 
#



# Clean-up. Closing connections
conn.close()