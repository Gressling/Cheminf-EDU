from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Construct the full table name for reaction participants.
REACTIONPARTICIPANTS_TABLE = f"{DB_NAME}.{DB_PREFIX}reactionparticipants"

# Helper function to fetch reaction participants for a given ReactionID.
def get_reaction_participants(reaction_id):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

external_stylesheets = ['/static/styles.css']

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/reactions/participants/",
    title="ChemINF-EDU - Reaction Participants Maintenance",
    external_stylesheets=external_stylesheets
)

app.layout = html.Div(
    className="container",
    children=[
        # Home link
        html.Div(
            html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
            style={"textAlign": "right", "padding": "10px"}
        ),
        html.H1("Reaction Participants Maintenance"),
        # Section to load reaction participants.
        html.Div(
            className="card",
            children=[
                html.Div([
                    html.Label("Reaction ID:"),
                    dcc.Input(
                        id="reaction-id-input",
                        type="number",
                        value=1,
                        min=1,
                        style={"color": "black"}
                    ),
                    html.Button("Load Participants", id="load-participants-btn")
                ]),
                html.Br(),
                dash_table.DataTable(
                    id="participants-table",
                    columns=[
                        {"name": "Reaction ID", "id": "ReactionID"},
                        {"name": "Molecule ID", "id": "MoleculeID"},
                        {"name": "Role", "id": "Role"},
                        {"name": "Stoichiometric Coefficient", "id": "StoichiometricCoefficient"}
                    ],
                    data=[],
                    row_selectable="single",
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"color": "black"}
                )
            ]
        ),
        html.Br(),
        # Maintenance section for reaction participant create/update/delete.
        html.Div(
            className="card",
            children=[
                html.H4("Reaction Participant Maintenance"),
                html.Div([
                    html.Label("Molecule ID:"),
                    dcc.Input(
                        id="molecule-id-input",
                        type="number",
                        placeholder="Enter Molecule ID",
                        style={"color": "black", "width": "100%"}
                    )
                ]),
                html.Br(),
                html.Div([
                    html.Label("Role:"),
                    dcc.Input(
                        id="role-input",
                        type="text",
                        placeholder="Enter role (reactant, product, catalyst, etc.)",
                        style={"color": "black", "width": "100%"}
                    )
                ]),
                html.Br(),
                html.Div([
                    html.Label("Stoichiometric Coefficient:"),
                    dcc.Input(
                        id="stoich-input",
                        type="number",
                        placeholder="Enter coefficient",
                        step=0.001,
                        style={"color": "black", "width": "100%"}
                    )
                ]),
                html.Br(),
                html.Div([
                    html.Button("Add Participant", id="add-participant-btn"),
                    html.Button("Update Participant", id="update-participant-btn"),
                    html.Button("Delete Participant", id="delete-participant-btn")
                ], style={"display": "flex", "gap": "10px"}),
                html.Br(),
                html.Div(id="participant-msg", style={"color": "black"})
            ]
        )
    ]
)

# Combined callback to load and maintain reaction participants.
@app.callback(
    Output("participant-msg", "children"),
    Output("participants-table", "data"),
    Input("load-participants-btn", "n_clicks"),
    Input("add-participant-btn", "n_clicks"),
    Input("update-participant-btn", "n_clicks"),
    Input("delete-participant-btn", "n_clicks"),
    State("reaction-id-input", "value"),
    State("molecule-id-input", "value"),
    State("role-input", "value"),
    State("stoich-input", "value"),
    State("participants-table", "selected_rows"),
    State("participants-table", "data")
)
def update_participants(load_n, add_n, update_n, delete_n, reaction_id, molecule_id, role, stoich, *args, **kwargs):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

    reaction_id = int(reaction_id) if reaction_id else 1
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    msg = ""
    
    # If only loading participants.
    if button_id == "load-participants-btn":
        participants = get_reaction_participants(reaction_id)
        return "", participants

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if button_id == "add-participant-btn":
            if not molecule_id or not role or stoich is None:
                msg = "Please provide Molecule ID, Role, and Stoichiometric Coefficient."
            else:
                cursor.execute(
                    f"INSERT INTO {REACTIONPARTICIPANTS_TABLE} (ReactionID, MoleculeID, Role, StoichiometricCoefficient) VALUES (%s, %s, %s, %s)",
                    (reaction_id, molecule_id, role, stoich)
                )
                connection.commit()
                msg = "Reaction participant added successfully."
        elif button_id == "update-participant-btn":
            if not selected_rows:
                msg = "Please select a participant to update."
            elif not molecule_id or not role or stoich is None:
                msg = "Please provide updated Molecule ID, Role, and Stoichiometric Coefficient."
            else:
                row_index = selected_rows[0]
                orig = current_data[row_index]
                # Update based on composite key (ReactionID, MoleculeID, Role)
                cursor.execute(
                    f"UPDATE {REACTIONPARTICIPANTS_TABLE} SET MoleculeID = %s, Role = %s, StoichiometricCoefficient = %s WHERE ReactionID = %s AND MoleculeID = %s AND Role = %s",
                    (molecule_id, role, stoich, reaction_id, orig["MoleculeID"], orig["Role"])
                )
                connection.commit()
                msg = "Reaction participant updated successfully."
        elif button_id == "delete-participant-btn":
            if not selected_rows:
                msg = "Please select a participant to delete."
            else:
                row_index = selected_rows[0]
                orig = current_data[row_index]
                cursor.execute(
                    f"DELETE FROM {REACTIONPARTICIPANTS_TABLE} WHERE ReactionID = %s AND MoleculeID = %s AND Role = %s",
                    (reaction_id, orig["MoleculeID"], orig["Role"])
                )
                connection.commit()
                msg = "Reaction participant deleted successfully."
    except Exception as e:
        msg = f"Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()
    
    # Refresh table data after any operation.
    participants = get_reaction_participants(reaction_id)
    return msg, participants

if __name__ == "__main__":
    app.run_server(debug=True)