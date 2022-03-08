from dash import Dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
import flask
from dash.dependencies import Input, Output

from layout.total_capacity.total_capacity import plot_capacity
from layout.layout import layout
from layout.models.models import pie_chart


server = flask.Flask(__name__)
app = Dash(
    name=__name__, 
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = layout

cache = Cache(app.server, config={
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "cache-directory"
})
