######################################
# Daily Grind
#
# ToDo: Need to rewrite this with functions as the code is being repeated 3 times.
#

import sqlite3, time, csv
from datetime import date, datetime, timedelta
from openpyxl import Workbook

# start timer for performance measurement
start_timer = time.time()

# Greeting message
print(f"\nWelcome! Today is {date.today().strftime('%A %B %d, the %jth day of %Y')}\n")

# Create filenames based on today's date
basename = 'Useless'+date.today().strftime("%y%m%d")
logname = basename + ".log"               # log file
dbname = basename + ".db"                 # DB file
xlname = basename + ".xlsx"               # Excel file

# Begin logging activities
with open(logname, 'a') as f:
    f.write(f'{datetime.now().strftime("%y-%m-%d %X")} Launching Daily grind program...\n')

# open DB Connection
conn = sqlite3.Connection(dbname)
cursor = conn.cursor()

# Get list of tables from DB, create them if they are not there.
tables = cursor.execute("SELECT name from sqlite_schema").fetchall()

print("Validating if POPULATION table exists in the database.")

if tables == [] or ('population',) not in tables:      

    # importing csv file
    with open("Datasets/worldbank-population-2021.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # csv_reader is an iterator. Converted to a tuple of data to use it more freely.
        csvDB = tuple(csv_reader) 

    # Get csv file info: # of fields, header names, etc.
    fieldnames = csvDB[0]
    nbfields = len(fieldnames)
    fieldnamestring = "'" + "', '".join(fieldnames) + "'"
  
    sqlstring = "CREATE TABLE population ("            # Beginning of SQL CREATE command
    for field in fieldnames:
        sqlstring += " '" + field + "' TEXT,"         # Add the various field to create
    
    sqlstring = sqlstring[:-1] + ")"                # Remove last comma and close the bracket
    cursor.execute(sqlstring)

    print("Creating POPULATION table into the database.")

###############################################
# Populate the database with data from CSV file
#
# We create a SQLstring command and a variable holding the data to be insert

    print("Populating POPULATION table into the database.")

    for row in csvDB[1:]:
        sqlstring = f"INSERT INTO population ({fieldnamestring}) VALUES ({('?,'*nbfields)[:-1]})"
        cursor.execute(sqlstring, row)
    conn.commit()

print("Validating if GDP table exists in the database.")

if tables == [] or ('gdp',) not in tables:      

    # importing csv file
    with open("Datasets/worldbank-GDP-2021.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # csv_reader is an iterator. Converted to a tuple of data to use it more freely.
        csvDB = tuple(csv_reader) 

    # Get csv file info: # of fields, header names, etc.
    fieldnames = csvDB[0]
    nbfields = len(fieldnames)
    fieldnamestring = "'" + "', '".join(fieldnames) + "'"

    sqlstring = "CREATE TABLE gdp ("            # Beginning of SQL CREATE command
    for field in fieldnames:
        sqlstring += " '" + field + "' TEXT,"         # Add the various field to create
    
    sqlstring = sqlstring[:-1] + ")"                # Remove last comma and close the bracket
    cursor.execute(sqlstring)

    print("Creating GDP table into the database.")

###############################################
# Populate the database with data from CSV file
#
# We create a SQLstring command and a variable holding the data to be insert

    print("Populating GDP table into the database.")

    for row in csvDB[1:]:
        sqlstring = f"INSERT INTO gdp ({fieldnamestring}) VALUES ({('?,'*nbfields)[:-1]})"
        cursor.execute(sqlstring, row)
    conn.commit()

print("Validating if DEBT table exists in the database.")

if tables == [] or ('debt',) not in tables:      

    # importing csv file
    with open("Datasets/worldbank-External Debt-2021.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # csv_reader is an iterator. Converted to a tuple of data to use it more freely.
        csvDB = tuple(csv_reader) 

    # Get csv file info: # of fields, header names, etc.
    fieldnames = csvDB[0]
    nbfields = len(fieldnames)
    fieldnamestringDEBT = "'" + "', '".join(fieldnames) + "'"

    sqlstring = "CREATE TABLE debt ("            # Beginning of SQL CREATE command
    for field in fieldnames:
        sqlstring += " '" + field + "' TEXT,"         # Add the various field to create
    
    sqlstring = sqlstring[:-1] + ")"                # Remove last comma and close the bracket
    cursor.execute(sqlstring)

    print("Creating DEBT table into the database.")

###############################################
# Populate the database with data from CSV file
#
# We create a SQLstring command and a variable holding the data to be insert

    print("Populating GDP table into the database.")

    for row in csvDB[1:]:
        sqlstring = f"INSERT INTO debt ({fieldnamestring}) VALUES ({('?,'*nbfields)[:-1]})"
        cursor.execute(sqlstring, row)
    conn.commit()

#########
# Perform data treatment here... 

sqlstring = ('Select t1."Country Name", t1.debtvalue, t2.pop '
            'FROM (SELECT "Country Name", "2021 [YR2021]" as debtvalue from debt) AS t1 '
            'JOIN ( SELECT "Country Name", "2021 [YR2021]" AS pop from population) AS t2 '
            'ON t1."Country Name" = t2."Country Name" ')

data = cursor.execute(sqlstring).fetchall()

#####################################
# Write data back to excel file/sheet
#

print("Saving Data into an Excel workbook.")
wb = Workbook()
ws = wb.active
ws.title = "World Bank Country information"

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
wb.save('UselessWorldBank.xlsx')

# Clean-up. Closing connections
print("Wrapping up.")
conn.close()

# Close final 
with open(logname, 'a') as f:
    f.write(f'{datetime.now().strftime("%y-%m-%d %X")} Ending Daily grind program.\n')

# Calculating elapsed time. Notice the float to 2 decimal place formatting
print(f"Total runtime was: {(time.time()-start_timer):.2f} seconds\n")