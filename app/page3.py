import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import available_region, available_states, available_regions_states, encoded_image, state_stats, race_pop_data, race_victim_pop_data
from app.helper_functions import filter_data
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE
from app.app import app



sidebar_page_3 = html.Div(
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
        html.H5('Filter on executions', style={'font-size':'14px'}),
        html.Br(),
        html.H6('REGION:'),
        dcc.Dropdown(
            id='input_region_page3',
            options=[{'label': i, 'value': i} for i in available_region],
            multi=True,
            placeholder='Select region..'
        ),
        html.Br(),
        html.H6('STATE:'),
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
        html.H2('Death Row Executions 1977-2020'),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id='map2'
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
                        html.H4('Executions Per Million of Total Race Population'),
                        dcc.Graph(
                            id='race_execution_output'
                        )
                    ]),
                    width=6
                ),
                dbc.Col(
                    html.Div([
                        html.H4('Victims Per Million of Total Race Population'),
                        dcc.Graph(
                            id='race_victims_output'
                        )
                    ]),
                    width=6
                ),
                html.Footer(
                    [
                        "https://www.governing.com/gov-data/census/state-minority-population-data-estimates.html"
                    ]
                )
            ]
        )
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




@app.callback(
    Output('map2', 'figure'),
    Input('input_region_page3', 'value'),
    Input('input_state_page3', 'value'),
)
def update_map2(input_region, input_state):
    df_local = filter_data(state_stats,
        input_region=input_region,
        input_state=input_state)

    df_local['pop_m'] = round(df_local['Population'] / 1000000,2)
    df_local['exe-pop-ratio_round'] = round(df_local['exe-pop-ratio'],2)

    fig = go.Figure(
        data=go.Choropleth(
        locations=df_local['State Code'],
        z=df_local["exe-pop-ratio"].astype(float),
        zmin=0,
        zmax=30,
        locationmode='USA-states',
        colorscale=px.colors.sequential.Teal,
        colorbar_len=0.5,
        autocolorscale=False,
        marker_line_color='white', # line markers between states
        text=df_local[['State', 'Executions', 'pop_m', 'exe-pop-ratio_round']], # hover text
        hovertemplate=
            '<b>%{text[0]}</b><br>' +
            '<i>Executions</i>: %{text[1]} <br>' +
            '<i>Population</i>: %{text[2]}M <br>' +
            '<i>Executions pr. M capita</i>: %{text[3]}' +
            '<extra></extra>',
        colorbar=dict(
            title="No. of executions",
            x=0.8,
            y=0.5,
            titleside="top",
            tickmode="array",
            tickvals=[1, 29],
            ticktext=['Low', 'High'],
            ticks="outside"
        )
    ))

    fig.update_layout(
        # title_text='Death Row Executions 1977-2020',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
            height=600,
            width=1500,
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            hoverlabel_align = 'right',
            margin = dict(t=0, l=0, r=0, b=50),
    )

    return fig


@app.callback(
    Output('race_execution_output', 'figure'),
    Input('input_region_page3', 'value'),
    Input('input_state_page3', 'value'),
)
def race_executions(input_region, input_state):


    df_local = filter_data(race_pop_data,
        input_region=input_region,
        input_state=input_state)

    df_local = df_local.groupby(['Race']).sum().reset_index()

    df_local['Executions Race Ratio'] = round(df_local['Executions'] / (df_local['Race Population']/1e6),2)

    df_local['Race Population M'] = round(df_local['Race Population']/1e6, 2)


    fig = go.Figure(data=[
        go.Bar(
            name='Executions',
            y=df_local['Executions Race Ratio'],
            x=df_local['Race'],
            text=df_local[['Race', 'Executions', 'Executions Race Ratio', 'Race Population M']],
            hovertemplate=
            '<b>%{text[0]}</b><br>' +
            '<i>Executions</i>: %{text[1]} <br>' +
            '<i>Race population </i>: %{text[3]}M <br>' +
            '<i>Executions pr. M capita</i>: %{text[2]} <br>' +
            '<extra></extra>',
        )
    ])
    fig.update_yaxes(
        title='Executions pr. M capita'
    )

    fig.update_xaxes(
        title='Race',
        categoryorder="total descending"
    )

    fig.update_traces(
        marker_color=colors['plot_color'],
        # marker_line_color='rgb(8,48,107)',
        # marker_line_width=1.5,
        # opacity=0.6
    )

    fig.update_layout(
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
    )

    return fig



@app.callback(
    Output('race_victims_output', 'figure'),
    Input('input_region_page3', 'value'),
    Input('input_state_page3', 'value'),
)
def race_victims(input_region, input_state):


    df_local = filter_data(
        race_victim_pop_data,
        input_region=input_region,
        input_state=input_state
    )

    df_local = df_local.groupby(['Race']).sum().reset_index()


    df_local['Victims Race Ratio'] = round(df_local['Victim'] / (df_local['Race Population']/1e6), 2)

    df_local['Race Population M'] = round(df_local['Race Population']/1e6, 2)

    fig = go.Figure(data=[
        go.Bar(
            name='Victim',
            y=df_local['Victims Race Ratio'],
            x=df_local['Race'],
            text=df_local[['Race', 'Victim', 'Victims Race Ratio', 'Race Population M']],
            hovertemplate=
            '<b>%{text[0]}</b><br>' +
            '<i>Victims</i>: %{text[1]} <br>' +
            '<i>Race population</i>: %{text[3]}M <br>' +
            '<i>Victims pr. M capita </i>: %{text[2]} <br>' +
            '<extra></extra>',
        )
    ])
    fig.update_yaxes(
        title='Victims pr. M capita'

    )

    fig.update_xaxes(
        title='Race',
        categoryorder="total descending"
    )

    fig.update_traces(
        marker_color=colors['plot_color'],
        # marker_line_color='rgb(8,48,107)',
        # marker_line_width=1.5,
        # opacity=0.6
    )

    fig.update_layout(
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
    )
    return fig
