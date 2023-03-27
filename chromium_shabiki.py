"""
A module to login in to Chromium browser and search for links
from the games and save them to txt files for each game.

The links will be found from duckduckgo.com.
"""

# Import some necessary modules
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


load_dotenv()

# Set the credentials
MOBILE_NO = os.getenv("MOBILE_NO")
PASSWORD = os.getenv("PASSWORD")


EXECUTABLE_PATH = "/usr/bin/chromium"
# Update with the path to Chromium browser

CHROME_DRIVER = "/usr/bin/chromedriver"
# Update with the path to Chrome driver

options = webdriver.ChromeOptions()
options.binary_location = EXECUTABLE_PATH

driver = webdriver.Chrome(CHROME_DRIVER, options=options)


def main():
    """
    Main function to login and search for links
    """

    driver.get("https://www.shabiki.com/Login")

    driver.find_element(By.ID, "userMobile").send_keys(MOBILE_NO)

    driver.find_element(By.ID, "userPass").send_keys(PASSWORD)

    # Login
    driver.find_element(By.ID, "disableLoginButtonClick").send_keys(Keys.ENTER)

    driver.find_elements(By.CLASS_NAME, "SB-jackpot")[0].click()


if __name__ == "__main__":
    main()
