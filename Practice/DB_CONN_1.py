# Name:                                             Renacin Matadeen
# Date:                                               11/18/2018
# Title                                          PostgresSQL & Python
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import psycopg2
from pprint import pprint

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

'''

# ----------------------------------------------------------------------------------------------------------------------


class DatabaseConnection:
    # Initialize the connection with the database
    # All functions, and methods will be stored within a class, this will make things easier down the line
    # Within the initial __init__ method, we will connect to the database, and create a cursor
    # Note when we call the DatabaseConnection() the init method is implicitly run

    # Connect To Database
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='NationalWeather' user='postgres' host='localhost' password='password' port='5432' ")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except psycopg2.DatabaseError:
            pprint("Cannot Connect...")

    # Create A Table Within The Database
    def create_table(self):
        create_table_command = "CREATE TABLE IF NOT EXISTS Weather_Date(Location varchar(20), Weather varchar(10))"
        self.cursor.execute(create_table_command)

# ----------------------------------------------------------------------------------------------------------------------


# Main entry point
if __name__ == '__main__':

    # Connect To The Database
    database_connection = DatabaseConnection()

    # Add Tables If Not Present
    database_connection.create_table()
