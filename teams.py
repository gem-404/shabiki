#!/usr/bin/python3.10
"""
A module created to get teams on which I should
place my bets.
"""

import datetime

import pandas as pd
from bs4 import BeautifulSoup
from typing import List
from typing import Union


website0: str = "https://winonbetonline.com"
website1: List[Union[str, int]] = ["https://www.betensured.com", 1869, 2108]
website2: List[Union[str, int]] = ["https://betnumbers.gr/free-betting-tips",
                                   267, 431]


def check_time_before_one():
    """
    Games from website0 comes from 1:00pm in the afternoon...
    Therefore, if the time is not yet 1:00pm, then we should
    not bother getting any data from website0.
    """
    now = datetime.datetime.now()
    if now.hour < 13:
        return True
    return False


csv_filename: str = f'{datetime.datetime.now().strftime("%Y-%m-%d")}_teams.csv'


def perf_bash_ops(website_lst: List[Union[str, int]]) -> None:
    """Perform bash operations to get table data from the website"""
    import subprocess

    website: Union[str, int] = website_lst[0]
    start: Union[str, int] = website_lst[1]
    end: Union[str, int] = website_lst[2]

    bash_query: str = f"curl -s {website} -o main.html"
    new_query: str = f"sed -n '{start},{end}p' main.html > tmpfile"
    mv_query: str = "mv tmpfile main.html"

    subprocess.call(bash_query, shell=True)
    subprocess.call(new_query, shell=True)
    subprocess.call(mv_query, shell=True)


# Read the contents of file
def read_html_contents(file) -> str:
    """Read the contents of main.html"""
    with open(file, 'r') as f:
        html_table = f.read()
    return html_table


def data_cleaner(data: list[list[str]]) -> list[list[str]]:

    # Take data up to the first seven items
    data = data[:7]

    # Clean up the data
    for i in range(len(data)):
        first_word = data[i][0].split('\n\n\n')
        data[i][0] = first_word[1].strip()
        data[i].insert(0, first_word[0])

    return data


# get contents of first website -> website0
def get_website0_data(website) -> pd.DataFrame:
    """Get data from the first website by reading
    the table contents of the html file"""

    teams_table = pd.read_html(website)
    df = teams_table[0]
    df.to_csv(csv_filename, index=False)

    return df


def lst_splitter(lst: list[list[str]]) -> list[list[str]]:

    new_list = [[item.split()[0], item.split()[1]] + sub_list + ['']
                for sub_list in lst for item in sub_list[3:4]]

    return new_list


# Get data from the second website -> website1
def get_website1_data(html_table) -> pd.DataFrame:

    # parse the html code using beautifulsoup
    soup = BeautifulSoup(html_table, 'html.parser')

    # find the table element and extract its contents
    table = soup.find('table')
    rows = table.find_all('tr')

    # extract the table data
    data = []
    for row in rows[1:]:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    if len(data) == 10:
        data = data_cleaner(data=data)

    new_df = pd.DataFrame(data)

    return new_df


def main():
    """Main function"""

    file: str = 'main.html'

    perf_bash_ops(website1)
    html_table = read_html_contents(file)

    new_df = get_website1_data(html_table=html_table)

    perf_bash_ops(website2)
    html_table_one = read_html_contents(file)

    newer_df = get_website1_data(html_table=html_table_one)

    df: pd.DataFrame = pd.DataFrame()

    if not check_time_before_one():
        df = get_website0_data(website0)

    # Remove the last two columns  from newer_df
    newer_df = newer_df.drop(columns=newer_df.columns[-3:])
    # Remove the first column from newer_df
    newer_df = newer_df.drop(newer_df.columns[0], axis=1)

    # Split the last column into two and drop the last column
    newer_df[[4, 5]] = newer_df[3].str.split(' ', 1, expand=True)
    newer_df = newer_df.drop(newer_df.columns[-1], axis=1)
    newer_df = newer_df.drop(newer_df.columns[-2], axis=1)

    # Rename the columns
    newer_df.columns = [0, 1, 2]

    # Reset newer_df header columns to 0, 1, 2
    newer_df.columns = [0, 1, 2]
    merged_df = pd.concat([df, new_df, newer_df], ignore_index=True)

    # Remove the last two columns from merged_df
    merged_df = merged_df.iloc[:, :-2]

    print(merged_df.head(40))


if __name__ == "__main__":
    main()
