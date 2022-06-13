"""
PHASE 1: Refund all inventory items (except legacy) at 60% market value.
"""
import mariadb
import sys
from .items import ITEM_DICT, OMIT_ITEMS
from config import db_details, INVENTORY_REFUND_PERCENTAGE as refund_percentage
import math
from . import get_all_players

COUNTER = 0

# Connect to our MariaDB database
try:
    connect = mariadb.connect(
        **db_details,
        autocommit=True
    )
except mariadb.Error as e:
    print(f"There was an error connecting to MariaDB: {e}")
    sys.exit(1)


def check_user_already_processed_phase1(key):
    """
    A function to check if a user has already been processed through Phase 1.
    We can return a boolean value and use it as a condition when processing a user.
    """

    cursor = connect.cursor()
    try:
        cursor.execute(
            f"SELECT phase1_verify FROM players WHERE _Key = {key}"
        )
        result = cursor.fetchone()
        if result[0] == 1:
            return True
    except mariadb.Error as e:
        print(f"Error: {e}")
    cursor.close()


def user_has_inventory(inventory):
    if inventory == "" or inventory == "NULL" or inventory is None:
        return False


def convert_inventory_into_items(inventory):
    """
    A function that takes a block of text with a set format and dissects it into a list
    of separate strings and their quantities.
    """

    inv = inventory.split("; ")
    # Found some strange entries that had a semi-colon after the value with no suffix
    inv = [i.replace(";", "") for i in inv]
    items = [i.split(": ", 2) for i in inv]

    return items


def refund_user(items, inventory):
    """
    A function to process the refund of a user dependant on the items in their inventory, their market value
    and the quantity of that item the user has.
    """

    refund = 0

    for item in items:
        # Check the users items are in the dictionary and refund them
        if item[0] in ITEM_DICT.keys():
            refund += ITEM_DICT[item[0]] * float(item[1])
        # If they have legacy vehicles add them to a new list
        elif item[0] in OMIT_ITEMS:
            inventory.append(item)

    pre_value = refund

    refund = int(math.ceil(refund * refund_percentage))

    post_value = refund

    return pre_value, refund, post_value


def join_new_inventory(inventory):
    """
    A function to rebuild the new inventory from our new list of items from OMIT_ITEMS depending
    on if the user had them. We also want to give them a default of 5 Chinese.
    """

    if len(inventory) >= 1:
        inventory = [": ".join(i) for i in inventory]
        inventory = "; ".join(inventory)
        inventory += "; chinese: 5"
    else:
        inventory = "chinese: 5"

    return inventory


def update_user_money_inventory_in_db(money, inventory, key):
    """
    Update the user in the database with their new money and new inventory
    """

    cursor = connect.cursor()
    try:
        cursor.execute(
            f"UPDATE players SET _Money = {money}, _Inventory = '{inventory}', phase1_verify = 1 WHERE _Key = {key}"
        )
    except mariadb.Error as e:
        print(f"Error: {e}")
    cursor.close()


def main():
    global COUNTER

    input("Please press 'ENTER' to begin PHASE 1 refunds")

    # Append to a file - and/or create it if it doesn't exist
    log = open(
        "1_refund_log.txt", "a", encoding="utf-8"
    )

    users, rowcount = get_all_players('_Key, _SteamID, _Inventory, _Money')
    # Loop through all the rows of players
    for user in users:
        key = user[0]
        steamid = user[1]
        inventory = user[2]
        money = user[3]
        new_inventory = []

        if check_user_already_processed_phase1(key):
            continue

        log.write(
            f"ID: {key} \nSteamID: {steamid} \nOriginal Wallet: ${money}\n"
        )

        if user_has_inventory(inventory) is False:
            cursor = connect.cursor()
            try:
                cursor.execute(
                    f"UPDATE players SET _Inventory = 'chinese: 5', phase1_verify = 1 WHERE _Key = {key}"
                )
            except mariadb.Error as e:
                print(f"Error: {e}")
            cursor.close()
            log.write("[!]NO INVENTORY[!]\n\n")
            COUNTER += 1
            print(COUNTER, "of", rowcount, "does not have an Inventory")
            continue

        items = convert_inventory_into_items(inventory)

        pre_value, refund, post_value = refund_user(items, new_inventory)

        inventory = join_new_inventory(new_inventory)

        net_worth = money + pre_value

        log.write(
            f"Wallet (+ Inventory value): ${net_worth}\n"
        )

        money += post_value
        # More log file additions
        log.write(
            f"Wallet - (after {(refund_percentage * 100)}% decrease on inventory value): ${int(money)}\n\n"
        )

        update_user_money_inventory_in_db(money, inventory, key)

        COUNTER += 1
        # Some visual feedback in console
        print(COUNTER, "of", rowcount, "refunded!")

    print("\n[!]PHASE 1 REFUND SUCCESSFULLY EXECUTED[!]")
