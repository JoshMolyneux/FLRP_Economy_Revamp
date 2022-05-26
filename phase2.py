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


def phase2(connect):
    input("Please press 'ENTER' to begin PHASE 2 tax deductions")

    cursor = connect.cursor()
    try:
        cursor.execute("SELECT _Key, _SteamID, _Money FROM players")
        # Store all the results in a variable
        result = cursor.fetchall()
    except mariadb.error as e:
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
        tax = 0
        pool = 0

        log_file_tax_bracket.write(
            f"ID: {key} \nSteamID: {steamid} \nPhase 1 Wallet: ${money}\n"
        )

        if money <= 199999:
            log_file_tax_bracket.write(
                "[!]NOT ENOUGH TO BE TAXED[!]\n\n"
            )
            continue
        elif money <= 499999:
            tax = 0.5   # 50%
            pool = (money - 199999) * tax
        elif money <= 749999:
            tax = 0.45  # 55%
            pool = (money - 499999) * tax
        elif money <= 999999:
            tax = 0.4  # 60%
            pool = (money - 749999) * tax
        elif money <= 1000000:
            tax = 0.35  # 65%
            pool = (money - 999999) * tax
        else:
            tax = 0.3  # 70%
            pool = (money - 1000000) * tax

        money = money - pool
        log_file_tax_bracket.write(
            f"Money Removed: ${money}\nPhase 2 Wallet: ${int(pool)}\n\n"
        )

        cursor = connect.cursor()
        try:
            cursor.execute(
                f"UPDATE players SET _Money = {int(pool)} WHERE _Key = {key}"
            )
        except mariadb.Error as e:
            print(f"Error: {e}")
        cursor.close()
        COUNTER += 1

        # Some visual feedback in console
        print(COUNTER, "of", ROW_COUNT, "taxed!")

    print("\n[!]PHASE 2 TAX DEDUCTION SUCCESSFULLY EXECUTED[!]")
