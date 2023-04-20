######################################
# Daily Grind
#
# Food for thought: Performance considerations while writing to file
# - use of with open() construct ; or
# - f = open() , and the f.close()

import sqlite3, time
from datetime import date, datetime, timedelta

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

# Close final 
with open(logname, 'a') as f:
    f.write(f'{datetime.now().strftime("%y-%m-%d %X")} Ending Daily grind program.\n')

# Calculating elapsed time. Notice the float to 2 decimal place formatting
print(f"Total runtime was: {(time.time()-start_timer):.2f} seconds\n")