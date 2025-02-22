from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Construct the full table name for reactions.
REACTION_TABLE = f"{DB_NAME}.{DB_PREFIX}reactions"

def get_all_reactions():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {REACTION_TABLE}")
    reactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return reactions

external_stylesheets = ['/static/styles.css']

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/reactions/",
    title="ChemINF-EDU - Reactions Maintenance",
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
        html.H1("Reactions Maintenance"),
        html.Div(
            className="card",
            children=[
                # Panel to create a new reaction.
                html.Div([
                    dcc.Input(
                        id="reaction-name-input",
                        type="text",
                        placeholder="Enter reaction name",
                        style={"color": "black"}
                    ),
                    dcc.Input(
                        id="reaction-description-input",
                        type="text",
                        placeholder="Enter reaction description",
                        style={"color": "black", "width": "100%"}
                    ),
                    html.Button("Add Reaction", id="add-reaction-btn"),
                    html.Div(id="reaction-add-msg")
                ]),
                html.Br(),
                dash_table.DataTable(
                    id="reactions-table",
                    columns=[
                        {"name": "Reaction ID", "id": "ReactionID"},
                        {"name": "Name", "id": "ReactionName"},
                        {"name": "Description", "id": "ReactionDescription"}
                    ],
                    data=get_all_reactions(),
                    row_selectable='single',
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"color": "black"}
                ),
                html.Br(),
                # Panel to update or delete a selected reaction.
                html.Div([
                    html.Button("Delete Selected", id="delete-reaction-btn"),
                    dcc.Input(
                        id="update-reaction-name",
                        type="text",
                        placeholder="New reaction name",
                        style={"color": "black"}
                    ),
                    dcc.Input(
                        id="update-reaction-description",
                        type="text",
                        placeholder="New reaction description",
                        style={"color": "black", "width": "100%"}
                    ),
                    html.Button("Update Selected", id="update-reaction-btn"),
                    html.Div(id="reaction-update-delete-msg")
                ])
            ]
        )
    ]
)

@app.callback(
    Output("reaction-add-msg", "children"),
    Output("reaction-update-delete-msg", "children"),
    Output("reactions-table", "data"),
    Input("add-reaction-btn", "n_clicks"),
    Input("delete-reaction-btn", "n_clicks"),
    Input("update-reaction-btn", "n_clicks"),
    State("reaction-name-input", "value"),
    State("reaction-description-input", "value"),
    State("update-reaction-name", "value"),
    State("update-reaction-description", "value"),
    State("reactions-table", "selected_rows"),
    State("reactions-table", "data")
)
def manage_reaction(add_clicks, delete_clicks, update_clicks,
                    new_name, new_description, update_name, update_description,
                    selected_rows, current_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    add_msg = ""
    update_delete_msg = ""
    try:
        if button_id == "add-reaction-btn":
            if not new_name:
                add_msg = "Please provide a reaction name."
            else:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    f"INSERT INTO {REACTION_TABLE} (ReactionName, ReactionDescription) VALUES (%s, %s)",
                    (new_name, new_description)
                )
                connection.commit()
                cursor.close()
                connection.close()
                add_msg = f"Reaction '{new_name}' added successfully."
        elif button_id == "delete-reaction-btn":
            if not selected_rows:
                update_delete_msg = "Please select a reaction to delete."
            else:
                row_index = selected_rows[0]
                reaction_id = current_data[row_index]["ReactionID"]
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM {REACTION_TABLE} WHERE ReactionID = %s", (reaction_id,))
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Deleted reaction with ID: {reaction_id}"
        elif button_id == "update-reaction-btn":
            if not selected_rows:
                update_delete_msg = "Please select a reaction to update."
            elif not update_name:
                update_delete_msg = "Please provide a new reaction name."
            else:
                row_index = selected_rows[0]
                reaction_id = current_data[row_index]["ReactionID"]
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    f"UPDATE {REACTION_TABLE} SET ReactionName = %s, ReactionDescription = %s WHERE ReactionID = %s",
                    (update_name, update_description, reaction_id)
                )
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Updated reaction ID {reaction_id} successfully."
    except Exception as e:
        if button_id == "add-reaction-btn":
            add_msg = f"Error: {str(e)}"
        else:
            update_delete_msg = f"Error: {str(e)}"
    updated_data = get_all_reactions()
    return add_msg, update_delete_msg, updated_data

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)