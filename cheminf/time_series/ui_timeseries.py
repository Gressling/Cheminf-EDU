from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import dash
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from cheminf.app_server import server
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX

external_stylesheets = ['/static/styles.css']

app = Dash(__name__, 
           server=server,
           url_base_pathname="/timeseries/",
           title="ChemINF-EDU - Time Series Analysis",
           external_stylesheets=external_stylesheets)

def get_all_experiments():
    """Get all experiments that have time series data"""
    try:
        query = f"""
        SELECT DISTINCT e.experiment_id, e.experiment_name, e.description,
               COUNT(ts.series_id) as series_count
        FROM {DB_PREFIX}experiments e
        JOIN {DB_PREFIX}time_series ts ON e.experiment_id = ts.experiment_id
        GROUP BY e.experiment_id, e.experiment_name, e.description
        ORDER BY e.experiment_name
        """
        return execute_query(query)
    except Exception as e:
        print(f"Error getting experiments: {e}")
        return []

def get_series_for_experiment(experiment_id):
    """Get all time series for a specific experiment"""
    try:
        query = f"""
        SELECT DISTINCT series_name, parameter_name, unit,
               COUNT(*) as data_points,
               MIN(timestamp) as start_time,
               MAX(timestamp) as end_time
        FROM {DB_PREFIX}time_series
        WHERE experiment_id = ?
        GROUP BY series_name, parameter_name, unit
        ORDER BY parameter_name
        """
        return execute_query(query, (experiment_id,))
    except Exception as e:
        print(f"Error getting series: {e}")
        return []

def get_time_series_data(experiment_id, parameters=None):
    """Get time series data for plotting"""
    try:
        if parameters:
            placeholders = ','.join(['?' for _ in parameters])
            query = f"""
            SELECT series_name, parameter_name, time_step, timestamp, value, unit
            FROM {DB_PREFIX}time_series
            WHERE experiment_id = ? AND parameter_name IN ({placeholders})
            ORDER BY parameter_name, time_step
            """
            params = [experiment_id] + parameters
        else:
            query = f"""
            SELECT series_name, parameter_name, time_step, timestamp, value, unit
            FROM {DB_PREFIX}time_series
            WHERE experiment_id = ?
            ORDER BY parameter_name, time_step
            """
            params = [experiment_id]
        
        return execute_query(query, params)
    except Exception as e:
        print(f"Error getting time series data: {e}")
        return []

def create_line_chart(experiment_id, selected_parameters):
    """Create a line chart for selected parameters"""
    if not experiment_id or not selected_parameters:
        return {}
    
    data = get_time_series_data(experiment_id, selected_parameters)
    if not data:
        return {}
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data, columns=['series_name', 'parameter_name', 'time_step', 'timestamp', 'value', 'unit'])
    
    # Create subplots if more than one parameter with different units
    unique_units = df['unit'].unique()
    if len(unique_units) > 1:
        # Create subplots for different units
        fig = make_subplots(
            rows=len(unique_units), 
            cols=1,
            subplot_titles=[f"Parameters in {unit}" if unit else "Dimensionless Parameters" for unit in unique_units],
            vertical_spacing=0.08
        )
        
        row = 1
        for unit in unique_units:
            unit_data = df[df['unit'] == unit]
            for param in unit_data['parameter_name'].unique():
                param_data = unit_data[unit_data['parameter_name'] == param]
                fig.add_trace(
                    go.Scatter(
                        x=param_data['time_step'],
                        y=param_data['value'],
                        mode='lines+markers',
                        name=f"{param} ({unit})" if unit else param,
                        line=dict(width=2),
                        marker=dict(size=4)
                    ),
                    row=row, col=1
                )
            
            fig.update_yaxes(title_text=f"Value ({unit})" if unit else "Value", row=row, col=1)
            row += 1
        
        fig.update_xaxes(title_text="Time Step", row=len(unique_units), col=1)
        
    else:
        # Single plot for same units
        fig = go.Figure()
        
        for param in df['parameter_name'].unique():
            param_data = df[df['parameter_name'] == param]
            unit = param_data['unit'].iloc[0]
            
            fig.add_trace(go.Scatter(
                x=param_data['time_step'],
                y=param_data['value'],
                mode='lines+markers',
                name=f"{param} ({unit})" if unit else param,
                line=dict(width=2),
                marker=dict(size=4)
            ))
        
        fig.update_xaxes(title="Time Step")
        fig.update_yaxes(title=f"Value ({unique_units[0]})" if unique_units[0] else "Value")
    
    fig.update_layout(
        title="Time Series Analysis",
        height=400 * len(unique_units) if len(unique_units) > 1 else 500,
        showlegend=True,
        template="plotly_white",
        font=dict(size=12)
    )
    
    return fig

