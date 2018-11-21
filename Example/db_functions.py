# Name:                                             Renacin Matadeen
# Date:                                                11/20/2018
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
    These functions will help connect, manipulate, and close the database.
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


# Query Delete Past Attempts Table
def database_delete(cursor):
    command = "DROP TABLE IF EXISTS VehicleData"
    cursor.execute(command)
    print("Table Deleted")
    del command


# Query Existence Of Table
def database_create(cursor):
    command = "CREATE TABLE IF NOT EXISTS VehicleData(Manufacturer varchar(30), \
                Make varchar(30), Year INTEGER, AVG_MPG FLOAT, Num_Vehicles INTEGER, Miles INTEGER)"

    cursor.execute(command)
    print("Table Created")
    del command


# Add Data To Database
def database_add(cursor, manu, make, year, mpg, num_veh, miles):
    command = "INSERT INTO VehicleData (Manufacturer, Make, Year, AVG_MPG, Num_Vehicles, Miles) \
                Values('" + manu + "','" + make + "','" + year + "','" + mpg + "','" + num_veh + "','" + miles + "')"

    cursor.execute(command)
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
