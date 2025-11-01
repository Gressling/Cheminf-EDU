from dash import dcc, html, Input, Output, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/lims_experiments/experiments/",
    title="ChemINF-EDU - Experiments",
    external_stylesheets=['/static/styles.css']
)

app.layout = html.Div([
    html.H2("Experiments List"),
    dcc.Loading(id="loading-experiments", children=[html.Div(id="experiments-data")])
])

@app.callback(
    Output("experiments-data", "children"),
    Input("loading-experiments", "children")
)
def load_experiments(_):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

if __name__ == '__main__':
    app.run_server(debug=True)