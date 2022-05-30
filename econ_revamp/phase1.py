"""
PHASE 1: Refund all inventory items (except legacy) at 60% market value.
"""
import mariadb
from .items import ITEM_DICT, OMIT_ITEMS
from config import INVENTORY_REFUND_PERCENTAGE as refund_percentage
import math
from . import get_all_players, get_total_money, connect

COUNTER = 0


def user_has_inventory(inventory):
    if inventory == "":
        return False


def convert_inventory_into_items(inventory):
    # Dissect the inventory string into their own objects
    inv = inventory.split("; ")
    # Found some strange entries that had a semi-colon after the value
    # ... even though nothing followed it lol
    inv = [i.replace(";", "") for i in inv]
    items = [i.split(": ", 2) for i in inv]
    print(items)

    return items


def refund_user(items, inventory):
    refund = 0

    for item in items:
        # name = item[0]
        # quantity = item[1]
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
    if len(inventory) >= 1:
        inventory = [": ".join(i) for i in inventory]
        inventory = "; ".join(inventory)
    else:
        inventory = ""

    return inventory


def update_user(money, inventory, key):
    cursor = connect().cursor()
    try:
        cursor.execute(
            f"UPDATE players SET _Money = _Money + {money}, _Inventory = '{inventory}' WHERE _Key = {key}"
        )
    except mariadb.Error as e:
        print(f"Error: {e}")
    cursor.close()


def main():
    global COUNTER

    input("Please press 'ENTER' to begin PHASE 1 refunds")

    # Append to a file - and/or create it if it doesn't exist
    log = open(
        "PHASE_1_refund_log.txt", "a", encoding="utf-8"
    )

    users, rowcount = get_all_players('_Key, _SteamID, _Inventory, _Money')
    # Loop through all the rows of players
    for user in users:
        key = user[0]
        steamid = user[1]
        inventory = user[2]
        money = user[3]
        new_inventory = []

        log.write(
            f"ID: {key} \nSteamID: {steamid} \nOld Wallet: ${money}\n"
        )

        if user_has_inventory(inventory) is False:
            log.write("[!]NO INVENTORY[!]")
            continue

        items = convert_inventory_into_items(inventory)

        pre_value, refund, post_value = refund_user(items, new_inventory)

        inventory = join_new_inventory(new_inventory)

        print(inventory)
        net_worth = money + pre_value

        log.write(
            f"New Wallet (Wallet + Inventory): ${net_worth}\n"
        )

        money += post_value
        # More log file additions
        log.write(
            f"Phase 1 Wallet (After % Decrease on inventory value): ${money}\n\n"
        )

        #update_user(money, inventory, key)

        COUNTER += 1
        # Some visual feedback in console
        print(COUNTER, "of", rowcount, "refunded!")

    REFUND = 0
    COUNTER = 0

    print("\n[!]PHASE 1 REFUND SUCCESSFULLY EXECUTED[!]")
