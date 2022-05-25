"""Automates queries sent to the database to complete the following:
- Refund all inventory items at 60% market value.
- Decrease wallets using a tax bracket system as follows when the player has.
  For the sake of the script, we'll give them names:
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
- Descale wallets by a fixed number

Usage:
    ./run.py

Author:
    Joshua Molyneux - 05-2022
"""

import mariadb
import sys
from items import ITEM_DICT


# Global variables for our requirements
INVENTORY_REFUND_PERCENTAGE = 60
DESCALE_VALUE = 5

# MaraDB Database Details - CHANGE WHERE NECCESSARY
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
        database=SQL_DATABASE
    )
except mariadb.Error as e:
    print(f"There was an error connecting to MariaDB: {e}")
    sys.exit(1)


"""
Refund all inventory items at 60% market value
"""
cursor = connect.cursor()

cursor.execute("SELECT _Key, _Name, _SteamID, _Inventory FROM players")
file = open("econ_refund_log.txt", "a", encoding="utf-8")
for (key, name, steamid, inventory) in cursor:
    file.write(f"ID: {key}\nName: {name} \nSteamID: {steamid} \n\n")
