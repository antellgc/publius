import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# reading docs into dataframes (to update to SQLite)
df_test_docs = pd.read_csv("./processed_data/test_docs.csv")
df_fed_para = pd.read_csv("./processed_data/fed_paragraphs.csv")

# selecting a paper (#71 as an example)
no = 71
title_name = list(df_test_docs[df_test_docs['No.'] == no]['Title'])[0]
paper_text = "No. " + str(no) + ' -- ' + str(title_name)
# select paragaphs
paragraph_selection = df_fed_para[df_fed_para['No.'] == no]
p_list = list(paragraph_selection['ParaText'])
t = "\\".join(p_list)


#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="What's your name, man?"),
    html.H3(children="Uncovering the authorship of the anonymously-written \
        Federalist Papers with machine learning"),
    html.Div(paper_text),
    html.Blockquote(t),
    dcc.Markdown(t)
])

if __name__ == '__main__':
    app.run_server(debug=True)