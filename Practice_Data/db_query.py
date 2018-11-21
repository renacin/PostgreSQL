# Name:                                             Renacin Matadeen
# Date:                                                11/21/2018
# Title                                             Fuelly Database
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import psycopg2

# ----------------------------------------------------------------------------------------------------------------------

'''
PURPOSE:
    These functions will help query the database.
'''

# ----------------------------------------------------------------------------------------------------------------------


# Connect To Database
def database_connect():
    try:
        conn = psycopg2.connect(
            "dbname='FuellyData' user='postgres' host='localhost' password='password' port='5432'")
        conn.autocommit = True
        cursor = conn.cursor()
        print("Database Connected")
        return conn, cursor

    except psycopg2.DatabaseError:
        print("Cannot Connect")


# Query Existence Of Table
def database_query(cursor):
    command = (
        """
        SELECT * FROM vehicledata

        WHERE vehicledata.miles > 5000
        AND make NOT IN ('PCX125')
        AND num_vehicles > 50

        ORDER BY avg_mpg DESC
        LIMIT 20;
        """
    )

    cursor.execute(command)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    del command


def close_cursor(cursor):
    cursor.close()


# Close Connection To Database
def database_close(connection):
    try:
        connection.close()
        print("Connection Closed")

    except AttributeError as e:
        print(e)
        print("Cannot Close Connection")


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Connect To Database
    conn, cur = database_connect()

    # Try To Query Data
    try:
        database_query(cur)
        close_cursor(cur)
        database_close(conn)

    except Exception as e:
        print(e)
        close_cursor(cur)
        database_close(conn)
