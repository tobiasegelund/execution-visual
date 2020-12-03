import dash
import dash_bootstrap_components as dbc

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

LUMEN = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/lumen/bootstrap.min.css"

LUX = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/lux/bootstrap.min.css"

SKETCHY = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sketchy/bootstrap.min.css"

SPACELAB = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/spacelab/bootstrap.min.css"

YETI = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/yeti/bootstrap.min.css"

app = dash.Dash(
    suppress_callback_exceptions=True,
    external_stylesheets=[LUX]
)
