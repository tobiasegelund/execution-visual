import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_regions_states, df_map_timeline
from app.helper_functions import filter_data
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE
from app.app import app


sidebar_page_2 = html.Div(
    [
        html.H2("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink("Overall", active=True, href="/overall"),
                dbc.NavLink("Timeline", active=True, href="/timeline"),
            ],
            style={'font-size': '18px'},
            vertical=True
        ),

        html.Hr(),
        dcc.Checklist(
            id='input_race_page2',
            options=[{'label': i, 'value': i} for i in ['White', 'Other']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            }
        ),
        html.Br(),
        dcc.Checklist(
            id='input_sex_page2',
            options=[{'label': i, 'value': i} for i in ['Male', 'Female']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            }
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region_page2',
            options=[{'label': i, 'value': i} for i in available_region],
            multi=True,
            placeholder='Select region..'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state_page2',
            # options=[{'label': i, 'value': i} for i in available_states],
            multi=True,
            placeholder='Select state..'
        )
    ],
    style=SIDEBAR_STYLE,
)

content_map_page_2 = html.Div([

    html.H1('INCOMING MAP'),
    dcc.Graph(
        id='map_timeline'
    ),
    dcc.RangeSlider(
        id='input_ranger',
        min=2010,
        max=2020,
        step=None,
        marks={str(year): str(year) for year in available_years},
        value=[2012, 2018]
    )
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
        input_state=input_state,
        input_time=input_time
    )

    fig = px.choropleth(
        data_frame=df_local,
        locationmode="USA-states",
        locations="State Code",
        color="Executions Scaled",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=[0,5],
        hover_name="State",
        hover_data={"Executions": True, "White Convicted": True, "Other Convicted": True, "State Code": False,
                    "Executions Scaled": False},
        title=f"Death Row Executions in year",
        scope="usa",
        # template="plotly_dark",
    )



    return fig





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
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
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
        marker_color='rgb(55, 83, 109)',
        hovertemplate =
            '<b>%{text}</b><br>' +
            '<i>Victims</i>: %{y} <br>'+
            '<i>Year</i>: %{x} <br>' +
            '<extra></extra>',
        text = [f'{first} {last}' for first, last in zip(df['First Name'], df['Last Name'])]
        ),
    )

    fig.update_xaxes(range=[1977, 2020], visible=True, dtick=10, fixedrange=True)
    fig.update_yaxes(range=[0, 140], visible=True, dtick=20, fixedrange=True)

    fig.update_layout(
        title='Victims over time since 1977',
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
        width=1000,
        height=500,
    )

    return fig
