import sys
sys.path.append("..")
import mariadb
from config import test_db_details


def sql_read(query, params=None):
    try:
        connect = mariadb.connect(**test_db_details)
        cursor = connect.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()
        connect.close()

        content = []

        for row in results:
            content.append(row)

        return content

    except mariadb.Error as e:
        print(f"Error: {e}")


def sql_write(query, params=None):
    try:
        connect = mariadb.connect(
            **test_db_details,
            autocommit=True
        )
        cursor = connect.cursor()
        cursor.execute(query, params)
        cursor.close()
        connect.close()

    except mariadb.Error as e:
        print(f"Error: {e}")
