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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {DB_NAME}.cheminf3_experiments"
    cursor.execute(query)
    experiments = cursor.fetchall()
    cursor.close()
    conn.close()
    if experiments:
        return [html.Div(f"ID: {e['experiment_id']} — Name: {e['experiment_name']}") for e in experiments]
    else:
        return "No experiments found."

if __name__ == '__main__':
    app.run_server(debug=True)