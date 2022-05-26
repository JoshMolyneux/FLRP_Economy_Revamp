"""
PHASE 3: Descale wallets by a fixed number. ez pz
"""
import mariadb


def phase3(connect, DESCALE_VALUE):
    input("Please press 'ENTER' to begin PHASE 3 descale")

    cursor = connect.cursor()
    try:
        cursor.execute("SELECT _Key, _SteamID, _Money FROM players")
        # Store all the results in a variable
        result = cursor.fetchall()
    except mariadb.error as e:
        print(f"Error: {e}")
    ROW_COUNT = cursor.rowcount
    cursor.close()

    COUNTER = 0

    log_file_descale = open(
        "PHASE_3_descale_log.txt", "a", encoding="utf-8"
    )

    for row in result:
        key = row[0]
        steamid = row[1]
        money = row[2]

        log_file_descale.write(
            f"ID: {key} \nSteamID: {steamid} \nPhase 2 Wallet: ${money}\n"
        )

        money = money / DESCALE_VALUE

        log_file_descale.write(
            f"Phase 3 Wallet: ${int(money)}\n\n"
        )

        cursor = connect.cursor()
        try:
            cursor.execute(
                f"UPDATE players SET _Money = {int(money)} WHERE _Key = {key}"
            )
        except mariadb.Error as e:
            print(f"Error: {e}")
        cursor.close()
        COUNTER += 1

        # Some visual feedback in console
        print(COUNTER, "of", ROW_COUNT, "descaled")

    print("\n[!]PHASE 3 DESCALE SUCCESSFULLY EXECUTED[!]")
