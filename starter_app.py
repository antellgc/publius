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

### APP LAYOUT
app = dash.Dash(__name__,
    static_folder='static',
    external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children="What's your name, man?",
        style = {'font-size':'4em'}),

    html.H3(children="Uncovering the authorship of the anonymously-written \
        Federalist Papers with machine learning"),

    dcc.Dropdown(
        id='dropdown-id',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value='initial value',
        clearable=False,
        placeholder="Select a Federalist Paper"
        ),

    html.Br(),

    html.Img(id="placeholder-image-id", style={'max-width':600}),

    html.Div([
        html.Div([
            html.H2(id='true-author-name'),
            html.Img(id='true-image-id', style={'max-width':600})
        ], style={'width': '49%', 'display': 'inline-block'}),
    
        html.Div([
            html.H2(id='predicted-author-name'),
            html.Img(id='predicted-image-id', style={'max-width':600})
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),

    html.H1(id='model-output-id'),

    html.Blockquote(
        id ='paragraph-output-id',
        style = {'textAlign':'left'}
        )
    ], 
    style = {'textAlign': 'center'})

##### APP OUTPUTS/CALLBACKS

#PLACEHOLDER IMAGE
@app.callback(
    Output(component_id='placeholder-image-id', component_property='src'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_image(value):
    if value in list(df_test_docs['Indicator Name']):
        return None
    else:
        src_name = "static/constitution.png"
        return src_name

#TRUE AUTHOR NAME
@app.callback(
    Output(component_id='true-author-name', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_name(value):
    if value in list(df_test_docs['Indicator Name']):
        mask1 = df_test_docs['Indicator Name'] == value
        author_name = list(df_test_docs[mask1]['Author'])[0]
        return "True Author: " + author_name
    else:
        return None

#TRUE IMAGE
@app.callback(
    Output(component_id='true-image-id', component_property='src'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_image(value):
    if value in list(df_test_docs['Indicator Name']):
        mask1 = df_test_docs['Indicator Name'] == value
        author = list(df_test_docs[mask1]['Author'])[0].lower()
        src_name = "static/" + author + ".png"
        return src_name
    else:
        return None

#MODEL PREDICTION
@app.callback(
    Output(component_id='predicted-author-name', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_model_output(value):
    if value in list(df_test_docs['Indicator Name']):
        return value
    else:
        return None

#PARAGRAPH TEXT
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
