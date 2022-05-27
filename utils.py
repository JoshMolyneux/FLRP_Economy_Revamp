import mariadb
from config import config


def sql_read(query, params=None):
    try:
        connect = mariadb.connect(**config)
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
            **config,
            autocommit=True
        )
        cursor = connect.cursor()
        cursor.execute(query, params)
        cursor.close()
        connect.close()

    except mariadb.Error as e:
        print(f"Error: {e}")
