import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('chained_assignment',None)

# queries the main url
url = 'https://www.congress.gov/resources/display/content/The+Federalist+Papers'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# parses the text information
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

# extracts table information
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

# stores info in dataframe
df = pd.DataFrame(all_rows)
df.columns = ['No.','Title','Author','Publication','Date']
# adds text and text length columns
df.loc[:,'Text'] = all_texts
df = df[['No.','Title','Author','Text']]
df.loc[:,'Length'] = df['Text'].apply(len)

# selects according to author
df_ham = df[df['Author'] == 'Hamilton'].reset_index().drop(['index'], axis=1)
df_mad = df[df['Author'] == 'Madison'].reset_index().drop(['index'], axis=1)
df_jay = df[df['Author'] == 'Jay'].reset_index().drop(['index'], axis=1)

# saves to raw_data directory
df_ham .to_csv('../raw_data/hamilton.csv', index=False)
df_mad .to_csv('../raw_data/madison.csv', index=False)
df_jay .to_csv('../raw_data/jay.csv', index=False)