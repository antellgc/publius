import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# reading docs into dataframes (to update to SQLite)
df = pd.read_csv("./processed_data/test_docs_merged.csv")
df_fed_para = pd.read_csv("./processed_data/fed_paragraphs.csv")

available_indicators = list(df['Indicator Name'])

# description text
description = """
The Federalist Papers are a series of 85 articles written from 1787 to 1788 to promote the 
ratification of the United States Constitution. The true authorship of each of these essays 
can be attributed to Alexander Hamilton, James Madison, or John Jay, but all were originally 
published anonymously under the pseudonym "Publius."
"""

### APP LAYOUT
app = dash.Dash(__name__,
    static_folder='static')
    #external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children="What's your name, man?",
        style = {'font-size':'4em'}),

    html.Div([    
        html.H3(children="Uncovering the authorship of the anonymously-written \
            Federalist Papers with machine learning"),
        html.P(children=description)],
        style={'width':'70%', 'textAlign':'center', 'margin':'0 auto'}
    ),

    html.Div([
    dcc.Dropdown(
        id='dropdown-id',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value='initial value',
        clearable=True,
        placeholder="Select a Federalist Paper")],
        style={'width':'50%','textAlign':'center','margin':'0 auto'}),

    html.Br(),

    html.Img(id="placeholder-image-id", style={'max-width':600}),

    html.Div([
        html.Div([
            html.H1(id='madison-confidence', style = {'font-size':'2.5em'}),
            html.Img(id='madison-img-id', style={'max-width':600})
        ], 
        style={'width':'33%', 'display':'inline-block'}),

        html.Div([
            html.H1(id='jay-confidence', style = {'font-size':'2.5em'}),
            html.Img(id='jay-img-id', style={'max-width':600})
        ], 
        style={'width':'33%', 'display':'inline-block'}),
     
        html.Div([
            html.H1(id='hamilton-confidence', style = {'font-size':'2.5em'}),
            html.Img(id='hamilton-img-id', style={'max-width':600})
        ], 
        style={'width':'33%', 'display':'inline-block'})
    ]),

    html.Div([
        html.Div([
            html.H2(id='madison-true')
        ], 
        style={'width':'33%', 'display':'inline-block'}),

        html.Div([
            html.H2(id='jay-true')
        ], 
        style={'width':'33%', 'display':'inline-block'}),
     
        html.Div([
            html.H2(id='hamilton-true')
        ], 
        style={'width':'33%', 'display':'inline-block'})
    ]),

    html.Br(),

    html.H2(id='title-name'),

    html.Blockquote(
        id ='paragraph-output-id',
        style = {'textAlign':'left'}
        )
    ],
    style = {'textAlign': 'center'})

##### APP OUTPUTS/CALLBACKS

# CONSTITUTION PLACEHOLDER IMAGE
@app.callback(
    Output(component_id='placeholder-image-id', component_property='src'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_image(value):
    if value in list(df['Indicator Name']):
        return None
    else:
        src_name = "static/constitution.png"
        return src_name

# MADISON IMAGE
@app.callback(
    Output(component_id='madison-img-id', component_property='src'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_madison_image(value):
    if value in list(df['Indicator Name']):
        src_name = "static/madison.png"
        return src_name
    else:
        return None

# JAY IMAGE
@app.callback(
    Output(component_id='jay-img-id', component_property='src'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_jay_image(value):
    if value in list(df['Indicator Name']):
        src_name = "static/jay.png"
        return src_name
    else:
        return None

# HAMILTON IMAGE
@app.callback(
    Output(component_id='hamilton-img-id', component_property='src'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_hamilton_image(value):
    if value in list(df['Indicator Name']):
        src_name = "static/hamilton.png"
        return src_name
    else:
        
        return None

# MADISON CONFIDENCE
@app.callback(
    Output(component_id='madison-confidence', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_madison_confidence(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        conf = list(df[mask1]['Madison confidence'])[0]
        return str(int(round(conf, 2) * 100)) + "%"
    else:
        return None

# JAY CONFIDENCE
@app.callback(
    Output(component_id='jay-confidence', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_jay_confidence(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        conf = list(df[mask1]['Jay confidence'])[0]
        return str(int(round(conf, 2) * 100)) + "%"
    else:
        return None

# HAMILTON CONFIDENCE
@app.callback(
    Output(component_id='hamilton-confidence', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_hamilton_confidence(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        conf = list(df[mask1]['Hamilton confidence'])[0]
        return str(int(round(conf, 2) * 100)) + "%"
    else:
        return None

# MADISON TRUE
@app.callback(
    Output(component_id='madison-true', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_madison(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        true_author = list(df[mask1]['True Author'])[0]
        if true_author == "Madison":
            return "True Author"
        else:
            return None
    else:
        return None

# JAY TRUE
@app.callback(
    Output(component_id='jay-true', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_jay(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        true_author = list(df[mask1]['True Author'])[0]
        if true_author == "Jay":
            return "True Author"
        else:
            return None
    else:
        return None

# HAMILTON TRUE
@app.callback(
    Output(component_id='hamilton-true', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_true_hamilton(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        true_author = list(df[mask1]['True Author'])[0]
        if true_author == "Hamilton":
            return "True Author"
        else:
            return None
    else:
        return None

#PARAGRAPH TITLE
@app.callback(
    Output(component_id='title-name', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_title_output(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        full_name = list(df[mask1]['Full Name'])[0]
        return full_name
    else:
        return None

#PARAGRAPH TEXT
@app.callback(
    Output(component_id='paragraph-output-id', component_property='children'),
    [Input(component_id='dropdown-id', component_property='value')]
)
def update_text_output(value):
    if value in list(df['Indicator Name']):
        mask1 = df['Indicator Name'] == value
        title = list(df[mask1]['Title'])[0]
        mask2 = df_fed_para['Title'] == title
        p_list = list(df_fed_para[mask2]['ParaText'])
        return [html.P(paragraph) for paragraph in p_list]
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
