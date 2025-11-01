from dash import dcc, html, Input, Output, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/lims_experiments/samples/",
    title="ChemINF-EDU - Samples",
    external_stylesheets=['/static/styles.css']
)

app.layout = html.Div([
    html.H2("Samples List"),
    dcc.Loading(id="loading-samples", children=[html.Div(id="samples-data")])
])

@app.callback(
    Output("samples-data", "children"),
    Input("loading-samples", "children")
)
def load_samples(_):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

if __name__ == '__main__':
    app.run_server(debug=True)