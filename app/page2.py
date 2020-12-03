import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_victim_types
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE


sidebar_page_2 = html.Div(
    [
        html.H2("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink(
                        "Overall", active=True, href="/execution-page1"
                ),
                dbc.NavLink("Timeline", active=True, href="/execution-page2"),
            ],
            vertical=True
        ),

        html.Hr(),
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
            id='input_victim_types',
            options=[{'label': i, 'value': i} for i in available_victim_types],
            multi=True
        )
    ],
    style=SIDEBAR_STYLE,
)

content_page_2= html.Div([
    html.H1('PAGE 2'),
    ],
    style=CONTENT_MAP_STYLE
)


page_2_layout = html.Div([
        sidebar_page_2,
        content_page_2
    ]
)
