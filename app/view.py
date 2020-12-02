import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
from collections import Counter

df = pd.read_csv('./data/executions.csv')

available_region = df['Region'].unique()
available_states = df['State'].unique()
available_countys = df['County'].unique()

app = dash.Dash()

colors = {
    'background': '#ffffff',
    'text': '#7FDBFF'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_MAP_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "40rem"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "40rem"
}

sidebar = html.Div(
    [
        html.H2("Execution data", className="sidebar-design"),
        html.Hr(),
        html.P(
            "Two pages perhaps?", className="lead"
        ),
        dcc.RadioItems(
            id='input_race',
            options=[{'label': i, 'value': i} for i in ['Black', 'White']],
            value='Black'
            # labelStyle={'display': 'inline-block'}
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region',
            options=[{'label': i, 'value': i} for i in available_region],
            # value='Dropdown of regions'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state',
            options=[{'label': i, 'value': i} for i in available_states],
            # value='Dropdown of states'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_county',
            options=[{'label': i, 'value': i} for i in available_countys],
            # value='Dropdown of countys'
        ),
        html.Br()
    ],
    style=SIDEBAR_STYLE,
)

content_map = html.Div([

    dcc.Graph(
        id='indicator-tester'
    )

    ],
    style=CONTENT_MAP_STYLE
)

content = html.Div([
    # Til plots
])


@app.callback(
    Output('indicator-tester', 'figure'),
    Input('input_race', 'value'),
    Input('input_region', 'value')
)
def update_figure(input_race, input_region):


    if input_region is None:
        df_local=df[df['Race']==input_race]

    else:
        df_local=df[(df['Race']==input_race) & (df['Region']==input_region)]

    fig = px.line(
        x=list(Counter(df_local['Year']).keys()),
        y=list(Counter(df_local['Year']).values())
    )

    return fig


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[sidebar, content_map])
