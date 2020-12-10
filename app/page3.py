import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_regions_states, df_map_timeline, encoded_image
from app.helper_functions import filter_data
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE
from app.app import app



sidebar_page_3 = html.Div(
    [
        html.H2("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Span(
                        [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={'height': '20px', 'margin-top': '-3px'}
                        ),
                        html.P("Overview", style={'margin-left': '8px', 'margin-top': '1px', 'margin-bottom': '-25px'})
                    ],
                    style={'display': '-webkit-inline-box', 'opacity': '0.6'}
                    ),
                    active=True,
                    href="/overview"
                ),
                dbc.NavLink(
                    html.Span(
                        [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={'height': '20px', 'margin-top': '-3px'}
                        ),
                        html.P("Timeline", style={'margin-left': '8px', 'margin-top': '0px', 'margin-bottom': '-25px'})
                    ],
                    style={'display': '-webkit-inline-box', 'opacity': '0.6'}
                    ),
                    active=True,
                    href="/timeline"),
                dbc.NavLink(
                    html.Span(
                        [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={'height': '20px', 'margin-top': '-3px'}
                        ),
                        html.P("Frame of reference", style={'margin-left': '8px', 'margin-top': '0px'})
                    ],
                    style={'display': '-webkit-inline-box'}
                    ),
                    active=True,
                    href="/frameofreference"),
            ],
            style={'font-size': '18px'},
            vertical=True
        ),

        html.Hr(),
        dcc.Checklist(
            id='input_race_page3',
            options=[{'label': i, 'value': i} for i in ['White', 'Other']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            },
            labelStyle={"margin-right": "10px"},
            inputStyle={"margin-right": "5px"}
        ),
        html.Br(),
        dcc.Checklist(
            id='input_sex_page3',
            options=[{'label': i, 'value': i} for i in ['Male', 'Female']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            },
            labelStyle={"margin-right": "10px"},
            inputStyle={"margin-right": "5px"}
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region_page3',
            options=[{'label': i, 'value': i} for i in available_region],
            multi=True,
            placeholder='Select region..'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state_page3',
            # options=[{'label': i, 'value': i} for i in available_states],
            multi=True,
            placeholder='Select state..'
        )
    ],
    style=SIDEBAR_STYLE,
)

content_page3 = html.Div(
    [
        html.H2('INCOMING')
    ],
    style=CONTENT_MAP_STYLE
)

page_3_layout = html.Div([
        sidebar_page_3,
        content_page3
    ]
)


@app.callback(
    Output('input_state_page3', 'options'),
    Input('input_region_page3', 'value'),
)
def update_states(input_region):
    if input_region is None or input_region == []:
        return [{'label': i, 'value': i} for i in available_states]

    else:
        values = list(map(available_regions_states.get, input_region))
        states = []
        for value in values:
            for state in value:
                states.append(state)

        return [{'label': i, 'value': i} for i in states]
