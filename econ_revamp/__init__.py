import mariadb
import sys
sys.path.append("..")
from config import db_details, test_db_details


def connect(test=False):
    if test is False:
        try:
            connect = mariadb.connect(
                **db_details,
                autocommit=True
            )
        except mariadb.Error as e:
            print(f"There was an error connecting to MariaDB: {e}")
            sys.exit(1)
    else:
        try:
            connect = mariadb.connect(
                **test_db_details,
                autocommit=True
            )
        except mariadb.Error as e:
            print(f"There was an error connecting to MariaDB: {e}")
            sys.exit(1)

    return connect


def get_all_players(params, test=False):
    cursor = connect(test).cursor()

    try:
        cursor.execute(
            f"SELECT {params} FROM players")
        # Store all the results in a variable
        result = cursor.fetchall()
        rowcount = cursor.rowcount
    except mariadb.Error as e:
        print(f"Error getting all players: {e}")
    cursor.close()

    return result, rowcount


def get_total_money():
    cursor = connect().cursor()
    try:
        cursor.execute("SELECT SUM(_Money) FROM players")
        # Store all the results in a variable
        total = cursor.fetchone()
    except mariadb.Error as e:
        print(f"Error getting SUM value: {e}")
    cursor.close()

    return total


def set_inv_value_to_zero():
    # Set all Inventory values to ZERO
    cursor = connect().cursor()
    try:
        cursor.execute("UPDATE players SET _Invvalue = 0")
    except mariadb.error as e:
        print(f"Error setting inv values to zero: {e}")
    cursor.close()
