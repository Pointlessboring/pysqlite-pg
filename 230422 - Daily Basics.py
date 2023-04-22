################################
# Daily Grind...
# 

import sqlite3, csv, time, tkinter
from datetime import date, datetime, timedelta

def english_ord(n):
    """ simple function to return the English Ordinal Suffix: st, nd, rd, th"""
    return f"{n}"+ ("th" if (n%100) not in [11,12,13] else ( ["st", "nd", "rd"][n%10-1]))

# Start timer to measure elapsed time later
start_timer = time.time()

# Greet user, display date.
daynum = english_ord(int(date.today().strftime('%j')))
print(f"Welcome! Today's date is {date.today().strftime(f'%A %b %d, the {daynum} day of %Y')}")

# Creating names for our files
basename = "Useless"+date.today().strftime("%y%m%d")
logfile = basename + ".log"
dbfile = basename + ".db"
xlfile = basename + ".xlsx"

window = tkinter.Tk()
greeting = tkinter.Label(text="Hello, Tkinter")
time.sleep(20)