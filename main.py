"""Automates queries sent to the database to complete the following:
- PHASE 1 Refund all inventory items (except legacy) at 60% market value.
- PHASE 2 Decrease wallets using a tax bracket system as follows when the player has.
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
- PHASE 3 Descale wallets by a fixed number

Usage:
    ./main.py

Author:
    Joshua Molyneux - 05-2022
    https://fearlessrp.net/member.php?action=profile&uid=17825
    Discord: @Awestruck#3143
"""

import mariadb
import sys
from phase1 import phase1
from phase2 import phase2
from phase3 import phase3


# Global variables for our requirements
INVENTORY_REFUND_PERCENTAGE = 0.6  # 40% DECREASE
DESCALE_VALUE = 3

# MariaDB Database Details - CHANGE WHERE NECCESSARY
SQL_HOST = 'localhost'
SQL_PORT = 3306
SQL_USER = 'root'
SQL_PASSWORD = ''
SQL_DATABASE = 'fearless_cityrp'

try:
    connect = mariadb.connect(
        user=SQL_USER,
        password=SQL_PASSWORD,
        host=SQL_HOST,
        port=SQL_PORT,
        database=SQL_DATABASE,
        autocommit=True
    )
except mariadb.Error as e:
    print(f"There was an error connecting to MariaDB: {e}")
    sys.exit(1)

# Get the total sum of money BEFORE the changes
cursor = connect.cursor()
try:
    cursor.execute("SELECT SUM(_Money) FROM players")
    # Store all the results in a variable
    TOTAL_CASH_START = cursor.fetchone()
except mariadb.error as e:
    print(f"Error getting SUM value: {e}")
cursor.close()


if __name__ == '__main__':
    # Run our phases
    phase1(connect, INVENTORY_REFUND_PERCENTAGE)
    phase2(connect)
    phase3(connect, DESCALE_VALUE)


# Get the total sum of money AFTER the changes
cursor = connect.cursor()
try:
    cursor.execute("SELECT SUM(_Money) FROM players")
    TOTAL_CASH_END = cursor.fetchone()
except mariadb.error as e:
    print(f"Error: {e}")
cursor.close()


# Set all Inventory values to ZERO
cursor = connect.cursor()
try:
    cursor.execute("UPDATE players SET _Invvalue = 0")
except mariadb.error as e:
    print(f"Error: {e}")
cursor.close()

# Print the total sum of money to the console
total = int(TOTAL_CASH_START[0]) - int(TOTAL_CASH_END[0])
print(f"\n\n Total money BEFORE: ${int(TOTAL_CASH_START[0])}")
print(f"\n\n Total money AFTER: ${int(TOTAL_CASH_END[0])}")
print(f"\n\n Total money removed: ${total}")
connect.close()
