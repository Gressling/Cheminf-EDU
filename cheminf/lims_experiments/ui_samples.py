from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX

external_stylesheets = ['/static/styles.css']

app = Dash(__name__, 
           server=server,
           url_base_pathname="/samples/",
           title="ChemINF-EDU - Samples",
           external_stylesheets=external_stylesheets)

def get_all_samples():
    """Get all samples with experiment info"""
    try:
        query = f"""
        SELECT s.sample_id, s.sample_code, s.sample_type, s.collection_date, 
               s.experiment_id, e.experiment_name
        FROM {DB_PREFIX}samples s
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        ORDER BY s.sample_id
        """
        return execute_query(query)
    except Exception as e:
        print(f"Error getting samples: {e}")
        return []

def get_all_experiments():
    """Get all experiments for dropdown"""
    try:
        return execute_query(f"SELECT experiment_id, experiment_name FROM {DB_PREFIX}experiments ORDER BY experiment_name")
    except Exception as e:
        print(f"Error getting experiments: {e}")
        return []

def insert_sample(experiment_id, sample_code, sample_type, collection_date):
    """Insert a new sample"""
    try:
        execute_query(
            f"INSERT INTO {DB_PREFIX}samples (experiment_id, sample_code, sample_type, collection_date) VALUES (?, ?, ?, ?)",
            (experiment_id, sample_code, sample_type, collection_date)
        )
        return True
    except Exception as e:
        print(f"Error inserting sample: {e}")
        return False

def delete_sample(sample_id):
    """Delete a sample"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}samples WHERE sample_id = ?", (sample_id,))
        return True
    except Exception as e:
        print(f"Error deleting sample: {e}")
        return False

app.layout = html.Div([
    html.Header([
        html.H1("ChemINF-EDU - LIMS Samples", style={"color": "white"})
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H2("Add New Sample"),
            dcc.Dropdown(
                id="sample-experiment-dropdown",
                options=[{"label": e["experiment_name"], "value": e["experiment_id"]} for e in get_all_experiments()],
                placeholder="Select experiment...",
                style={"width": "300px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="sample-code-input",
                type="text",
                placeholder="Sample code...",
                style={"width": "200px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="sample-type-input",
                type="text",
                placeholder="Sample type...",
                style={"width": "200px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Br(),
            html.Label("Collection Date:"),
            dcc.Input(
                id="sample-collection-date",
                type="date",
                style={"marginRight": "10px", "marginBottom": "10px"}
            ),
            html.Br(),
            html.Button("Add Sample", id="add-sample-btn", n_clicks=0, className="button"),
            html.Button("Delete Selected", id="delete-sample-btn", n_clicks=0, className="button delete"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Samples"),
            html.Button("Refresh", id='load-samples-btn', n_clicks=0, className="button"),
            dash_table.DataTable(
                id="samples-table",
                columns=[
                    {"name": "Sample ID", "id": "sample_id"},
                    {"name": "Code", "id": "sample_code"},
                    {"name": "Type", "id": "sample_type"},
                    {"name": "Collection Date", "id": "collection_date"},
                    {"name": "Experiment", "id": "experiment_name"}
                ],
                data=get_all_samples(),
                row_selectable="single",
                selected_rows=[],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#000', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #000'},
                style_data={'backgroundColor': '#fff', 'color': '#000', 'border': '1px solid #000'},
            )
        ], className="table-section"),
        
        html.Div(id="samples-status", className="status-message"),
        
        html.Div([
            html.A("← Back to Experiments", href="/experiments/", className="nav-link"),
            html.A("View Measurements →", href="/measurements/", className="nav-link", style={"marginLeft": "20px"}),
            html.A("← Back to Home", href="/", className="nav-link", style={"marginLeft": "20px"})
        ], className="navigation")
        
    ], className="container")
])

@app.callback(
    [Output("samples-table", "data"),
     Output("samples-status", "children"),
     Output("sample-code-input", "value"),
     Output("sample-type-input", "value"),
     Output("sample-collection-date", "value"),
     Output("sample-experiment-dropdown", "value")],
    [Input("load-samples-btn", "n_clicks"),
     Input("add-sample-btn", "n_clicks"),
     Input("delete-sample-btn", "n_clicks")],
    [State("sample-experiment-dropdown", "value"),
     State("sample-code-input", "value"),
     State("sample-type-input", "value"),
     State("sample-collection-date", "value"),
     State("samples-table", "selected_rows"),
     State("samples-table", "data")]
)
def manage_samples(load_clicks, add_clicks, delete_clicks,
                  experiment_id, sample_code, sample_type, collection_date,
                  selected_rows, table_data):
    """Handle sample operations"""
    ctx = callback_context
    if not ctx.triggered:
        return get_all_samples(), "", "", "", "", None
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    status_msg = ""
    
    if button_id == "load-samples-btn":
        status_msg = f"📊 Loaded {len(get_all_samples())} samples"
    
    elif button_id == "add-sample-btn" and experiment_id and sample_code:
        if insert_sample(experiment_id, sample_code, sample_type or "", collection_date):
            status_msg = f"✅ Sample '{sample_code}' added successfully!"
        else:
            status_msg = "❌ Failed to add sample"
    
    elif button_id == "delete-sample-btn" and selected_rows:
        selected_sample = table_data[selected_rows[0]]
        if delete_sample(selected_sample['sample_id']):
            status_msg = f"✅ Sample '{selected_sample['sample_code']}' deleted"
        else:
            status_msg = "❌ Failed to delete sample"
    
    return get_all_samples(), status_msg, "", "", "", None

if __name__ == '__main__':
    app.run_server(debug=True)