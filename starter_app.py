import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# reading docs into dataframes (to update to SQLite)
df_test_docs = pd.read_csv("./processed_data/test_docs.csv")
df_fed_para = pd.read_csv("./processed_data/fed_paragraphs.csv")

# creating indicators for drop down menu
df_test_docs['Indicator Name'] = "No. " + df_test_docs['No.'].map(str) + " - " + df_test_docs['Title']
available_indicators = df_test_docs['Indicator Name'].unique()

### app

app = dash.Dash(__name__,
    static_folder='static',
    external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children="What's your name, man?",
        style = {'font-size':'4em'}),

    html.Img(src="static/constitution.png",
        style = {'max-width':600}),

    html.H3(children="Uncovering the authorship of the anonymously-written \
        Federalist Papers with machine learning"),

    dcc.Dropdown(
        id='dropdown-id',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value='initial value',
        clearable=False,
        placeholder="Select a Federalist Paper"
        ),

    html.H1(id='image-output-id'),

    html.H1(id='model-output-id'),

    html.Blockquote(id='paragraph-output-id', style = {'textAlign':'left'})], 
    style={'textAlign': 'center'})

##### outputs

### IMAGE OUTPUT
@app.callback(
    Output(component_id='image-output-id', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_author_output(value):
    if value in list(df_test_docs['Indicator Name']):
        mask1 = df_test_docs['Indicator Name'] == value
        author = list(df_test_docs[mask1]['Author'])[0].lower()
        return author
    else:
        return None

### MODEL PREDICTION
@app.callback(
    Output(component_id='model-output-id', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_model_output(value):
    if value in list(df_test_docs['Indicator Name']):
        return value
    else:
        return None

#### PARAGRAPH TEXT
@app.callback(
    Output(component_id='paragraph-output-id', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_text_output(value):
    if value in list(df_test_docs['Indicator Name']):
        mask1 = df_test_docs['Indicator Name'] == value
        title = list(df_test_docs[mask1]['Title'])[0]
        mask2 = df_fed_para['Title'] == title
        p_list = list(df_fed_para[mask2]['ParaText'])
        return [html.P(paragraph) for paragraph in p_list]
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
