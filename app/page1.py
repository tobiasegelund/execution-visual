import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_victim_types
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE
from app.app import app


sidebar_page_1 = html.Div(
    [
        html.H2("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink("Overall", active=True, href="/execution-page1"),
                dbc.NavLink("Timeline", active=True, href="/execution-page2"),
            ],
            vertical=True,
        ),

        html.Hr(),
        dcc.RadioItems(
            id='input_race_page1',
            options=[{'label': i, 'value': i} for i in ['Black', 'White']],
            value='Black'
            # labelStyle={'display': 'inline-block'}
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region_page1',
            options=[{'label': i, 'value': i} for i in available_region],
            # value='Dropdown of regions'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state_page1',
            options=[{'label': i, 'value': i} for i in available_states],
            # value='Dropdown of states'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_victim_types_page1',
            options=[{'label': i, 'value': i} for i in available_victim_types],
            multi=True
        )
    ],
    style=SIDEBAR_STYLE,
)

content_map_page_1 = html.Div([

    dcc.Slider(
        id='input_slider_page1',
        min=2010,
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in available_years},
        step=None
    ),
    dcc.Graph(
        id='indicator_tester_page1'
    )

    ],
    style=CONTENT_MAP_STYLE
)

content_page_1 = html.Div([
    html.H1('PAGE 1'),
    ],
    style=CONTENT_MAP_STYLE
)



page_1_layout = html.Div([
        sidebar_page_1,
        content_map_page_1
    ]
)


@app.callback(
    Output('indicator_tester_page1', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value')
)
def update_figure(input_race, input_region):


    if input_region is None:
        df_local=df[df['Race']==input_race]

    else:
        df_local=df[(df['Race']==input_race) & (df['Region']==input_region)]


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(Counter(df_local['Year']).keys()),
        y=list(Counter(df_local['Year']).values()),
        name='Legend-name',
        line={'width': 2, 'color': 'rgb(229, 151, 50)', 'dash':'dash'}
        # dash options include 'dash', 'dot', and 'dashdot'
        )
    )

    # fig.update_xaxes(visible=False, fixedrange=True)
    # fig.update_yaxes(visible=False, fixedrange=True)

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

    # strip down the rest of the plot
    fig.update_layout(
        title='Figure Title',
        xaxis_title='Year',
        yaxis_title='Deaths',
        showlegend=False,
        plot_bgcolor="white",
        # margin=dict(t=10,l=10,b=10,r=10)
    )


    return fig
