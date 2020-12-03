import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_countys, available_region, available_states, available_years, available_victim_types
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE

# START APP
app = dash.Dash()

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
        html.Br(),
        dcc.Dropdown(
            id='input_victim_types',
            options=[{'label': i, 'value': i} for i in available_victim_types],
            multi=True
        )
    ],
    style=SIDEBAR_STYLE,
)

content_map = html.Div([

    dcc.Slider(
        id='input_slider',
        min=2010,
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in available_years},
        step=None
    ),
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


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[sidebar, content_map])
