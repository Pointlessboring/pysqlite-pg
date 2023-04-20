###############################################################
# Daily grinding 
#
# sqlite, openpyxl, csv files...
#
# Using airbnb data from http://insideairbnb.com/get-the-data/
#
# Concept refresher: iterators 
#
# ToDo: Clean-up/Format EXCEL file. Add header row. 

import sqlite3
import csv
import time
from openpyxl import Workbook
from datetime import date, datetime, timedelta

# mark start time for measurement
start_time = time.time()

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
# Perform data treatment here... 

sqlstring = ("SELECT t1.listing_id, t1.maxprice, t2.name, t2.picture_url, t2.host_name, t2.host_picture_url, t2.neighbourhood_group_cleansed, t2.latitude, t2.longitude "
            "FROM (SELECT listing_id, max(price) AS maxprice from calendar GROUP by listing_id) as t1 "
            "JOIN (SELECT id, name, picture_url, host_name, host_picture_url, neighbourhood_group_cleansed, latitude, longitude FROM listing) as t2 "
            "ON t1.listing_id = t2.id")
data = cursor.execute(sqlstring).fetchall()

#####################################
# Write data back to excel file/sheet
#

print("Saving Data into an Excel workbook.")
wb = Workbook()
ws = wb.active
ws.title = "NY Airbnb max price per listing"

x = 0
for line in data:
    x += 1
    y = 0
    for element in line:
        y += 1
        fixed_element = element
        # testing for special case where element starts with '=' which causes error as EXCEL believes it is a formula. 
        if element != "" and element[0] == "=":
            fixed_element = "'" + fixed_element
        ws.cell(row = x, column = y, value = fixed_element)

# Saving to excel file. 
wb.save('UselessAirBnBFile.xlsx')

# Clean-up. Closing connections
print("Wrapping up.")
conn.close()

# Calculating elapsed time since marker
print(f"Elapsed time: {round(time.time()-start_time,2)} seconds")