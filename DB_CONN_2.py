# Name:                                             Renacin Matadeen
# Date:                                               11/19/2018
# Title                                          PostgresSQL & Python
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import psycopg2
from pprint import pprint
import time

# ----------------------------------------------------------------------------------------------------------------------

'''

PURPOSE:
    In this attempt, PostgresSQL will be used, in conjunction with Python, as a storage method for
data. PostgresSQL will be used opposed to SQLite or other similar Databases, as it will allow for multiple concurrent
connections, while allowing for continuous data collection

NOTES:
    - To create a table with fields, use the CREATE TABLE NAME(Field TYPE, ...) query
    - To if you dont know if a table exist, but want one to be present, use the IF NOT EXISTS query
    - To drop a table, use the DROP TABLE query. Note that this can be paired with the IF statement as well
        EX, DROP TABLE IF EXISTS TABLENAME
    - Remember you don't have to commit if autocommit is on!
    - For beginners it's easier to define a single function that will connect, add, and close to a DB
    - However for more advanced users classes can be used for more pythonic programming

'''

# ----------------------------------------------------------------------------------------------------------------------


# Connect To Database
def database_connect():
    try:
        connection = psycopg2.connect(
            "dbname='NationalWeather' user='postgres' host='localhost' password='password' port='5432' ")
        connection.autocommit = True
        cursor = connection.cursor()
        pprint("Database Connected")

        return connection, cursor

    except psycopg2.DatabaseError:
        pprint("Cannot Connect...")


# Query Database
def database_query(cursor):
    create_table_command = "CREATE TABLE IF NOT EXISTS Weather_Date(Location varchar(20), Weather varchar(10))"
    cursor.execute(create_table_command)
    time.sleep(20)
    pprint("Cursor Executed")
    cursor.close()
    pprint("Cursor Closed")


# Close Connection To Database
def database_close(connection):
    try:
        connection.close()
        pprint("Connection Closed")

    except AttributeError as e:
        pprint(e)
        pprint("Cannot Close Connection")

# ----------------------------------------------------------------------------------------------------------------------


# Main Entry Point
if __name__ == '__main__':
    # Connect To Database
    conn, cur = database_connect()

    # Query Database
    database_query(cur)

    # Close Database ConnectionError
    database_close(conn)
