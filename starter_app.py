import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# reading docs into dataframes (to update to SQLite)
df_test_docs = pd.read_csv("./processed_data/test_docs.csv")
df_fed_para = pd.read_csv("./processed_data/fed_paragraphs.csv")

# creating indicators for drop down menu
df_test_docs['Indicator Name'] = "No. " + df_test_docs['No.'].map(str) + " - " + df_test_docs['Title']
available_indicators = df_test_docs['Indicator Name'].unique()

# generating paragraphs functin
def generate_paragraphs(dataframe, no):
    df_show = dataframe[dataframe['No.'] == no]
    p_list = list(df_show['ParaText'])
    return html.Div([html.P(paragraph) for paragraph in p_list])

## selecting a paper (#71 as an example)
no = 78 # temporary

app = dash.Dash(__name__,
    static_folder='static')
    #external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children="What's your name, man?",
        style = {'font-size':'4em'}),

    html.Img(src="static/constitution.png",
        style = {'max-width':600}),

    html.H3(children="Uncovering the authorship of the anonymously-written \
        Federalist Papers with machine learning"),

    dcc.Input(id='my-id', value='initial value', type='text'),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value='x',
        clearable=False,
        placeholder="Select a Federalist Paper"
        ),

    html.Br(),

    html.Blockquote(generate_paragraphs(df_fed_para, no),
        style = {'textAlign':'left'})

], style={'textAlign': 'center'})

@app.callback(
    Output(),
    [Input()]
)

def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
