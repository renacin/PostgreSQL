# Name:                                             Renacin Matadeen
# Date:                                                11/20/2018
# Title                                             Fuelly Database
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import re
import pandas as pd
from selenium import webdriver

from db_functions import database_add

# ----------------------------------------------------------------------------------------------------------------------

'''
PURPOSE:
    These functions will help parse the data from the pertinent website.
'''

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

        # State Sanitized Name & Make
        manu = df["Manufacturer"][x]
        name = df["Name"][x]
        manu = manu.replace("'", "")
        name = name.replace("'", "")

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

            mpg = re.findall('data">(.*)</span> <span class="summary-avg-label">A', listing)
            mpg = list(map(float, mpg))

            num_vehicles = re.findall('-total">(.*) <span>Vehicle', listing)

            miles = re.findall('miles">(.*) <span>Miles Tracked', listing)
            miles = [value.replace('N/A', '0') for value in miles]
            miles = [value.replace(',', '') for value in miles]

            # Add Data To Database
            for y in range(0, len(year)):
                database_add(cursor, manu, name, year[y], mpg[y], num_vehicles[y], miles[y])

        # User Information
        print("{0}: {1} - Complete".format(df["Manufacturer"][x], df["Name"][x]))

    # Quit Current Chrome Driver
    chrome.quit()

# ----------------------------------------------------------------------------------------------------------------------
