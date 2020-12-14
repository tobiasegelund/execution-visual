import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_regions_states, encoded_image, df_map, df_executions_sunburst, df_victims_sunburst, github_image
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE,CONTENT_STYLE_PART1, CONTENT_STYLE_PART2
from app.helper_functions import filter_data, build_hierarchical_dataframe
from app.app import app


sidebar_page_1 = html.Div(
    [
        html.H2("Executions", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Span(
                        [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={'height': '20px', 'margin-top': '-3px'}
                        ),
                        html.P("Overview", style={'margin-left': '8px', 'margin-top': '1px', 'margin-bottom': '-25px'})
                    ],
                    style={'display': '-webkit-inline-box'}
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
                    style={'display': '-webkit-inline-box', 'opacity': '0.6'}
                    ),
                    active=True,
                    href="/frameofreference"),
            ],
            style={'font-size': '18px'},
            vertical=True,
        ),

        html.Hr(),
        html.H5('Filter on executed', style={'font-size':'14px'}),
        html.Br(),
        html.H6('RACE:'),
        dcc.Checklist(
            id='input_race_page1',
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
        html.H6('GENDER:'),
        dcc.Checklist(
            id='input_sex_page1',
            options=[{'label': i, 'value': i} for i in ['Male', 'Female']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            },
            labelStyle={"margin-right": "20px"},
            inputStyle={"margin-right": "5px"}
        ),
        html.Br(),
        html.H6('REGION:'),
        dcc.Dropdown(
            id='input_region_page1',
            options=[{'label': i, 'value': i} for i in available_region],
            multi=True,
            placeholder='Select region..'
        ),
        html.Br(),
        html.H6('STATE:'),
        dcc.Dropdown(
            id='input_state_page1',
            # options=[{'label': i, 'value': i} for i in available_states],
            multi=True,
            placeholder='Select state..'
        ),
        html.Br(),
        html.Span(
            [
                "Source: ",
                html.A(
                    [
                       "deathpenaltyinfo.org"
                    ], href='https://deathpenaltyinfo.org/executions/execution-database', target="_blank", #style={"margin-left": "60px"}
                ),
            ]
        ),
        html.Br(),
        html.A(
            [
            html.Img(src='data:image/png;base64,{}'.format(github_image.decode()),
                                style={'height': '50px'})
            ], href='https://github.com/tobiasegelund/execution-visual', target="_blank", style={"margin-left": "75px"}
        ),
        html.Div(
            [
                html.P(
                    'Made by: Martin Christiansen, Magnus Engelsen, Bilal Ali & Tobias Egelund'
                ),
            ], style={'padding-top': '550px'}
        )
    ],
    style=SIDEBAR_STYLE,
)

content_page1 = html.Div(
    [
        html.H2('Death Row Executions 1977-2020'),
        html.H6('(Hover to explore)'),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id='map1'
                        )
                    ]),
                    width={"offset": 2}
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H4('Executions based on race & gender'),
                        html.H6('(Hover and click to explore)'),
                        dcc.Graph(
                            id='convicted_sunburst_figure',
                            # style={'margin-top': '-20px'},
                        )
                    ]),
                    width={"offset": 2}
                ),
                dbc.Col(
                    html.Div([
                        html.H4('Victims based on race & gender'),
                        html.H6('(Hover or click to explore)'),
                        dcc.Graph(
                            id='victims_figure'
                        )
                    ]),
                    width={"offset": 2}
                ),
            ]
        ),
    ],
    style=CONTENT_MAP_STYLE
)



page_1_layout = html.Div([
    sidebar_page_1,
    content_page1
])


