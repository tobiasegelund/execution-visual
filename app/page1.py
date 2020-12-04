import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE,CONTENT_STYLE_PART1, CONTENT_STYLE_PART2
from app.helper_functions import filter_data
from app.app import app


sidebar_page_1 = html.Div(
    [
        html.H2("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink("Overall", active=True, href="/overall"),
                dbc.NavLink("Timeline", active=True, href="/timeline"),
            ],
            vertical=True,
        ),

        html.Hr(),
        dcc.RadioItems(
            id='input_race_page1',
            options=[{'label': i, 'value': i} for i in ['All', 'White', 'Other']],
            value='All'
        ),
        html.Br(),
        dcc.RadioItems(
            id='input_sex_page1',
            options=[{'label': i, 'value': i} for i in ['Both', 'Male', 'Female']],
            value='Both'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region_page1',
            options=[{'label': i, 'value': i} for i in available_region]
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state_page1',
            options=[{'label': i, 'value': i} for i in available_states]
        ),
        html.Br()
    ],
    style=SIDEBAR_STYLE,
)

content_map_page_1 = html.Div([
    html.H1('INCOMING MAP')

    ],
    style=CONTENT_MAP_STYLE
)

content_part1_page_1 = html.Div([
    dcc.Graph(
        id='race_convicted_figure'
    ),
    dcc.Graph(
        id='victims_figure'
    )
    ],
    style=CONTENT_STYLE_PART1
)

content_part2_page_1 = html.Div([
    dcc.Graph(
        id='sex_convicted_figure'
    )
    ],
    style=CONTENT_STYLE_PART2
)



page_1_layout = html.Div([
        sidebar_page_1,
        content_map_page_1,
        content_part1_page_1,
        content_part2_page_1
    ]
)


@app.callback(
    Output('race_convicted_figure', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def race_convicted_update(input_race, input_region, input_sex, input_state):


    df_local = filter_data(df,
        input_region=input_region,
        input_sex=input_sex,
        input_state=input_state
    )

    if input_race == 'White':
        local_colors  = [colors['highlight_color'], colors['plot_color']]
    elif input_race == 'Other':
        local_colors = [colors['plot_color'], colors['highlight_color']]
    else:
        local_colors = [colors['plot_color'], colors['plot_color']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_local[['White Convicted', 'Other Convicted']].sum().keys(),
        y=df_local[['White Convicted', 'Other Convicted']].sum(),
        marker_color=local_colors
        )
    )

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

    fig.update_layout(
        title='Executions based on race',
        height=400,
        width=400,
        plot_bgcolor="white",
    )

    return fig


@app.callback(
    Output('sex_convicted_figure', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def sex_convicted_update(input_race, input_region, input_sex, input_state):


    df_local = filter_data(df,
        input_race=input_race,
        input_region=input_region,
        input_state=input_state
    )

    if input_sex == 'Male':
        local_colors  = [colors['highlight_color'], colors['plot_color']]
    elif input_sex == 'Female':
        local_colors = [colors['plot_color'], colors['highlight_color']]
    else:
        local_colors = [colors['plot_color'], colors['plot_color']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_local[['Male Convicted', 'Female Convicted']].sum().keys(),
        y=df_local[['Male Convicted', 'Female Convicted']].sum(),
        marker_color=local_colors
        )
    )

    fig.update_layout(
        title='Executions based on sex',
        height=400,
        width=400,
        plot_bgcolor="white",
    )

    return fig


@app.callback(
    Output('victims_figure', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def victims_update(input_race, input_region, input_sex, input_state):

    fig = go.Figure()

    df_local = filter_data(df,
        input_race=input_race,
        input_region=input_region,
        input_sex=input_sex,
        input_state=input_state
        )

    fig.add_trace(go.Bar(
        x=df_local[['White Male Victims', 'White Female Victims', 'Other Male Victims', 'Other Female Victims']].sum().keys(),
        y=df_local[['White Male Victims', 'White Female Victims', 'Other Male Victims', 'Other Female Victims']].sum(),
        marker_color=colors['plot_color'],
        )
    )

    fig.update_layout(
        title='Victims based on race and sex',
        plot_bgcolor="white",
    )

    return fig
