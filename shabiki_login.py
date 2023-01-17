"""
A module to login in to brave browser and search for links
from the games and save them to txt files for each game.

The links will be found from duckduckgo.com.
"""

# Import some necessary modules
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


load_dotenv()

# Set the credentials
MOBILE_NO = os.getenv("MOBILE_NO")
PASSWORD = os.getenv("PASSWORD")


EXECUTABLE_PATH = "/usr/bin/brave"
CHROME_DRIVER = "/usr/bin/chromedriver"

service = Service(CHROME_DRIVER)

options = webdriver.ChromeOptions()
options.binary_location = EXECUTABLE_PATH

driver = webdriver.Chrome(service=service, options=options)


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
