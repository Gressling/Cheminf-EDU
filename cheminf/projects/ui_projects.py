from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/projects/",
                title="ChemINF-EDU - Projects",
                external_stylesheets=external_stylesheets)

def get_all_projects():
    """Get all projects from database"""
    try:
        return execute_query(f"SELECT * FROM {DB_PREFIX}project ORDER BY id")
    except Exception as e:
        print(f"Error getting projects: {e}")
        return []

def insert_project(name):
    """Insert a new project"""
    try:
        execute_query(f"INSERT INTO {DB_PREFIX}project (name) VALUES (?)", (name,))
        return True
    except Exception as e:
        print(f"Error inserting project: {e}")
        return False

def update_project(project_id, name):
    """Update a project"""
    try:
        execute_query(f"UPDATE {DB_PREFIX}project SET name = ? WHERE id = ?", (name, project_id))
        return True
    except Exception as e:
        print(f"Error updating project: {e}")
        return False

def delete_project(project_id):
    """Delete a project"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}project WHERE id = ?", (project_id,))
        return True
    except Exception as e:
        print(f"Error deleting project: {e}")
        return False

# Layout
app.layout = html.Div([
    html.Header([
        html.H1("ChemINF-EDU - Projects Management", style={"color": "white"})
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H2("Add New Project"),
            dcc.Input(
                id="project-name-input",
                type="text",
                placeholder="Enter project name...",
                style={"width": "300px", "marginRight": "10px"}
            ),
            html.Button("Add Project", id="add-project-btn", n_clicks=0, className="button"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Update Project"),
            dcc.Input(
                id="update-project-name",
                type="text", 
                placeholder="New project name...",
                style={"width": "300px", "marginRight": "10px"}
            ),
            html.Button("Update Selected", id="update-project-btn", n_clicks=0, className="button"),
            html.Button("Delete Selected", id="delete-project-btn", n_clicks=0, className="button delete"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Projects Table"),
            dash_table.DataTable(
                id="projects-table",
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Project Name", "id": "name"}
                ],
                data=get_all_projects(),
                row_selectable="single",
                selected_rows=[],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#000', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #000'},
                style_data={'backgroundColor': '#fff', 'color': '#000', 'border': '1px solid #000'},
            )
        ], className="table-section"),
        
        html.Div(id="projects-status", className="status-message"),
        
        html.Div([
            html.A("← Back to Home", href="/", className="nav-link"),
            html.A("View Tasks →", href="/tasks/", className="nav-link", style={"marginLeft": "20px"})
        ], className="navigation")
        
    ], className="container")
])

@app.callback(
    [Output("projects-table", "data"),
     Output("projects-status", "children"),
     Output("project-name-input", "value"),
     Output("update-project-name", "value")],
    [Input("add-project-btn", "n_clicks"),
     Input("update-project-btn", "n_clicks"), 
     Input("delete-project-btn", "n_clicks")],
    [State("project-name-input", "value"),
     State("update-project-name", "value"),
     State("projects-table", "selected_rows"),
     State("projects-table", "data")]
)
def manage_projects(add_clicks, update_clicks, delete_clicks, 
                   project_name, update_name, selected_rows, table_data):
    """Handle project operations"""
    ctx = callback_context
    if not ctx.triggered:
        return get_all_projects(), "", "", ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    status_msg = ""
    
    if button_id == "add-project-btn" and project_name:
        if insert_project(project_name):
            status_msg = f"✅ Project '{project_name}' added successfully!"
        else:
            status_msg = "❌ Failed to add project"
    
    elif button_id == "update-project-btn" and selected_rows and update_name:
        selected_project = table_data[selected_rows[0]]
        if update_project(selected_project['id'], update_name):
            status_msg = f"✅ Project updated to '{update_name}'"
        else:
            status_msg = "❌ Failed to update project"
    
    elif button_id == "delete-project-btn" and selected_rows:
        selected_project = table_data[selected_rows[0]]
        if delete_project(selected_project['id']):
            status_msg = f"✅ Project '{selected_project['name']}' deleted"
        else:
            status_msg = "❌ Failed to delete project"
    
    return get_all_projects(), status_msg, "", ""
