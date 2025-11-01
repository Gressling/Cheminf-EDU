from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/tasks/",
                title="ChemINF-EDU - Tasks",
                external_stylesheets=external_stylesheets)

def get_all_tasks():
    """Get all tasks with project names"""
    try:
        query = f"""
        SELECT t.id, t.description, t.content, t.project_id, p.name as project_name
        FROM {DB_PREFIX}task t
        JOIN {DB_PREFIX}project p ON t.project_id = p.id
        ORDER BY t.id
        """
        return execute_query(query)
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return []

def get_all_projects():
    """Get all projects for dropdown"""
    try:
        return execute_query(f"SELECT id, name FROM {DB_PREFIX}project ORDER BY name")
    except Exception as e:
        print(f"Error getting projects: {e}")
        return []

def insert_task(project_id, description, content):
    """Insert a new task"""
    try:
        execute_query(
            f"INSERT INTO {DB_PREFIX}task (project_id, description, content) VALUES (?, ?, ?)",
            (project_id, description, content)
        )
        return True
    except Exception as e:
        print(f"Error inserting task: {e}")
        return False

def update_task(task_id, project_id, description, content):
    """Update a task"""
    try:
        execute_query(
            f"UPDATE {DB_PREFIX}task SET project_id = ?, description = ?, content = ? WHERE id = ?",
            (project_id, description, content, task_id)
        )
        return True
    except Exception as e:
        print(f"Error updating task: {e}")
        return False

def delete_task(task_id):
    """Delete a task"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}task WHERE id = ?", (task_id,))
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False

# Layout
app.layout = html.Div([
    html.Header([
        html.H1("ChemINF-EDU - Tasks Management", style={"color": "white"})
    ], className="header"),
    
    html.Div([
        html.Div([
            html.H2("Add New Task"),
            dcc.Dropdown(
                id="project-dropdown",
                options=[{"label": p["name"], "value": p["id"]} for p in get_all_projects()],
                placeholder="Select project...",
                style={"width": "300px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="task-description-input",
                type="text",
                placeholder="Enter task description...",
                style={"width": "300px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            dcc.Textarea(
                id="task-content-input",
                placeholder="Enter task content/details...",
                style={"width": "300px", "height": "100px", "marginRight": "10px"}
            ),
            html.Br(),
            html.Button("Add Task", id="add-task-btn", n_clicks=0, className="button"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Update Task"),
            dcc.Dropdown(
                id="update-project-dropdown",
                options=[{"label": p["name"], "value": p["id"]} for p in get_all_projects()],
                placeholder="Select new project...",
                style={"width": "300px", "marginBottom": "10px"}
            ),
            dcc.Input(
                id="update-task-description",
                type="text",
                placeholder="New task description...",
                style={"width": "300px", "marginRight": "10px", "marginBottom": "10px"}
            ),
            dcc.Textarea(
                id="update-task-content",
                placeholder="New task content...",
                style={"width": "300px", "height": "100px", "marginRight": "10px"}
            ),
            html.Br(),
            html.Button("Update Selected", id="update-task-btn", n_clicks=0, className="button"),
            html.Button("Delete Selected", id="delete-task-btn", n_clicks=0, className="button delete"),
        ], className="input-section"),
        
        html.Div([
            html.H2("Tasks Table"),
            dash_table.DataTable(
                id="tasks-table",
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Project", "id": "project_name"},
                    {"name": "Description", "id": "description"},
                    {"name": "Content", "id": "content"}
                ],
                data=get_all_tasks(),
                row_selectable="single",
                selected_rows=[],
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#000', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #000'},
                style_data={'backgroundColor': '#fff', 'color': '#000', 'border': '1px solid #000'},
                style_cell_conditional=[
                    {'if': {'column_id': 'content'}, 'width': '40%'},
                    {'if': {'column_id': 'description'}, 'width': '30%'},
                ]
            )
        ], className="table-section"),
        
        html.Div(id="tasks-status", className="status-message"),
        
        html.Div([
            html.A("← Back to Projects", href="/projects/", className="nav-link"),
            html.A("← Back to Home", href="/", className="nav-link", style={"marginLeft": "20px"})
        ], className="navigation")
        
    ], className="container")
])

@app.callback(
    [Output("tasks-table", "data"),
     Output("tasks-status", "children"),
     Output("task-description-input", "value"),
     Output("task-content-input", "value"),
     Output("update-task-description", "value"),
     Output("update-task-content", "value"),
     Output("project-dropdown", "value"),
     Output("update-project-dropdown", "value")],
    [Input("add-task-btn", "n_clicks"),
     Input("update-task-btn", "n_clicks"),
     Input("delete-task-btn", "n_clicks")],
    [State("project-dropdown", "value"),
     State("task-description-input", "value"),
     State("task-content-input", "value"),
     State("update-project-dropdown", "value"),
     State("update-task-description", "value"),
     State("update-task-content", "value"),
     State("tasks-table", "selected_rows"),
     State("tasks-table", "data")]
)
def manage_tasks(add_clicks, update_clicks, delete_clicks,
                project_id, description, content,
                update_project_id, update_description, update_content,
                selected_rows, table_data):
    """Handle task operations"""
    ctx = callback_context
    if not ctx.triggered:
        return get_all_tasks(), "", "", "", "", "", None, None
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    status_msg = ""
    
    if button_id == "add-task-btn" and project_id and description:
        if insert_task(project_id, description, content or ""):
            status_msg = f"✅ Task '{description}' added successfully!"
        else:
            status_msg = "❌ Failed to add task"
    
    elif button_id == "update-task-btn" and selected_rows:
        selected_task = table_data[selected_rows[0]]
        new_project_id = update_project_id or selected_task['project_id']
        new_description = update_description or selected_task['description']
        new_content = update_content or selected_task['content']
        
        if update_task(selected_task['id'], new_project_id, new_description, new_content):
            status_msg = f"✅ Task updated successfully!"
        else:
            status_msg = "❌ Failed to update task"
    
    elif button_id == "delete-task-btn" and selected_rows:
        selected_task = table_data[selected_rows[0]]
        if delete_task(selected_task['id']):
            status_msg = f"✅ Task '{selected_task['description']}' deleted"
        else:
            status_msg = "❌ Failed to delete task"
    
    return get_all_tasks(), status_msg, "", "", "", "", None, None
