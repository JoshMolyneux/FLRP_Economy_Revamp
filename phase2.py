"""
PHASE 2: Decrease wallets using a tax bracket system as follows when the player has:
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
"""
import mariadb

NON_TAXABLE_LIMIT = 199999
TAX = [0.5, 0.45, 0.4, 0.35, 0.3]
LIMIT = [499999, 749999, 999999, 499999]


def phase2(connect):
    input("Please press 'ENTER' to begin PHASE 2 tax deductions")

    cursor = connect.cursor()
    try:
        cursor.execute("SELECT _Key, _SteamID, _Money FROM players")
        # Store all the results in a variable
        result = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error: {e}")
    ROW_COUNT = cursor.rowcount
    COUNTER = 0
    cursor.close()

    log_file_tax_bracket = open(
        "PHASE_2_tax_log.txt", "a", encoding="utf-8"
    )

    for row in result:
        key = row[0]
        steamid = row[1]
        money = row[2]
        pool = 0

        log_file_tax_bracket.write(
            f"ID: {key} \nSteamID: {steamid} \nPhase 1 Wallet: ${money}\n"
        )

        if money <= NON_TAXABLE_LIMIT:
            log_file_tax_bracket.write(
                "[!]NOT ENOUGH TO BE TAXED[!]\n\n"
            )
            continue
        elif money <= LIMIT[0]:
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

        money -= pool

        log_file_tax_bracket.write(
            f"Money Removed: ${money}\nPhase 2 Wallet: ${float(pool)}\n\n"
        )

        cursor = connect.cursor()
        try:
            cursor.execute(
                f"UPDATE players SET _Money = {float(pool)} WHERE _Key = {key}"
            )
        except mariadb.Error as e:
            print(f"Error: {e}")
        cursor.close()
        COUNTER += 1
        # Some visual feedback in console
        print(COUNTER, "of", ROW_COUNT, "taxed!")

    print("\n[!]PHASE 2 TAX DEDUCTION SUCCESSFULLY EXECUTED[!]")
