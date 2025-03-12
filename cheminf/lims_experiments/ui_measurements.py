from dash import dcc, html, Input, Output, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/lims_experiments/measurements/",
    title="ChemINF-EDU - Measurements",
    external_stylesheets=['/static/styles.css']
)

app.layout = html.Div([
    html.H2("Measurements List"),
    dcc.Loading(id="loading-measurements", children=[html.Div(id="measurements-data")])
])

@app.callback(
    Output("measurements-data", "children"),
    Input("loading-measurements", "children")
)
def load_measurements(_):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {DB_NAME}.cheminf3_measurements"
    cursor.execute(query)
    measurements = cursor.fetchall()
    cursor.close()
    conn.close()
    if measurements:
        return [html.Div(f"ID: {m['measurement_id']} — {m['parameter']}: {m['value']} {m.get('unit','')}") for m in measurements]
    else:
        return "No measurements found."

if __name__ == '__main__':
    app.run_server(debug=True)