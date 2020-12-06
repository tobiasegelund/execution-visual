import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from collections import Counter
from app.inputs import df, available_region, available_states, available_years, available_regions_states, encoded_image, encoded_image2, df_map
from app.style import colors, SIDEBAR_STYLE, CONTENT_MAP_STYLE, CONTENT_STYLE,CONTENT_STYLE_PART1, CONTENT_STYLE_PART2
from app.helper_functions import filter_data
from app.app import app


sidebar_page_1 = html.Div(
    [
        html.H1("Execution", className="sidebar-design"),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Span(
                        [html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                            style={'height': '30px'}
                        ),
                        html.P("Overall", style={'margin-left': '8px', 'margin-top': '1px', 'margin-bottom': '-25px'})
                    ],
                    style={'display': '-webkit-inline-box'}
                    ),
                    active=True,
                    href="/overall"
                ),
                dbc.NavLink(
                    html.Span(
                        [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={'height': '30px'}
                        ),
                        html.P("Timeline", style={'margin-left': '8px', 'margin-top': '1px'})
                    ],
                    style={'display': '-webkit-inline-box'}
                    ),
                    active=True,
                    href="/timeline"),
            ],
            style={'font-size': '18px'},
            vertical=True,
        ),

        html.Hr(),
        dcc.Checklist(
            id='input_race_page1',
            options=[{'label': i, 'value': i} for i in ['White', 'Other']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            }
        ),
        html.Br(),
        dcc.Checklist(
            id='input_sex_page1',
            options=[{'label': i, 'value': i} for i in ['Male', 'Female']],
            value=[],
            style={
                'font-size': '17px',
                'font-weight': '700'
            }
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_region_page1',
            options=[{'label': i, 'value': i} for i in available_region],
            multi=True,
            placeholder='Select region..'
        ),
        html.Br(),
        dcc.Dropdown(
            id='input_state_page1',
            # options=[{'label': i, 'value': i} for i in available_states],
            multi=True,
            placeholder='Select state..'
        ),
        html.Br()
    ],
    style=SIDEBAR_STYLE,
)

content_map_page_1 = html.Div([
    html.H2('INCOMING MAP'),
    dcc.Graph(
        id='map1'
    )
    ],
    style=CONTENT_MAP_STYLE
)

content_part1_page_1 = html.Div([
    dcc.Graph(
        id='race_convicted_figure'
    ),
    dcc.Graph(
        id='victims_figure'
    )],
    style=CONTENT_STYLE_PART1
)

content_part2_page_1 = html.Div([
    dcc.Graph(
        id='sex_convicted_figure'
    )],
    style=CONTENT_STYLE_PART2
)


page_1_layout = html.Div([
    sidebar_page_1,
    content_map_page_1,
    content_part1_page_1,
    content_part2_page_1
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

    if input_race == ['White']:
        local_colors  = [colors['highlight_color'], colors['plot_color']]
    elif input_race == ['Other']:
        local_colors = [colors['plot_color'], colors['highlight_color']]
    else:
        local_colors = [colors['plot_color'], colors['plot_color']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_local[['White Convicted', 'Other Convicted']].sum().keys(),
        y=df_local[['White Convicted', 'Other Convicted']].sum(),
        marker_color=local_colors,
        hovertemplate =
          '<b>%{text}</b><br>' +
          '<i>Deaths</i>: %{y} <br>' +
          '<extra></extra>',
        text = ['White Convicted', 'Other Convicted']
    ))

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

    fig.update_layout(
        title='Executions based on race',
        height=400,
        width=400,
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right'
    )

    return fig


@app.callback(
    Output('map1', 'figure'),
    Input('input_race_page1', 'value'),
    Input('input_region_page1', 'value'),
    Input('input_sex_page1', 'value'),
    Input('input_state_page1', 'value')
)
def update_map(input_race, input_region, input_sex, input_state):

    df_local = filter_data(
            df=df_map,
            input_state=input_state
        )

    fig = px.choropleth(
        data_frame=df_local,
        locationmode="USA-states",
        locations="State Code",
        color=np.log(df_local["Executions"]+1),
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=[0,8],
        hover_name="State",
        hover_data={"Executions": True, "White Convicted": True, "Other Convicted": True, "State Code": False,
                    "Executions Scaled": False, "White/Other ratio": False},
        title="Death Row Executions 1977-2016",
        scope="usa"
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

    if input_sex == ['Male']:
        local_colors  = [colors['highlight_color'], colors['plot_color']]
    elif input_sex == ['Female']:
        local_colors = [colors['plot_color'], colors['highlight_color']]
    else:
        local_colors = [colors['plot_color'], colors['plot_color']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_local[['Male Convicted', 'Female Convicted']].sum().keys(),
        y=df_local[['Male Convicted', 'Female Convicted']].sum(),
        marker_color=local_colors,
        hovertemplate =
          '<b>%{text}</b><br>' +
          '<i>Deaths</i>: %{y} <br>' +
          '<extra></extra>',
        text = ['Male', 'Female']
        )
    )

    fig.update_layout(
        title='Executions based on sex',
        height=400,
        width=400,
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right'
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
        hovertemplate =
          '<b>%{text}</b><br>' +
          '<i>Deaths</i>: %{y} <br>' +
          '<extra></extra>',
        text = ['White Male Victims', 'White Female Victims', 'Other Male Victims', 'Other Female Victims']
        )
    )

    fig.update_layout(
        title='Victims based on race and sex',
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        hoverlabel_align = 'right'
    )

    return fig
