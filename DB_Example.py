# Name:                                             Renacin Matadeen
# Date:                                                11/18/2018
# Title                                             Fuelly Database
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import time
import re
import psycopg2
import pprint
import pandas as pd
from selenium import webdriver

# ----------------------------------------------------------------------------------------------------------------------

'''
PURPOSE:
    Using Selenium as a headless webscraper, data will be parsed from fuelly. The scraped data will then be handed off
    to a PostgreSQL database. Once the database has been populated a number of SQL queries will be made.
'''

# ----------------------------------------------------------------------------------------------------------------------


# Connect To Database
def database_connect():
    try:
        connection = psycopg2.connect(
            "dbname='FuellyData' user='postgres' host='localhost' password='password' port='5432' ")
        connection.autocommit = True
        cursor = connection.cursor()
        pprint("Database Connected")

        return connection, cursor

    except psycopg2.DatabaseError:
        pprint("Cannot Connect")


# Query Delete Past Attempts Table
def database_delete(cursor):
    command = "DELETE TABLE IF EXISTS VehicleData"

    cursor.execute(command)
    pprint("Table Deleted")
    cursor.close()
    pprint("Cursor Closed")
    del command


# Query Existence Of Table
def database_create(cursor):
    command = "CREATE TABLE IF NOT EXISTS VehicleData(Manufacturer varchar(15), \
                Make varchar(15), Year INTERGER, AVG_MPG FLOAT, Num_Vehicles INTERGER, Miles INTERGER)"

    cursor.execute(command)
    pprint("Table Created")
    cursor.close()
    pprint("Cursor Closed")
    del command


# Add Data To Database
def database_add(cursor, manu, make, year, mpg, num_veh, miles):
    command = "INSERT INTO VehicleData (Manufacturer, Make, Year, AVG_MPG) \
                Values('" + manu + "','" + make + "','" + year + "','" + mpg + "','" + num_veh + "','" + miles + "')"

    cursor.execute(command)
    pprint("Data Inserted")
    cursor.close()
    pprint("Cursor Closed")
    del command


# Close Connection To Database
def database_close(connection):
    try:
        connection.close()
        pprint("Connection Closed")

    except AttributeError as e:
        pprint(e)
        pprint("Cannot Close Connection")


# ----------------------------------------------------------------------------------------------------------------------


# This Function Will Collect The Websites Associated With Each Entry
def get_links(x):
    # Prepare The Chrome Driver
    path1 = "/Users/renacinmatadeen/Documents/Programming/Python/2018/DriverSelenium/uBlock-Origin_v1.14.8.crx"
    chromedriver = "/Users/renacinmatadeen/Documents/Programming/Python/2018/DriverSelenium/chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(path1)
    chrome = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

    # Initialize The Chrome Driver
    chrome.get(x)

    try:
        # Make Empty Lists
        manufacturer_, name_, website_ = [], [], []

        # Get All Instances Of "Make-Header-Link"
        instances_location = "/html/body/div[1]/div/div[2]/div/div[2]/div/ul"
        entries = chrome.find_elements_by_xpath(instances_location)

        # Iterate Through And Take Make, Model, Then Build The Link
        for listing in entries:
            listing = listing.get_attribute("outerHTML")

            # Use Regex To Parse Info, Data Stored In List
            match = re.findall('<a href="(.*)</a>', listing)

            # Iterate Through List & Parse Information
            for website in match:
                # Car Name
                parse_web = website.split(">")
                car_name = parse_web[1]
                name_.append(car_name)

                # Car Manufacturer
                make_split = parse_web[0].split("/")
                manufacturer_name = make_split[4]
                manufacturer_.append(manufacturer_name)

                # Complete WebLink
                weblink_split = website.split('"')
                weblink = weblink_split[0]
                website_.append(weblink)

        chrome.quit()

        # Add Data To DF, then Return DF
        df = pd.DataFrame()
        df["Manufacturer"] = manufacturer_
        df["Name"] = name_
        df["Website"] = website_

        print("\n{:-^15}".format("Links Parsed"))
        return df

    # If Something Goes Wrong Catch The Error
    except IOError:
        chrome.quit()

    except ValueError:
        chrome.quit()


def parse_data(cursor, df):
    print("\n{:-^15}".format("Data Parsed"))
    # Paths
    path1 = "/Users/renacinmatadeen/Documents/Programming/Python/2018/DriverSelenium/uBlock-Origin_v1.14.8.crx"
    chromedriver = "/Users/renacinmatadeen/Documents/Programming/Python/2018/DriverSelenium/chromedriver"

    # Prepare The Chrome Driver, Headless Wont Be Used As Extensions Cannot Be Used
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(path1)
    chrome = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

    # Get Range Of DF
    df_len = len(df.index)

    # Loop Through Each Row & Visit The Associated Website. Pull Information, Upload To The DB
    for x in range(0, df_len):

        # Search Website
        focus_url = df["Website"][x]
        chrome.get(focus_url)

        # If There Is A Pop Up, Click The Dismiss Button
        button_ = '//*[@id="close_x"]'
        try:
            pop_up_escape = chrome.find_element_by_xpath(button_)
            pop_up_escape.click()

        except Exception:
            pass

        # Get All Instances
        instances_location = "/html/body/div[1]/div/div[2]/section/div"
        entries = chrome.find_elements_by_xpath(instances_location)
        for listing in entries:
            listing = listing.get_attribute("outerHTML")

            # Use Regex To Parse Year, MPG, Num_Vehiclesand Total Miles & Clean When Needed!
            year = re.findall('year"><span>(.*)</span></li>', listing)
            year = list(map(int, year))

            mpg = re.findall('data">(.*)</span> <span class="summary-avg-label">A', listing)
            mpg = list(map(float, mpg))

            num_vehicles = re.findall('-total">(.*) <span>Vehicle', listing)
            num_vehicles = list(map(int, num_vehicles))

            miles = re.findall('miles">(.*) <span>Miles Tracked', listing)
            miles = [value.replace('N/A', '0') for value in miles]
            miles = [value.replace(',', '') for value in miles]
            miles = list(map(int, miles))

            # Add Data To Database
            database_add(cursor, df["Manufacturer"][x], df["Name"]
                         [x], year, mpg, num_vehicles, miles)

        # User Information
        print("{0}: {1} - Complete".format(df["Manufacturer"][x], df["Name"][x]))

        # Quit Current Chrome Driver
        chrome.quit()


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
    database_delete(cur)

    # Parse Data From Links, Append To Database
    parse_data(cur, df)

    # Close Database ConnectionError
    database_close(conn)
