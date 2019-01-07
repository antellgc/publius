import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('chained_assignment',None)

# global variables
url = "https://www.congress.gov/resources/display/content/The+Federalist+Papers"
author_names = ['Madison','Hamilton','Jay','Hamilton and Madison','Hamilton or Madison']
raw_data_path = "../raw_data/"

def get_soup_from_url(url):
    """
    Query a given url and return the page content as BeautifulSoup object.
    Parameters:
        url: the url to be scraped
    Returns:
        soup: a BeautifulSoup object
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def parse_federalist_text(soup):
    """
    Extract the text information based on known structure of Federalist papers.
    Parameters:
        soup: a BeautifulSoup object
    Returns:
        all_texts: a list of the scraped texts
    """
    text_block = soup.find_all("div", class_="wiki-content")[0].get_text()
    all_texts = []
    n = 1
    for string in text_block.split('|| Federalist No.')[1:]:
        string = string.replace(u'\xa0', u' ')
        string = '|| Federalist No.' + string
        string = string.split('To the People of the State of New York:')[1]
        string = string.split('↑ Back to Top')[0]
        string = string.split('PUBLIUS')[0]
        all_texts.append(string)
        n += 1
    return all_texts

def extract_federalist_table(soup):
    """
    Extract table information and return as list object.
    Parameters:
        soup: a BeautifulSoup object
    Returns:
        all_rows: a list of lists containing table information
    """
    count = 0
    row = []
    all_rows = []
    for i in soup.find_all("td", class_="confluenceTd"):
        count += 1
        if count%5 != 0:
            row.append(i.get_text())
        else:
            row.append(i.get_text())
            all_rows.append(row)
            row = []
    return all_rows

def federalist_data_to_dataframe(all_rows, all_texts):
    """
    Store table data and text data into a single pandas dataframe.
    Parameters:
        all_rows: a list of lists containing table information
        all_texts: a list of the scraped texts
    Returns:
        federalist_dataframe: a pandas dataframe combining the two data sources
    """
    federalist_dataframe = pd.DataFrame(all_rows)
    federalist_dataframe.columns = ['No.','Title','Author','Publication','Date']
    federalist_dataframe.loc[:,'Text'] = all_texts
    federalist_dataframe.loc[:,'Length'] = federalist_dataframe['Text'].apply(len)
    return federalist_dataframe

def select_papers_by_author(federalist_dataframe, author_name):
    """Provide name and return dataframe containing only this author."""
    author_dataframe = federalist_dataframe[federalist_dataframe['Author'] == author_name].reset_index().drop(['index'], axis=1)
    return author_dataframe

def save_to_path(author_dataframe, filename, raw_data_path):
    """Provide dataframe and save to filename"""
    save_path = raw_data_path + filename + ".csv"
    author_dataframe.to_csv(save_path, index=False)

def main(url, author_names, raw_data_path):
    soup = get_soup_from_url(url)
    all_texts = parse_federalist_text(soup)
    all_rows = extract_federalist_table(soup)
    federalist_dataframe = federalist_data_to_dataframe(all_rows, all_texts)
    # iterates through the authors of interest
    for author_name in author_names:
        author_dataframe = select_papers_by_author(federalist_dataframe, author_name)
        print(author_name, author_dataframe.shape)
        save_to_path(author_dataframe, author_name, raw_data_path)
    print("Compelete")

main(url, author_names, raw_data_path)

# selects according to author
#df_ham = df[df['Author'] == 'Hamilton'].reset_index().drop(['index'], axis=1)
#df_mad = df[df['Author'] == 'Madison'].reset_index().drop(['index'], axis=1)
#df_jay = df[df['Author'] == 'Jay'].reset_index().drop(['index'], axis=1)

# saves to raw_data directory
#df_ham.to_csv('../raw_data/hamilton.csv', index=False)
#df_mad.to_csv('../raw_data/madison.csv', index=False)
#df_jay.to_csv('../raw_data/jay.csv', index=False)