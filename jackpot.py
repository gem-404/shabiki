"""
A module to login in to brave browser and search for links
from the games and save them to txt files for each game.

The links will be found from duckduckgo.com.
"""

import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def games_to_be_played(jp_file: str) -> list:
    """
    Function to get games from file and return a list
    """

    with open(jp_file, "r") as file:
        games = file.read().splitlines()

    return games


def create_filename(game: str):
    """
    Function to create a filename for each game
    """
    filename = game + ".txt"
    return filename


def write_links_to_file(filename: str, links: list):
    """
    Function to write links to file
    """
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")

    return None


def search_links(games: list):
    """
    Function to search for links
    """
    links: list = games

    for game in games:
        links.append(game)

    return links


# Run a file cleaner on all txt files
def file_cleaner():
    """
    Function to clean all txt files
    """
    os.system("sh ./cut_duck_sites.sh")


executable_path = "/usr/bin/brave"
chrome_driver = "/usr/bin/chromedriver"

service = Service(chrome_driver)

options = webdriver.ChromeOptions()
options.binary_location = executable_path

driver = webdriver.Chrome(service=service, options=options)


def main():
    """
    Main function to login and search for links
    """
    driver.get("https://www.duckduckgo.com")

    driver.find_element(By.ID, "q").click()

    driver.find_element(By.ID, "login").send_keys(Keys.ENTER)

    # Instantiate the jackpot file.
    jackpot_file = "new_jackpot.txt"

    # Collect the games to be played.
    games = games_to_be_played(jackpot_file)

    for game in games:
        # Create a filename for each game.
        filename = create_filename(game)

        # Search for links.
        links = search_links(game)

        # Write links to file.
        write_links_to_file(filename, links)


if __name__ == "__main__":
    main()
