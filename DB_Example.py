# Name:                                             Renacin Matadeen
# Date:                                                11/18/2018
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

# ----------------------------------------------------------------------------------------------------------------------

'''
PURPOSE:
    Using Selenium as a headless webscraper, data will be parsed from fuelly. The scraped data will then be handed off
    to a PostgreSQL database. Once the database has been populated a number of SQL queries will be made.
'''

# ----------------------------------------------------------------------------------------------------------------------


# //TODO: CAN THIS BE SIMPLIFIED?
# This Function Will Collect The Websites Associated With Each Entry
def get_data(x):

    # Prepare The Chrome Driver
    chromedriver = "/Users/renacinmatadeen/Documents/Programming/Python/2018/DriverSelenium/chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
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

        return df

    # If Something Goes Wrong Catch The Error
    except IOError:
        chrome.quit()

    except ValueError:
        chrome.quit()


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Main Program
    target_url = "http://www.fuelly.com/car"
    df = get_data(target_url)
    print(df.head())
