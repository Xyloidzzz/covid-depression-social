import sqlite3
from sqlite3 import Error

path = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok.sql"
schema = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok-schema.sql"


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# function to create .db file from tiktok.sql using sqlite3
def create_table(connection, create_table_sql):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(f"The error '{e}' occurred")

  # main
if __name__ == '__main__':
    conn = create_connection(path)
    # in table video look through videoDesc column and count how many times #depression appears in that value
    # then print the number of times #depression appears
    conn.execute(
        "SELECT COUNT(*) FROM video WHERE videoDesc LIKE '%#depression%'")
    result = conn.fetchall()
    print(result)
    conn.close()
    print("Done")
