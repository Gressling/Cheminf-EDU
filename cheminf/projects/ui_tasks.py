from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Construct the full table name for tasks.
TASK_TABLE = f"{DB_NAME}.{DB_PREFIX}task"

# Helper function to fetch tasks for a given project_id.
def get_tasks_for_project(project_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {TASK_TABLE} WHERE project_id = %s", (project_id,))
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks

external_stylesheets = ['/static/styles.css']

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/tasks/",
    title="ChemINF-EDU - Tasks Maintenance",
    external_stylesheets=external_stylesheets
)

app.layout = html.Div(
    className="container",
    children=[
        # Home link at the top.
        html.Div(
            html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
            style={"textAlign": "right", "padding": "10px"}
        ),
        html.H1("Tasks Maintenance"),
        # Section to load tasks.
        html.Div(
            className="card",
            children=[
                html.Div([
                    html.Label("Project ID:"),
                    dcc.Input(
                        id="project-id-input",
                        type="number",
                        value=1,
                        min=1,
                        style={"color": "black"}
                    ),
                    html.Button("Load Tasks", id="load-tasks-btn")
                ]),
                html.Br(),
                dash_table.DataTable(
                    id="tasks-table",
                    columns=[
                        {"name": "ID", "id": "id"},
                        {"name": "Project ID", "id": "project_id"},
                        {"name": "Description", "id": "description"},
                        {"name": "Content", "id": "content"}
                    ],
                    data=[],
                    row_selectable="single",
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"color": "black"}  # Ensures the font color is black for all cells
                )
            ]
        ),
        html.Br(),
        # Maintenance section for task create/update/delete.
        html.Div(
            className="card",
            children=[
                html.H4("Task Maintenance"),
                html.Div([
                    html.Label("Task Description:"),
                    dcc.Input(
                        id="task-desc-input",
                        type="text",
                        placeholder="Enter task description",
                        style={"color": "black", "width": "100%"}
                    )
                ]),
                html.Br(),
                html.Div([
                    html.Label("Task Content:"),
                    dcc.Textarea(
                        id="task-content-input",
                        placeholder="Enter task content (JSON or text)",
                        style={"color": "black", "width": "100%"}
                    )
                ]),
                html.Br(),
                html.Div([
                    html.Button("Add Task", id="add-task-btn"),
                    html.Button("Update Task", id="update-task-btn"),
                    html.Button("Delete Task", id="delete-task-btn")
                ], style={"display": "flex", "gap": "10px"}),
                html.Br(),
                html.Div(id="task-msg", style={"color": "black"})
            ]
        )
    ]
)

# Combined callback to load tasks & handle add/update/delete.
@app.callback(
    Output("task-msg", "children"),
    Output("tasks-table", "data"),
    Input("load-tasks-btn", "n_clicks"),
    Input("add-task-btn", "n_clicks"),
    Input("update-task-btn", "n_clicks"),
    Input("delete-task-btn", "n_clicks"),
    State("project-id-input", "value"),
    State("task-desc-input", "value"),
    State("task-content-input", "value"),
    State("tasks-table", "selected_rows"),
    State("tasks-table", "data")
)
def update_tasks(load_n, add_n, update_n, delete_n, project_id, task_desc, task_content, selected_rows, current_tasks):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate

    project_id = int(project_id) if project_id else 1
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    msg = ""
    
    # If only loading tasks.
    if button_id == "load-tasks-btn":
        tasks = get_tasks_for_project(project_id)
        # Ensure each task has default keys.
        for task in tasks:
            task.setdefault("id", None)
            task.setdefault("project_id", None)
            task.setdefault("description", "")
            task.setdefault("content", "")
        return "", tasks

    # Otherwise, handle maintenance operations.
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if button_id == "add-task-btn":
            if not task_desc:
                msg = "Please provide a task description."
            else:
                cursor.execute(
                    f"INSERT INTO {TASK_TABLE} (project_id, description, content) VALUES (%s, %s, %s)",
                    (project_id, task_desc, task_content)
                )
                connection.commit()
                msg = f"Task '{task_desc}' added successfully."
        elif button_id == "update-task-btn":
            if not selected_rows:
                msg = "Please select a task to update."
            elif not task_desc:
                msg = "Please provide a new task description."
            else:
                row_index = selected_rows[0]
                task_id = current_tasks[row_index]["id"]
                cursor.execute(
                    f"UPDATE {TASK_TABLE} SET description = %s, content = %s WHERE id = %s",
                    (task_desc, task_content, task_id)
                )
                connection.commit()
                msg = f"Task ID {task_id} updated successfully."
        elif button_id == "delete-task-btn":
            if not selected_rows:
                msg = "Please select a task to delete."
            else:
                row_index = selected_rows[0]
                task_id = current_tasks[row_index]["id"]
                cursor.execute(
                    f"DELETE FROM {TASK_TABLE} WHERE id = %s", (task_id,)
                )
                connection.commit()
                msg = f"Task ID {task_id} deleted successfully."
    except Exception as e:
        msg = f"Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()

    # Refresh tasks table after any operation.
    tasks = get_tasks_for_project(project_id)
    for task in tasks:
        task.setdefault("id", None)
        task.setdefault("project_id", None)
        task.setdefault("description", "")
        task.setdefault("content", "")
    return msg, tasks

if __name__ == "__main__":
    app.run_server(debug=True)