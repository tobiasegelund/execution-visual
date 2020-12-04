import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years
from app.helper_functions import filter_data
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE
from app.app import app


sidebar_page_2 = html.Div(
    [
        html.H2("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink(
                        "Overall", active=True, href="/overall"
                ),
                dbc.NavLink("Timeline", active=True, href="/timeline"),
            ],
            vertical=True
        ),

        html.Hr(),
        dcc.RadioItems(
            id='input_race_page2',
            options=[{'label': i, 'value': i} for i in ['All', 'White', 'Other']],
            value='All'
        ),
        html.Br(),
        dcc.RadioItems(
            id='input_sex_page2',
            options=[{'label': i, 'value': i} for i in ['Both', 'Male', 'Female']],
            value='Both'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region_page2',
            options=[{'label': i, 'value': i} for i in available_region]
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state_page2',
            options=[{'label': i, 'value': i} for i in available_states]
        )
    ],
    style=SIDEBAR_STYLE,
)

content_map_page_2 = html.Div([

    html.H1('INCOMING MAP'),
    dcc.Slider(
        id='input_slider_page1',
        min=2010,
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in available_years},
        step=None
    ),
    ],
    style=CONTENT_MAP_STYLE
)

content_page_2= html.Div([
    dcc.Graph(
        id='executions_timeline_page2'
    ),
    dcc.Graph(
        id='victims_grouped_page2'
    )
    ],
    style=CONTENT_STYLE
)


page_2_layout = html.Div([
        sidebar_page_2,
        content_map_page_2,
        content_page_2
    ]
)


@app.callback(
    Output('executions_timeline_page2', 'figure'),
    Input('input_race_page2', 'value'),
    Input('input_region_page2', 'value'),
    Input('input_sex_page2', 'value'),
    Input('input_state_page2', 'value')
)
def executions_timelige(input_race, input_region, input_sex, input_state):

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
        line={'width': 2, 'color': colors['plot_color']}
        # dash options include 'dash', 'dot', and 'dashdot'
        )
    )

    df_local_white = df_local[df_local['Race']=='White']
    df_local_other = df_local[df_local['Race']!='White']

    fig.add_trace(go.Scatter(
        x=list(Counter(df_local_white['Year']).keys()),
        y=list(Counter(df_local_white['Year']).values()),
        name='White humans',
        line={'width': 2, 'color': 'green'},
        )
    )

    fig.add_trace(go.Scatter(
        x=list(Counter(df_local_other['Year']).keys()),
        y=list(Counter(df_local_other['Year']).values()),
        name='Other humans',
        line={'width': 2, 'color': 'crimson'},
        )
    )

    fig.update_xaxes(range=[1977, 2020], visible=True, dtick=10, fixedrange=True)
    fig.update_yaxes(range=[0, 100], visible=True, dtick=20, fixedrange=True)

    # strip down the rest of the plot
    fig.update_layout(
        title='Humans executated over time since 1977',
        xaxis_title='Year',
        yaxis_title='Executions',
        showlegend=True,
        plot_bgcolor="white",
        # margin=dict(t=10,l=10,b=10,r=10)
    )


    return fig


@app.callback(
    Output('victims_grouped_page2', 'figure'),
    Input('input_race_page2', 'value'),
    Input('input_region_page2', 'value'),
    Input('input_sex_page2', 'value'),
    Input('input_state_page2', 'value')
)
def victims_timeline(input_race, input_region, input_sex, input_state):

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
        marker_color='rgb(55, 83, 109)'
        )
    )

    fig.update_xaxes(range=[1977, 2020], visible=True, dtick=10, fixedrange=True)
    fig.update_yaxes(range=[0, 140], visible=True, dtick=20, fixedrange=True)

    fig.update_layout(
        title='Victims over time since 1977',
        xaxis_title='Year',
        yaxis_title='# of Victims',
        showlegend=False,
        plot_bgcolor="white",
        # width=1000,
        # height=500,
    )

    return fig
