# Name:                                             Renacin Matadeen
# Date:                                                11/20/2018
# Title                                             Fuelly Database
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

from parse_functions import get_links, parse_data
from db_functions import database_connect, database_delete, database_create, close_cursor, database_close

# ----------------------------------------------------------------------------------------------------------------------

'''
PURPOSE:
    Using Selenium as a headless webscraper, data will be parsed from fuelly. The scraped data will then be handed off
    to a PostgreSQL database. Once the database has been populated a number of SQL queries will be made.
'''

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Get Links
    target_url = "http://www.fuelly.com/car"
    df = get_links(target_url)

    # Connect To Database
    conn, cur = database_connect()

    # Delete Past Database
    database_delete(cur)

    # Create Database
    database_create(cur)

    # Parse Data From Links, Append To Database
    parse_data(cur, df)

    # Close The Cursor
    close_cursor(cur)

    # Close Database ConnectionError
    database_close(conn)

# ----------------------------------------------------------------------------------------------------------------------
