"""
PHASE 2: Decrease wallets using a tax bracket system as follows when the player has:
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease

    and

    Process descale by fixed DESCALE_VALUE
"""
import mariadb
import sys
from . import get_all_players
from config import db_details, DESCALE_VALUE

COUNTER = 0

NON_TAXABLE_LIMIT = 199999
TAX = [0.5, 0.45, 0.4, 0.35, 0.3]
LIMIT = [499999, 749999, 999999, 4999999]

# Connect to our MariaDB database
try:
    connect = mariadb.connect(
        **db_details,
        autocommit=True
    )
except mariadb.Error as e:
    print(f"There was an error connecting to MariaDB: {e}")
    sys.exit(1)


def check_user_already_processed_phase2(key):
    """
    A function to check if a user has already been processed through Phase 2.
    We can return a boolean value and use it as a condition when processing a user.
    """

    cursor = connect.cursor()
    try:
        cursor.execute(
            f"SELECT phase2_verify FROM players WHERE _Key = {key}"
        )
        result = cursor.fetchone()
        if result[0] == 1:
            return True
    except mariadb.Error as e:
        print(f"Error: {e}")
    cursor.close()


def money_is_non_taxable(money):
    if money <= NON_TAXABLE_LIMIT:
        return True


def process_tax(money):
    """
    A function to process a tax bracket decrease on a user's entire money value.
    Variable tax is dependant on the amount of money a user has. The NON_TAXABLE_LIMIT
    value is safe and won't be affected.
    """
    pool = 0

    if money <= LIMIT[0]:
        pool = (TAX[0] * (money - NON_TAXABLE_LIMIT))
    elif money <= LIMIT[1]:
        pool = (TAX[0] * (LIMIT[0] - NON_TAXABLE_LIMIT)) + \
               (TAX[1] * (money - LIMIT[0]))
    elif money <= LIMIT[2]:
        pool = (TAX[0] * (LIMIT[0] - NON_TAXABLE_LIMIT)) + \
               (TAX[1] * (LIMIT[1] - LIMIT[0])) + \
               (TAX[2] * (money - LIMIT[1]))
    elif money <= LIMIT[3]:
        pool = (TAX[0] * (LIMIT[0] - NON_TAXABLE_LIMIT)) + \
               (TAX[1] * (LIMIT[1] - LIMIT[0])) + \
               (TAX[2] * (LIMIT[2] - LIMIT[1])) + \
               (TAX[3] * (money - LIMIT[2]))
    else:
        pool = (TAX[0] * (LIMIT[0] - NON_TAXABLE_LIMIT)) + \
               (TAX[1] * (LIMIT[1] - LIMIT[0])) + \
               (TAX[2] * (LIMIT[2] - LIMIT[1])) + \
               (TAX[3] * (LIMIT[3] - LIMIT[2])) + \
               (TAX[4] * (money - LIMIT[3]))

    pool /= DESCALE_VALUE
    pool += NON_TAXABLE_LIMIT

    return pool


def update_user_money_in_db(money, key):
    """Update the user in the database with their new money."""

    cursor = connect.cursor()
    try:
        cursor.execute(
            f"UPDATE players SET _Money = {money}, phase2_verify = 1 WHERE _Key = {key}"
        )
    except mariadb.Error as e:
        print(f"Error: {e}")
    cursor.close()


def main():
    global COUNTER

    input("Please press 'ENTER' to begin PHASE 2 tax deductions AND descale")

    log = open(
        "2_decrease_descale_log.txt", "a", encoding="utf-8"
    )

    users, rowcount = get_all_players('_Key, _SteamID, _Money')

    for user in users:
        key = user[0]
        steamid = user[1]
        money = user[2]

        if check_user_already_processed_phase2(key):
            continue

        log.write(
            f"ID: {key} \nSteamID: {steamid} \nWallet (before tax and descale): ${money}\n"
        )

        if money_is_non_taxable(money):
            log.write(
                f"[!]NOT ENOUGH TO BE TAXED OR DESCALED[!] \nFinal Wallet (after Refund, Descale): ${int(money)}\n\n"
            )
            COUNTER += 1
            print(COUNTER, "of", rowcount, "descaled only!")
            continue

        pool = process_tax(money)

        money_removed = money - pool

        log.write(
            f"Money Removed: ${money_removed}\nWallet (after tax): ${pool}\n"
        )

        #  money = pool / DESCALE_VALUE

        log.write(
            f"Final Wallet (after Refund, Decrease, Descale): ${int(money)}\n\n"
        )

        update_user_money_in_db(int(pool), key)

        COUNTER += 1

        # Some visual feedback in console
        print(COUNTER, "of", rowcount, "taxed AND descaled!")

    print("\n[!]PHASE 2 TAX DEDUCTION SUCCESSFULLY EXECUTED[!]")
