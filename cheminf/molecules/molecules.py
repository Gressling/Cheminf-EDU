import dash
from dash import dcc, html, Input, Output, State, dash_table, exceptions
from flask import Flask, request, jsonify

# Import database functions from our SQLite module
from ..db.db import get_db_connection, execute_query

# Define the table name using the prefix.
TABLE_NAME = "cheminf3_molecules"

# -------------------------------
# Database functions
# -------------------------------

def get_all_rows():
    """Retrieve all rows from the molecules table."""
    return execute_query(f"SELECT * FROM {TABLE_NAME}")

def insert_molecule(molecule_name):
    """Insert a new molecule."""
    return execute_query(
        f"INSERT INTO {TABLE_NAME} (MoleculeUpacName) VALUES (?)", 
        (molecule_name,)
    )

def update_molecule(molecule_id, molecule_name):
    """Update an existing molecule."""
    return execute_query(
        f"UPDATE {TABLE_NAME} SET MoleculeUpacName = ? WHERE id = ?", 
        (molecule_name, molecule_id)
    )

def delete_molecule(molecule_id):
    """Delete a molecule by ID."""
    return execute_query(
        f"DELETE FROM {TABLE_NAME} WHERE id = ?", 
        (molecule_id,)
    )

# -------------------------------
# Create Flask server and Dash app
# -------------------------------

server = Flask(__name__)
app = dash.Dash(__name__, server=server, title="ChemINF-EDU")

# -------------------------------
# Dash app layout
# -------------------------------

app.layout = html.Div([
    html.H1("ChemINF-EDU"),
    
    # Insertion area
    html.Div([
        dcc.Input(id='input-name', type='text', placeholder='Enter Molecule UPAC Name'),
        html.Button('Insert', id='insert-btn'),
        html.Div(id='insert-output')
    ]),
    
    html.Hr(),
    
    # Data table with selectable rows (for delete/update)
    dash_table.DataTable(
        id='data-table',
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "MoleculeUpacName", "id": "MoleculeUpacName"}
        ],
        data=get_all_rows(),
        row_selectable='single',
        selected_rows=[]
    ),
    
    html.Br(),
    
    # Delete and update controls
    html.Div([
        html.Button('Delete Selected', id='delete-btn'),
        dcc.Input(id='update-name', type='text', placeholder='New Molecule UPAC Name'),
        html.Button('Update Selected', id='update-btn'),
        html.Div(id='update-delete-output')
    ])
])

# -------------------------------
# Combined callback to manage insert, delete, and update
# -------------------------------

@app.callback(
    Output('insert-output', 'children'),
    Output('update-delete-output', 'children'),
    Output('data-table', 'data'),
    Input('insert-btn', 'n_clicks'),
    Input('delete-btn', 'n_clicks'),
    Input('update-btn', 'n_clicks'),
    State('input-name', 'value'),
    State('data-table', 'selected_rows'),
    State('data-table', 'data'),
    State('update-name', 'value')
)
def manage_molecule(insert_clicks, delete_clicks, update_clicks, input_name, selected_rows, current_data, update_name):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Initialize message variables
    insert_msg = ''
    update_delete_msg = ''
    
    if button_id == 'insert-btn':
        if not input_name:
            insert_msg = "Please provide a molecule name."
        else:
            try:
                insert_molecule(input_name)
                insert_msg = f"Inserted: {input_name}"
            except Exception as e:
                insert_msg = f"Error inserting: {str(e)}"
    elif button_id == 'delete-btn':
        if not selected_rows:
            update_delete_msg = "Please select a row to delete."
        else:
            try:
                # Use the selected row index to retrieve the corresponding row from current_data
                row_index = selected_rows[0]
                selected_row = current_data[row_index]
                id_to_delete = selected_row['id']
                
                delete_molecule(id_to_delete)
                update_delete_msg = f"Deleted row with ID: {id_to_delete}"
            except Exception as e:
                update_delete_msg = f"Error deleting: {str(e)}"
    elif button_id == 'update-btn':
        if not selected_rows:
            update_delete_msg = "Please select a row to update."
        elif not update_name:
            update_delete_msg = "Please provide a new name for update."
        else:
            try:
                row_index = selected_rows[0]
                selected_row = current_data[row_index]
                id_to_update = selected_row['id']
                
                update_molecule(id_to_update, update_name)
                update_delete_msg = f"Updated row with ID: {id_to_update} to {update_name}"
            except Exception as e:
                update_delete_msg = f"Error updating: {str(e)}"
    
    # Fetch the updated data regardless of which operation occurred
    updated_data = get_all_rows()
    return insert_msg, update_delete_msg, updated_data

# -------------------------------
# REST API endpoints using Flask routes
# -------------------------------

@server.route('/api/molecules', methods=['GET'])
def api_get_molecules():
    try:
        rows = get_all_rows()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/molecules', methods=['POST'])
def api_create_molecule():
    data = request.get_json()
    if not data or 'MoleculeUpacName' not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    molecule_name = data['MoleculeUpacName']
    try:
        insert_molecule(molecule_name)
        return jsonify({"message": "Molecule created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/molecules/<int:id>', methods=['PUT'])
def api_update_molecule(id):
    data = request.get_json()
    if not data or 'MoleculeUpacName' not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    molecule_name = data['MoleculeUpacName']
    try:
        update_molecule(id, molecule_name)
        return jsonify({"message": "Molecule updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/molecules/<int:id>', methods=['DELETE'])
def api_delete_molecule(id):
    try:
        delete_molecule(id)
        return jsonify({"message": "Molecule deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Main entry point
# -------------------------------

if __name__ == '__main__':
    app.run(debug=True)
