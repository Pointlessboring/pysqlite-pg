################################
# Daily Grind...
# 

import sqlite3, csv, time
import tkinter as tk
from datetime import date, datetime, timedelta

def english_ord(n):
    return str(n) + ("th" if ((n%100) in [11,12,23]) else (["th", "st", "nd", "rd"]+["th"]*7)[n%10])

# Start timer to measure elapsed time later
start_timer = time.time()

print(english_ord(3))

# Greet user, display date.
daynum = english_ord(int(date.today().strftime('%j')))
print(f"Welcome! Today's date is {date.today().strftime(f'%A %b %d, the {daynum} day of %Y')}")

# Creating names for our files
basename = "Useless"+date.today().strftime("%y%m%d")
logfile = basename + ".log"
dbfile = basename + ".db"
xlfile = basename + ".xlsx"

window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
tk.mainloop()