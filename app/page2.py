import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_regions_states, df_map_timeline, encoded_image, github_image
from app.helper_functions import filter_data
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE
from app.app import app


sidebar_page_2 = html.Div(
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
                    style={'display': '-webkit-inline-box'}
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
            vertical=True
        ),

        html.Hr(),
        html.H5('Filter on executions', style={'font-size':'14px'}),
        html.Br(),
        html.H6('RACE:'),
        dcc.Checklist(
            id='input_race_page2',
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
            id='input_sex_page2',
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
        html.H6('REGION:'),
        dcc.Dropdown(
            id='input_region_page2',
            options=[{'label': i, 'value': i} for i in available_region],
            multi=True,
            placeholder='Select region..'
        ),
        html.Br(),
        html.H6('STATE:'),
        dcc.Dropdown(
            id='input_state_page2',
            # options=[{'label': i, 'value': i} for i in available_states],
            multi=True,
            placeholder='Select state..'
        ),
        html.Br(),
        html.A(
            [
            html.Img(src='data:image/png;base64,{}'.format(github_image.decode()),
                                style={'height': '50px'})
            ], href='https://github.com/tobiasegelund/execution-visual', target="_blank", style={"margin-left": "80px"}
        )
    ],
    style=SIDEBAR_STYLE,
)

content_page2 = html.Div(
    [

        html.H2('Death Row Executions 1977-2020'),
        html.Div(
            dcc.RangeSlider(
                id='input_ranger',
                min=1977,
                max=2020,
                step=None,
                marks={str(year): {'label': str(year), 'style': {'font-size': '13px'}} for year in available_years},
                value=[1985, 2010]
            )
         ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id='map_timeline'
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
                        html.H4('Executions over time since 1977'),
                        dcc.Graph(
                            id='executions_timeline_page2'
                        )
                    ]),
                    width=6
                ),
                dbc.Col(
                    html.Div([
                        html.H4('Number of victims by executed humans over time since 1977'),
                        dcc.Graph(
                            id='victims_grouped_page2'
                        )
                    ]),
                    width=6
                ),
            ]
        )
    ],
    style=CONTENT_MAP_STYLE
)

page_2_layout = html.Div([
        sidebar_page_2,
        content_page2
    ]
)

@app.callback(
    Output('input_state_page2', 'options'),
    Input('input_region_page2', 'value'),
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
    Output('map_timeline', 'figure'),
    Input('input_race_page2', 'value'),
    Input('input_region_page2', 'value'),
    Input('input_sex_page2', 'value'),
    Input('input_state_page2', 'value'),
    Input('input_ranger', 'value')
)
def update_map_timeline(input_race, input_region, input_sex, input_state, input_time):

    df_local = filter_data(
        df_map_timeline,
        input_sex=input_sex,
        input_race=input_race,
        input_state=input_state,
        input_time=input_time,
        input_region=input_region
    )

    # https://plotly.com/python/reference/#layout-legend
    fig = go.Figure(
        data=go.Choropleth(
        locations=df_local['State Code'],
        z=df_local["Executions scaled"].astype(float),
        zmin=0,
        zmax=6,
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
            tickvals=[0.5, 5.5],
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
            width=1300,
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
    Output('executions_timeline_page2', 'figure'),
    Input('input_race_page2', 'value'),
    Input('input_region_page2', 'value'),
    Input('input_sex_page2', 'value'),
    Input('input_state_page2', 'value'),
    Input('input_ranger', 'value')
)
def executions_timeline(input_race, input_region, input_sex, input_state, input_year):

    df_local = filter_data(df,
        # input_race=input_race,
        input_region=input_region,
        input_sex=input_sex,
        input_state=input_state
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(Counter(df_local['Year']).keys()),
        y=list(Counter(df_local['Year']).values()),
        name='All',
        line={'width': 2, 'color': 'black', 'dash': 'dash'}
        # dash options include 'dash', 'dot', and 'dashdot'
        )
    )

    df_local_white = df_local[df_local['Race']=='White']
    df_local_other = df_local[df_local['Race']!='White']

    fig.add_trace(go.Scatter(
        x=list(Counter(df_local_white['Year']).keys()),
        y=list(Counter(df_local_white['Year']).values()),
        name='White humans',
        line={'width': 2, 'color': '#183363'},
        )
    )

    fig.add_trace(go.Scatter(
        x=list(Counter(df_local_other['Year']).keys()),
        y=list(Counter(df_local_other['Year']).values()),
        name='Other humans',
        line={'width': 2, 'color': '#68021f'},
        )
    )

    fig.update_xaxes(range=[1977, 2020], visible=True, dtick=10, fixedrange=True)
    fig.update_yaxes(range=[0, 100], visible=True, dtick=20, fixedrange=True)

    # strip down the rest of the plot
    fig.update_layout(
        # title='Humans executated over time since 1977',
        xaxis_title='Year',
        yaxis_title='Executions',
        showlegend=True,
        plot_bgcolor="white",
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        margin = dict(t=0, l=0, r=0, b=0),
    )


    return fig


@app.callback(
    Output('victims_grouped_page2', 'figure'),
    Input('input_race_page2', 'value'),
    Input('input_region_page2', 'value'),
    Input('input_sex_page2', 'value'),
    Input('input_state_page2', 'value'),
    Input('input_ranger', 'value')
)
def victims_timeline(input_race, input_region, input_sex, input_state, input_year):

    fig = go.Figure()

    df_local = filter_data(df,
        input_race=input_race,
        input_region=input_region,
        input_sex=input_sex,
        input_state=input_state
    )

    fig.add_trace(go.Bar(
        x=df_local['Year'],
        y=df_local['Number of Victims'],
        marker_color='rgb(55, 83, 109)',
        hovertemplate =
            '<b>%{text}</b><br>' +
            '<i>Victims</i>: %{y} <br>'+
            '<i>Year</i>: %{x} <br>' +
            '<extra></extra>',
        text = [f'{first} {last}' for first, last in zip(df_local['First Name'], df_local['Last Name'])]
        ),
    )

    fig.update_xaxes(range=[1977, 2020], visible=True, dtick=10, fixedrange=True)
    fig.update_yaxes(range=[0, 140], visible=True, dtick=20, fixedrange=True)

    fig.update_layout(
        # title='Victims over time since 1977',
        xaxis_title='Year',
        yaxis_title='Victims',
        showlegend=False,
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right',
        margin = dict(t=0, l=0, r=0, b=0),
        # width=1000,
        # height=500,
    )

    return fig
