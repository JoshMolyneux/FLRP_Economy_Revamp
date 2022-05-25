"""Automates queries sent to the database to complete the following:
- Refund all inventory items (except legacy) at 60% market value.
- Decrease wallets using a tax bracket system as follows when the player has.
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
    https://fearlessrp.net/member.php?action=profile&uid=17825
    Discord: @Awestruck#3143
"""

import mariadb
import sys
import math
from items import ITEM_DICT, OMIT_ITEMS


# Global variables for our requirements
INVENTORY_REFUND_PERCENTAGE = 0.4  # 60% DECREASE
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
        database=SQL_DATABASE,
        autocommit=True
    )
except mariadb.Error as e:
    print(f"There was an error connecting to MariaDB: {e}")
    sys.exit(1)


"""
PHASE 1: Refund all inventory items (except legacy) at 60% market value.
"""

input("Please press 'ENTER' to begin PHASE 1 refunds")

cursor = connect.cursor()
try:
    cursor.execute("SELECT _Key, _SteamID, _Inventory, _Money FROM players")
    # Store all the results in a variable
    result = cursor.fetchall()
except mariadb.error as e:
    print(f"Error: {e}")

ROW_COUNT = cursor.rowcount
COUNTER = 0
cursor.close()
# Append to a file - and/or create it if it doesn't exist
log_file_percentage_decrease = open(
    "PHASE_1_refund_log.txt", "a", encoding="utf-8"
)

# Loop through all the rows of players
for row in result:
    key = row[0]
    steamid = row[1]
    inventory = row[2]
    money = row[3]

    log_file_percentage_decrease.write(
        f"ID: {key} \nSteamID: {steamid} \nOld Wallet: {money}\n"
    )

    # If the inventory is empty, go to the next iteration of the loop
    if inventory is None:
        log_file_percentage_decrease.write("[!]NO INVENTORY[!]")
        continue

    # Initialise a variable that we'll use to increment our refund value
    refund = 0

    # Dissect the inventory string into their own objects
    inv = inventory.split("; ")
    # Found some strange entries that had a semi-colon after the value
    # ... even though nothing followed it lol
    inv = [i.replace(";", "") for i in inv]
    inv_items = [i.split(": ", 2) for i in inv]
    # Init an empty list for new inventories containg legacy items
    inv_edited = []

    # Get the items and their quantities
    for i in inv_items:
        # Check the users items are in the dictionary and refund them
        if i[0] in ITEM_DICT.keys():
            refund += ITEM_DICT[i[0]] * float(i[1])
        # If they have legacy vehicles add them to a new list
        elif i[0] in OMIT_ITEMS:
            inv_edited.append(i)

    # Let's fix our inventory string after we ripped it apart
    # Check if we have any values in there
    if len(inv_edited) >= 1:
        inv_edited = [": ".join(i) for i in inv_edited]
        inv_edited = "; ".join(inv_edited)
    else:
        inv_edited = ""

    log_file_percentage_decrease.write(
        f"New Wallet (Wallet + Inventory): {money+refund}\n"
    )

    refund = int(math.ceil(refund * INVENTORY_REFUND_PERCENTAGE))

    log_file_percentage_decrease.write(
        f"New Wallet (After % Decrease on inventory value): {money+refund}\n\n"
    )

    cursor = connect.cursor()
    try:
        cursor.execute(
            f"UPDATE players SET _Money = _Money + {refund}, _Inventory = '{inv_edited}' WHERE _Key = {key}"
        )
    except mariadb.Error as e:
        print(f"Error: {e}")

    COUNTER += 1
    # Some visual feedback in console
    print(COUNTER, "of", ROW_COUNT, "refunded!")

cursor.close()
print("\n[!]PHASE 1 REFUND SUCCESSFULLY EXECUTED[!]")


"""
PHASE 2: Decrease wallets using a tax bracket system as follows when the player has.
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
"""

input("Please press 'ENTER' to begin PHASE 2 deductions")
