from dash import dcc, html, Input, Output, State, exceptions, dash_table
import dash
from cheminf.app_server import server
from cheminf.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Build table name for inventory data
INVENTORY_TABLE = f"{DB_NAME}.{DB_PREFIX}inventory"

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/inventory/",
                title="ChemINF-EDU - Inventory",
                external_stylesheets=external_stylesheets)

# Helper function to fetch all inventory rows
def get_all_inventory():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {INVENTORY_TABLE}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

app.layout = html.Div(
    className="container",
    children=[
        # Home link in white at the top right
        html.Div(
            html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
            style={"textAlign": "right", "padding": "10px"}
        ),
        html.H1("Inventory"),
        html.Div(
            className="card",
            children=[
                html.H3("Check Inventory"),
                dcc.Input(
                    id='inventory-molecule',
                    type='text',
                    placeholder='Enter Molecule Name for Inventory',
                    style={"color": "black"}  # Added style for better text readability
                ),
                html.Button('Check Inventory', id='inventory-btn'),
                html.Div(id='inventory-output')
            ]
        ),
        html.Hr(),
        html.Div(
            className="card",
            children=[
                html.H3("Add New Inventory Entry"),
                dcc.Input(
                    id='inventory-input-name',
                    type='text',
                    placeholder='Enter Molecule UPAC Name',
                    style={"color": "black"}
                ),
                dcc.Input(
                    id='inventory-input-amount',
                    type='number',
                    placeholder='Enter Amount',
                    style={"color": "black"}
                ),
                dcc.Input(
                    id='inventory-input-unit',
                    type='text',
                    placeholder='Enter Unit (e.g., ml)',
                    style={"color": "black"}
                ),
                html.Button('Insert', id='inventory-insert-btn'),
                html.Div(id='inventory-insert-output')
            ]
        ),
        html.Br(),
        dash_table.DataTable(
            id='inventory-table',
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "MoleculeUpacName", "id": "MoleculeUpacName"},
                {"name": "Amount", "id": "amount"},
                {"name": "Unit", "id": "unit"}
            ],
            data=get_all_inventory(),
            row_selectable='single',
            selected_rows=[],
            style_data={"color": "black"},
            style_data_conditional=[
                {
                    "if": {"state": "selected"},
                    "color": "white"
                }
            ],
            style_table={
                "maxHeight": "300px",  # Approximately 10 rows visible
                "overflowY": "scroll"
            }
        ),
        html.Br(),
        html.Div(
            className="card",
            children=[
                html.Button('Delete Selected', id='inventory-delete-btn'),
                dcc.Input(
                    id='inventory-update-name',
                    type='text',
                    placeholder='New Molecule UPAC Name',
                    style={"color": "black"}
                ),
                dcc.Input(
                    id='inventory-update-amount',
                    type='number',
                    placeholder='New Amount',
                    style={"color": "black"}
                ),
                dcc.Input(
                    id='inventory-update-unit',
                    type='text',
                    placeholder='New Unit (e.g., ml)',
                    style={"color": "black"}
                ),
                html.Button('Update Selected', id='inventory-update-btn'),
                html.Div(id='inventory-update-delete-output')
            ]
        )
    ]
)

@app.callback(
    Output('inventory-insert-output', 'children'),
    Output('inventory-update-delete-output', 'children'),
    Output('inventory-table', 'data'),
    Input('inventory-insert-btn', 'n_clicks'),
    Input('inventory-delete-btn', 'n_clicks'),
    Input('inventory-update-btn', 'n_clicks'),
    State('inventory-input-name', 'value'),
    State('inventory-input-amount', 'value'),
    State('inventory-input-unit', 'value'),
    State('inventory-table', 'selected_rows'),
    State('inventory-table', 'data'),
    State('inventory-update-name', 'value'),
    State('inventory-update-amount', 'value'),
    State('inventory-update-unit', 'value')
)
def manage_inventory(insert_clicks, delete_clicks, update_clicks,
                     input_name, input_amount, input_unit,
                     selected_rows, current_data, update_name, update_amount, update_unit):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    insert_msg = ''
    update_delete_msg = ''

    if button_id == 'inventory-insert-btn':
        if not input_name or input_amount is None or not input_unit:
            insert_msg = "Please provide molecule name, amount, and unit."
        else:
            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    f"INSERT INTO {INVENTORY_TABLE} (MoleculeUpacName, amount, unit) VALUES (%s, %s, %s)",
                    (input_name, input_amount, input_unit)
                )
                connection.commit()
                cursor.close()
                connection.close()
                insert_msg = f"Inserted: {input_name} with amount {input_amount} {input_unit}"
            except Exception as e:
                insert_msg = f"Error inserting: {str(e)}"
    elif button_id == 'inventory-delete-btn':
        if not selected_rows:
            update_delete_msg = "Please select a row to delete."
        else:
            try:
                row_index = selected_rows[0]
                selected_row = current_data[row_index]
                id_to_delete = selected_row['id']
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM {INVENTORY_TABLE} WHERE id = %s", (id_to_delete,))
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Deleted row with ID: {id_to_delete}"
            except Exception as e:
                update_delete_msg = f"Error deleting: {str(e)}"
    elif button_id == 'inventory-update-btn':
        if not selected_rows:
            update_delete_msg = "Please select a row to update."
        elif not update_name or update_amount is None or not update_unit:
            update_delete_msg = "Please provide a new name, amount, and unit for update."
        else:
            try:
                row_index = selected_rows[0]
                selected_row = current_data[row_index]
                id_to_update = selected_row['id']
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    f"UPDATE {INVENTORY_TABLE} SET MoleculeUpacName = %s, amount = %s, unit = %s WHERE id = %s",
                    (update_name, update_amount, update_unit, id_to_update)
                )
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Updated row ID {id_to_update} to {update_name} with amount {update_amount} {update_unit}"
            except Exception as e:
                update_delete_msg = f"Error updating: {str(e)}"

    updated_data = get_all_inventory()
    return insert_msg, update_delete_msg, updated_data

@app.callback(
    Output('inventory-output', 'children'),
    Input('inventory-btn', 'n_clicks'),
    State('inventory-molecule', 'value')
)
def check_inventory(n_clicks, molecule_name):
    if not n_clicks or not molecule_name:
        raise exceptions.PreventUpdate
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT amount, unit FROM {INVENTORY_TABLE} WHERE MoleculeUpacName = %s", (molecule_name,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row:
            return f"Available stock for {molecule_name}: {row['amount']} {row['unit']}"
        else:
            return "Molecule not found in inventory."
    except Exception as e:
        return f"Error retrieving inventory: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)
