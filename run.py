import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app.style import colors
from app.page1 import page_1_layout
from app.page2 import page_2_layout
from app.page3 import page_3_layout
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
    if pathname == '/overview':
        return page_1_layout
    elif pathname == '/timeline':
        return page_2_layout
    elif pathname == '/frameofreference':
        return page_3_layout
    else:
        return page_1_layout



if __name__ == '__main__':
    app.run_server(debug=True)
