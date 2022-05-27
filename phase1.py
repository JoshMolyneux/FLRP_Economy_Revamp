"""
PHASE 1: Refund all inventory items (except legacy) at 60% market value.
"""
import mariadb
from items import ITEM_DICT, OMIT_ITEMS
from config import config
import math


def phase1(connect, refund_percentage):
    input("Please press 'ENTER' to begin PHASE 1 refunds")

    cursor = connect.cursor()
    try:
        cursor.execute(
            "SELECT _Key, _SteamID, _Inventory, _Money FROM players")
        # Store all the results in a variable
        result = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error: {e}")

    # Going to use these for visual feedback
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
            f"ID: {key} \nSteamID: {steamid} \nOld Wallet: ${money}\n"
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

        # Some log file additions
        log_file_percentage_decrease.write(
            f"New Wallet (Wallet + Inventory): ${money+refund}\n"
        )

        # Execute the percentage decreaseRound the refund and round the value
        # up to the nearest integer
        refund = int(math.ceil(refund * refund_percentage))

        # More log file additions
        log_file_percentage_decrease.write(
            f"Phase 1 Wallet (After % Decrease on inventory value): ${money+refund}\n\n"
        )

        # Update the user's Money AND inventory
        cursor = connect.cursor()
        try:
            cursor.execute(
                f"UPDATE players SET _Money = _Money + {refund}, _Inventory = '{inv_edited}' WHERE _Key = {key}"
            )
        except mariadb.Error as e:
            print(f"Error: {e}")
        cursor.close()

        COUNTER += 1
        # Some visual feedback in console
        print(COUNTER, "of", ROW_COUNT, "refunded!")

    print("\n[!]PHASE 1 REFUND SUCCESSFULLY EXECUTED[!]")
