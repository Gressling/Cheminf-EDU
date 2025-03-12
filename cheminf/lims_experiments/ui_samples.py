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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {DB_NAME}.cheminf3_samples"
    cursor.execute(query)
    samples = cursor.fetchall()
    cursor.close()
    conn.close()
    if samples:
        return [html.Div(f"ID: {s['sample_id']} — Code: {s['sample_code']}") for s in samples]
    else:
        return "No samples found."

if __name__ == '__main__':
    app.run_server(debug=True)