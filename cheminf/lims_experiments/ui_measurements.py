from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX

external_stylesheets = ['/static/styles.css']

app = Dash(__name__, 
           server=server,
           url_base_pathname="/measurements/",
           title="ChemINF-EDU - Measurements",
           external_stylesheets=external_stylesheets)

def get_all_measurements():
    """Get all measurements with sample and experiment info"""
    try:
        query = f"""
        SELECT m.measurement_id, m.parameter, m.value, m.unit, m.measurement_date,
               s.sample_code, e.experiment_name, m.sample_id
        FROM {DB_PREFIX}measurements m
        JOIN {DB_PREFIX}samples s ON m.sample_id = s.sample_id
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        ORDER BY m.measurement_id
        """
        return execute_query(query)
    except Exception as e:
        print(f"Error getting measurements: {e}")
        return []

def get_all_samples():
    """Get all samples for dropdown"""
    try:
        query = f"""
        SELECT s.sample_id, s.sample_code, e.experiment_name
        FROM {DB_PREFIX}samples s
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        ORDER BY s.sample_code
        """
        return execute_query(query)
    except Exception as e:
        print(f"Error getting samples: {e}")
        return []

def insert_measurement(sample_id, parameter, value, unit, measurement_date):
    """Insert a new measurement"""
    try:
        execute_query(
            f"INSERT INTO {DB_PREFIX}measurements (sample_id, parameter, value, unit, measurement_date) VALUES (?, ?, ?, ?, ?)",
            (sample_id, parameter, value, unit, measurement_date)
        )
        return True
    except Exception as e:
        print(f"Error inserting measurement: {e}")
        return False

def delete_measurement(measurement_id):
    """Delete a measurement"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}measurements WHERE measurement_id = ?", (measurement_id,))
        return True
    except Exception as e:
        print(f"Error deleting measurement: {e}")
        return False

app.layout = html.Div([
    html.Header([
        html.H1("ChemINF-EDU - LIMS Measurements", style={"color": "white"})
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H2("Add New Measurement"),
            dcc.Dropdown(
                id="measurement-sample-dropdown",
                options=[{"label": f"{s['sample_code']} ({s['experiment_name']})", "value": s["sample_id"]} for s in get_all_samples()],
                placeholder="Select sample...",
                style={"width": "400px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="measurement-parameter-input",
                type="text",
                placeholder="Parameter (e.g., pH, Temperature)...",
                style={"width": "200px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="measurement-value-input",
                type="number",
                placeholder="Value...",
                style={"width": "150px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="measurement-unit-input",
                type="text",
                placeholder="Unit (e.g., mg/L, °C)...",
                style={"width": "100px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Br(),
            html.Label("Measurement Date/Time:"),
            dcc.Input(
                id="measurement-datetime",
                type="datetime-local",
                style={"marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Br(),
            html.Button("Add Measurement", id="add-measurement-btn", n_clicks=0, className="button"),
            html.Button("Delete Selected", id="delete-measurement-btn", n_clicks=0, className="button delete"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Measurements"),
            html.Button("Refresh", id='load-measurements-btn', n_clicks=0, className="button"),
            dash_table.DataTable(
                id="measurements-table",
                columns=[
                    {"name": "ID", "id": "measurement_id"},
                    {"name": "Sample", "id": "sample_code"},
                    {"name": "Experiment", "id": "experiment_name"},
                    {"name": "Parameter", "id": "parameter"},
                    {"name": "Value", "id": "value", "type": "numeric"},
                    {"name": "Unit", "id": "unit"},
                    {"name": "Date/Time", "id": "measurement_date"}
                ],
                data=get_all_measurements(),
                row_selectable="single",
                selected_rows=[],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#000', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #000'},
                style_data={'backgroundColor': '#fff', 'color': '#000', 'border': '1px solid #000'},
                style_cell_conditional=[
                    {'if': {'column_id': 'value'}, 'textAlign': 'right'},
                ]
            )
        ], className="table-section"),
        
        html.Div(id="measurements-status", className="status-message"),
        
        html.Div([
            html.A("← Back to Samples", href="/samples/", className="nav-link"),
            html.A("← Back to Experiments", href="/experiments/", className="nav-link", style={"marginLeft": "20px"}),
            html.A("← Back to Home", href="/", className="nav-link", style={"marginLeft": "20px"})
        ], className="navigation")
        
    ], className="container")
])

@app.callback(
    [Output("measurements-table", "data"),
     Output("measurements-status", "children"),
     Output("measurement-parameter-input", "value"),
     Output("measurement-value-input", "value"),
     Output("measurement-unit-input", "value"),
     Output("measurement-datetime", "value"),
     Output("measurement-sample-dropdown", "value")],
    [Input("load-measurements-btn", "n_clicks"),
     Input("add-measurement-btn", "n_clicks"),
     Input("delete-measurement-btn", "n_clicks")],
    [State("measurement-sample-dropdown", "value"),
     State("measurement-parameter-input", "value"),
     State("measurement-value-input", "value"),
     State("measurement-unit-input", "value"),
     State("measurement-datetime", "value"),
     State("measurements-table", "selected_rows"),
     State("measurements-table", "data")]
)
def manage_measurements(load_clicks, add_clicks, delete_clicks,
                       sample_id, parameter, value, unit, measurement_datetime,
                       selected_rows, table_data):
    """Handle measurement operations"""
    ctx = callback_context
    if not ctx.triggered:
        return get_all_measurements(), "", "", "", "", "", None
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    status_msg = ""
    
    if button_id == "load-measurements-btn":
        status_msg = f"📊 Loaded {len(get_all_measurements())} measurements"
    
    elif button_id == "add-measurement-btn" and sample_id and parameter and value is not None:
        if insert_measurement(sample_id, parameter, value, unit or "", measurement_datetime):
            status_msg = f"✅ Measurement '{parameter}' added successfully!"
        else:
            status_msg = "❌ Failed to add measurement"
    
    elif button_id == "delete-measurement-btn" and selected_rows:
        selected_measurement = table_data[selected_rows[0]]
        if delete_measurement(selected_measurement['measurement_id']):
            status_msg = f"✅ Measurement deleted successfully"
        else:
            status_msg = "❌ Failed to delete measurement"
    
    return get_all_measurements(), status_msg, "", "", "", "", None

if __name__ == '__main__':
    app.run_server(debug=True)