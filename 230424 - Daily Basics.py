#############
# Daily Grind

import csv, sqlite3, time
from datetime import date, datetime, timedelta

def english_ord(n):
    return str(n) + ("th" if ((n%100) in [11,12,23]) else (["th", "st", "nd", "rd"]+["th"]*7)[n%10])


start_time = time.time()

# Generating temporary file name from today's date
basename = "Useless"+date.today().strftime("%y%m%d")
logfilename = basename + ".log"
dbfilename = basename + ".db"
xlfilename = basename + ".xlsx"

# Print greeting and today's date with correct english ordinal for day and day number.
print(f"Welcome! Today is: {date.today().strftime(f'%A %B ')}"+
                            english_ord(int(date.today().strftime('%d')))+
                            f", the {english_ord(int(date.today().strftime('%j')))}"+
                            f" day of {date.today().strftime('%Y')}"
                            )