app.layout = html.Div([
    html.Header([
        html.H1("ChemINF-EDU - Time Series Analysis", style={"color": "white"})
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H2("Experiment Selection"),
            dcc.Dropdown(
                id="experiment-dropdown",
                options=[
                    {"label": f"{exp['experiment_name']} ({exp['series_count']} series)", "value": exp['experiment_id']} 
                    for exp in get_all_experiments()
                ],
                placeholder="Select experiment...",
                style={"marginBottom": "20px"}
            ),
        ], className="input-section"),
        
        html.Div([
            html.H2("Parameter Selection"),
            dcc.Checklist(
                id="parameter-checklist",
                options=[],
                value=[],
                inline=False,
                style={"marginBottom": "20px"}
            ),
            html.Button("Update Chart", id="update-chart-btn", n_clicks=0, className="button"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Time Series Chart"),
            dcc.Graph(
                id="timeseries-chart",
                figure={},
                style={"height": "600px"}
            )
        ], className="table-section"),
        
        html.Div([
            html.H2("Series Information"),
            dash_table.DataTable(
                id="series-info-table",
                columns=[
                    {"name": "Parameter", "id": "parameter_name"},
                    {"name": "Unit", "id": "unit"},
                    {"name": "Data Points", "id": "data_points"},
                    {"name": "Start Time", "id": "start_time"},
                    {"name": "End Time", "id": "end_time"}
                ],
                data=[],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold'},
                style_data={'backgroundColor': '#1f1f1f', 'color': '#e0e0e0'},
            )
        ], className="table-section"),
        
        html.Div(id="timeseries-status", className="status-message"),
        
        html.Div([
            html.A("← Back to Home", href="/", className="nav-link"),
            html.A("View Experiments →", href="/experiments/", className="nav-link", style={"marginLeft": "20px"}),
        ], className="navigation")
        
    ], className="container")
])

@app.callback(
    [Output("parameter-checklist", "options"),
     Output("parameter-checklist", "value"),
     Output("series-info-table", "data")],
    [Input("experiment-dropdown", "value")]
)
def update_parameter_options(experiment_id):
    """Update parameter options when experiment is selected"""
    if not experiment_id:
        return [], [], []
    
    series_data = get_series_for_experiment(experiment_id)
    
    # Create options for parameter selection
    options = [
        {"label": f"{row['parameter_name']} ({row['unit']}) - {row['data_points']} points", 
         "value": row['parameter_name']} 
        for row in series_data
    ]
    
    # Select first 4 parameters by default (up to 4 as requested)
    default_selection = [row['parameter_name'] for row in series_data[:4]]
    
    return options, default_selection, series_data

@app.callback(
    [Output("timeseries-chart", "figure"),
     Output("timeseries-status", "children")],
    [Input("update-chart-btn", "n_clicks")],
    [State("experiment-dropdown", "value"),
     State("parameter-checklist", "value")]
)
def update_chart(n_clicks, experiment_id, selected_parameters):
    """Update the time series chart"""
    if not experiment_id or not selected_parameters:
        return {}, "Please select an experiment and parameters"
    
    if len(selected_parameters) > 4:
        return {}, "Please select up to 4 parameters maximum"
    
    try:
        fig = create_line_chart(experiment_id, selected_parameters)
        if not fig:
            return {}, "No data available for selected parameters"
        
        status_msg = f"Chart updated with {len(selected_parameters)} parameters"
        return fig, status_msg
    
    except Exception as e:
        return {}, f"Error creating chart: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)