@app.callback(
    Output('input_state_page1', 'options'),
    Input('input_region_page1', 'value'),
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


@app.callback(
    Output('map1', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def update_map(input_race, input_region, input_sex, input_state):

    # https://plotly.com/python/builtin-colorscales/
    df_local = filter_data(
            df=df_map,
            input_race=input_race,
            input_sex=input_sex,
            input_state=input_state,
            input_region = input_region
        )

    df_local = df_local.groupby(['State', 'Region', 'State Code']).sum().reset_index()
    df_local["Executions scaled"] = np.log(df_local["Executions"])

    fig = go.Figure(
        data=go.Choropleth(
        locations=df_local['State Code'],
        z=df_local["Executions scaled"].astype(float),
        zmin=0,
        zmax=8,
        locationmode='USA-states',
        colorscale=px.colors.sequential.Teal,
        colorbar_len=0.5,
        autocolorscale=False,
        marker_line_color='white', # line markers between states
        text=df_local[['State', 'Executions', 'White Convicted', 'Other Convicted']], # hover text
        hovertemplate=
            '<b>%{text[0]}</b><br>' +
            '<i>Executions</i>: %{text[1]} <br>' +
            '<extra></extra>',
        colorbar=dict(
            title="No. of executions",
            x=0.9,
            y=0.5,
            titleside="top",
            tickmode="array",
            tickvals=[0.5, 7.5],
            ticktext=['Low', 'High'],
            ticks="outside"
        )
    ))

    fig.update_layout(
        # title_text='Death Row Executions 1977-2020',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        height=600,
        width=1300,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right',
        margin = dict(t=0, l=0, r=0, b=50),
        legend=dict(
            bgcolor='black',
            orientation='v'
        )
    )

    return fig



@app.callback(
    Output('convicted_sunburst_figure', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def convicted_sunburst_update(input_race, input_region, input_sex, input_state):
    df_local = filter_data(df_executions_sunburst,
        input_race=input_race,
        input_region=input_region,
        input_sex=input_sex,
        input_state=input_state
    )

    df_local = build_hierarchical_dataframe(df_local, ['Race4', 'Race3', 'Race2'], 'Executions')

    fig = go.Figure()

    # https://plotly.com/python/reference/sunburst/#sunburst-text
    fig.add_trace(go.Sunburst(
        labels=df_local["id"],
        parents=df_local["parent"],
        values=df_local["value"],
        branchvalues="total",
        maxdepth=4,
        marker=dict(
            colors=df_local['color'],
            colorscale='RdBu',
            cmid=0.5,
            line=dict(
                width=1
            )
        ),
        insidetextfont=dict(
            size=16,
            family="Rockwell"
        ),
        text=df_local[['percentage']],
        textinfo='label',
        insidetextorientation='tangential',
        hovertemplate='<b>%{label} </b> <br> <i>Executions: </i>%{value}<br>'+
        '<i>Percentage: </i>%{text[0]} % <br>' +
                        '<extra></extra>',
    ))

    fig.update_layout(
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right',
        margin = dict(t=0, l=0, r=0, b=0),
        height = 550,
        width = 550
    )

    return fig


@app.callback(
    Output('victims_figure', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def victims_sunburst_update(input_race, input_region, input_sex, input_state):

    df_local = filter_data(df_victims_sunburst,
        input_race=input_race,
        input_region=input_region,
        input_sex=input_sex,
        input_state=input_state
    )

    df_local = build_hierarchical_dataframe(df_local, ['Race4', 'Race3', 'Race2'], 'Victim')

    fig = go.Figure()

    # https://plotly.com/python/reference/sunburst/#sunburst-text
    fig.add_trace(go.Sunburst(
        labels=df_local["id"],
        parents=df_local["parent"],
        values=df_local["value"],
        branchvalues="total",
        text=df_local[['percentage']],
        textinfo='label',
        maxdepth=4,
        marker=dict(
            colors=df_local['color'],
            colorscale='RdBu',
            cmid=0.5,
            line=dict(
                width=1
            )
        ),
        insidetextfont=dict(
            size=16,
            family="Rockwell"
        ),
        insidetextorientation='tangential',
        hovertemplate='<b>%{label} </b> <br> <i>Victims: </i>%{value}<br>'+
                        '<i>Percentage: </i>%{text[0]} % <br>' +
                        '<extra></extra>',
    ))

    fig.update_layout(
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right',
        margin = dict(t=0, l=0, r=0, b=0),
        height = 550,
        width = 550
    )

    return fig
