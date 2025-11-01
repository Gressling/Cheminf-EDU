from dash import dcc, html, Input, Output, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/reactions/overview/",
    title="ChemINF-EDU - Reaction Overview",
    external_stylesheets=['/static/styles.css']
)

app.layout = html.Div([
    # Home link in header
    html.Div(
      html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
      style={"textAlign": "right", "padding": "10px"}
    ),
    html.H1("Reaction Overview"),
    html.Button("Load Reaction Overview", id="load-overview-btn"),
    html.Div(id="overview-result", style={"marginTop": "20px", "padding": "10px", "border": "1px solid #ccc"})
])

@app.callback(
    Output("overview-result", "children"),
    Input("load-overview-btn", "n_clicks")
)
def load_overview(n_clicks):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

if __name__ == '__main__':
    app.run_server(debug=True)