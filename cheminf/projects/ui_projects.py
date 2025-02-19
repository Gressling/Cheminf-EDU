from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Construct the full table name for projects.
PROJECT_TABLE = f"{DB_NAME}.{DB_PREFIX}project"

external_stylesheets = ['/static/styles.css']

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/projects/",
    title="ChemINF-EDU - Projects Maintenance",
    external_stylesheets=external_stylesheets
)

def get_all_projects():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {PROJECT_TABLE}")
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return projects

app.layout = html.Div(
    className="container",
    children=[
        html.Div(
            html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
            style={"textAlign": "right", "padding": "10px"}
        ),
        html.H1("Projects Maintenance"),
        html.Div(
            className="card",
            children=[
                # Card with Add Project functionality
                html.Div([
                    dcc.Input(
                        id='project-name-input',
                        type='text',
                        placeholder='Enter project name',
                        style={"color": "black"}
                    ),
                    html.Button("Add Project", id='add-project-btn'),
                    html.Div(id='project-add-msg')
                ]),
                html.Br(),
                dash_table.DataTable(
                    id='projects-table',
                    columns=[
                        {"name": "ID", "id": "id"},
                        {"name": "Name", "id": "name"}
                    ],
                    data=get_all_projects(),
                    row_selectable='single',
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"color": "black"}  # Ensures the font color is black for all cells
                ),
                html.Br(),
                # Card with Delete/Update functionality
                html.Div([
                    html.Button("Delete Selected", id="delete-project-btn"),
                    dcc.Input(
                        id="update-project-name",
                        type="text",
                        placeholder="New project name",
                        style={"color": "black"}
                    ),
                    html.Button("Update Selected", id="update-project-btn"),
                    html.Div(id="project-update-delete-msg")
                ])
            ]
        )
    ]
)

@app.callback(
    Output('project-add-msg', 'children'),
    Output('project-update-delete-msg', 'children'),
    Output('projects-table', 'data'),
    Input('add-project-btn', 'n_clicks'),
    Input('delete-project-btn', 'n_clicks'),
    Input('update-project-btn', 'n_clicks'),
    State('project-name-input', 'value'),
    State('update-project-name', 'value'),
    State('projects-table', 'selected_rows'),
    State('projects-table', 'data')
)
def manage_project(add_clicks, delete_clicks, update_clicks, new_project_name, update_project_name, selected_rows, current_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    add_msg = ""
    update_delete_msg = ""

    try:
        if button_id == 'add-project-btn':
            if not new_project_name:
                add_msg = "Please provide a project name."
            else:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO {PROJECT_TABLE} (name) VALUES (%s)", (new_project_name,))
                connection.commit()
                cursor.close()
                connection.close()
                add_msg = f"Project '{new_project_name}' added successfully."
        elif button_id == 'delete-project-btn':
            if not selected_rows:
                update_delete_msg = "Please select a project to delete."
            else:
                row_index = selected_rows[0]
                id_to_delete = current_data[row_index]['id']
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM {PROJECT_TABLE} WHERE id = %s", (id_to_delete,))
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Deleted project with ID: {id_to_delete}"
        elif button_id == 'update-project-btn':
            if not selected_rows:
                update_delete_msg = "Please select a project to update."
            elif not update_project_name:
                update_delete_msg = "Please provide a new project name for update."
            else:
                row_index = selected_rows[0]
                id_to_update = current_data[row_index]['id']
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(f"UPDATE {PROJECT_TABLE} SET name = %s WHERE id = %s", (update_project_name, id_to_update))
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Updated project with ID {id_to_update} to '{update_project_name}'"
    except Exception as e:
        if button_id == 'add-project-btn':
            add_msg = f"Error: {str(e)}"
        else:
            update_delete_msg = f"Error: {str(e)}"
    
    updated_data = get_all_projects()
    return add_msg, update_delete_msg, updated_data

if __name__ == '__main__':
    app.run_server(debug=True)