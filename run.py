import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app.style import colors
from app.page1 import page_1_layout
from app.page2 import page_2_layout
from app.app import app

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

# UPDATE PAGE
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/execution-page1':
        return page_1_layout
    else:
        return page_2_layout



if __name__ == '__main__':
    app.run_server(debug=True)
