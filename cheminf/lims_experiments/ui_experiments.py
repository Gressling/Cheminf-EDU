from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX

external_stylesheets = ['/static/styles.css']

app = Dash(__name__, 
           server=server,
           url_base_pathname="/experiments/",
           title="ChemINF-EDU - Experiments",
           external_stylesheets=external_stylesheets)

def get_all_experiments():
    """Get all experiments from database"""
    try:
        return execute_query(f"SELECT * FROM {DB_PREFIX}experiments ORDER BY experiment_id")
    except Exception as e:
        print(f"Error getting experiments: {e}")
        return []

def insert_experiment(name, description, start_date, end_date):
    """Insert a new experiment"""
    try:
        execute_query(
            f"INSERT INTO {DB_PREFIX}experiments (experiment_name, description, start_date, end_date) VALUES (?, ?, ?, ?)",
            (name, description, start_date, end_date)
        )
        return True
    except Exception as e:
        print(f"Error inserting experiment: {e}")
        return False

def delete_experiment(experiment_id):
    """Delete an experiment"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}experiments WHERE experiment_id = ?", (experiment_id,))
        return True
    except Exception as e:
        print(f"Error deleting experiment: {e}")
        return False

app.layout = html.Div([
    html.Header([
        html.H1("ChemINF-EDU - LIMS Experiments", style={"color": "white"})
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H2("Add New Experiment"),
            dcc.Input(
                id="exp-name-input",
                type="text",
                placeholder="Experiment name...",
                style={"width": "200px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="exp-description-input",
                type="text",
                placeholder="Description...",
                style={"width": "300px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Br(),
            html.Label("Start Date:"),
            dcc.Input(
                id="exp-start-date",
                type="date",
                style={"marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Label("End Date:"),
            dcc.Input(
                id="exp-end-date",
                type="date",
                style={"marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Br(),
            html.Button("Add Experiment", id="add-exp-btn", n_clicks=0, className="button"),
            html.Button("Delete Selected", id="delete-exp-btn", n_clicks=0, className="button delete"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Experiments"),
            html.Button("Refresh", id='load-button', n_clicks=0, className="button"),
            dash_table.DataTable(
                id="experiments-table",
                columns=[
                    {"name": "ID", "id": "experiment_id"},
                    {"name": "Name", "id": "experiment_name"},
                    {"name": "Description", "id": "description"},
                    {"name": "Start Date", "id": "start_date"},
                    {"name": "End Date", "id": "end_date"}
                ],
                data=get_all_experiments(),
                row_selectable="single",
                selected_rows=[],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#000', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #000'},
                style_data={'backgroundColor': '#fff', 'color': '#000', 'border': '1px solid #000'},
            )
        ], className="table-section"),
        
        html.Div(id="experiments-status", className="status-message"),
        
        html.Div([
            html.A("← Back to Home", href="/", className="nav-link"),
            html.A("View Samples →", href="/samples/", className="nav-link", style={"marginLeft": "20px"}),
            html.A("View Measurements →", href="/measurements/", className="nav-link", style={"marginLeft": "20px"})
        ], className="navigation")
        
    ], className="container")
])

@app.callback(
    [Output("experiments-table", "data"),
     Output("experiments-status", "children"),
     Output("exp-name-input", "value"),
     Output("exp-description-input", "value"),
     Output("exp-start-date", "value"),
     Output("exp-end-date", "value")],
    [Input("load-button", "n_clicks"),
     Input("add-exp-btn", "n_clicks"),
     Input("delete-exp-btn", "n_clicks")],
    [State("exp-name-input", "value"),
     State("exp-description-input", "value"),
     State("exp-start-date", "value"),
     State("exp-end-date", "value"),
     State("experiments-table", "selected_rows"),
     State("experiments-table", "data")]
)
def manage_experiments(load_clicks, add_clicks, delete_clicks,
                      name, description, start_date, end_date,
                      selected_rows, table_data):
    """Handle experiment operations"""
    ctx = callback_context
    if not ctx.triggered:
        return get_all_experiments(), "", "", "", "", ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    status_msg = ""
    
    if button_id in ["load-button", "experiments-table"]:
        status_msg = f"📊 Loaded {len(get_all_experiments())} experiments"
    
    elif button_id == "add-exp-btn" and name:
        if insert_experiment(name, description or "", start_date, end_date):
            status_msg = f"✅ Experiment '{name}' added successfully!"
        else:
            status_msg = "❌ Failed to add experiment"
    
    elif button_id == "delete-exp-btn" and selected_rows:
        selected_exp = table_data[selected_rows[0]]
        if delete_experiment(selected_exp['experiment_id']):
            status_msg = f"✅ Experiment '{selected_exp['experiment_name']}' deleted"
        else:
            status_msg = "❌ Failed to delete experiment"
    
    return get_all_experiments(), status_msg, "", "", "", ""

if __name__ == '__main__':
    app.run_server(debug=True)