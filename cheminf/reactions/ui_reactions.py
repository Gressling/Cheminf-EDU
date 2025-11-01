from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Construct the full table name for reactions.
REACTION_TABLE = f"{DB_NAME}.{DB_PREFIX}reactions"

def get_all_reactions():
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

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
def manage_reaction(add_clicks, delete_clicks, update_clicks, add_name, add_description, update_name, update_description, selected_rows, table_data):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)