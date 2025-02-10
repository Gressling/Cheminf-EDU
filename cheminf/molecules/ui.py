from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
from cheminf.app_server import server  # Use the shared Flask server
from cheminf.db import get_all_rows, get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

# Import RDKit and required modules for image generation
from rdkit import Chem
from rdkit.Chem import Draw
import io
import base64

# Full table name
TABLE_NAME = f"{DB_NAME}.{DB_PREFIX}molecules"

# Use the shared CSS from /static
external_stylesheets = ['/static/styles.css']

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/molecules/",
    title="ChemINF-EDU - Molecules",
    external_stylesheets=external_stylesheets
)

def get_img_src(smiles):
    """
    Generate the base64 image src directly for html.Img.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return ""
    img = Draw.MolToImage(mol, size=(150, 150))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

app.layout = html.Div(
    className="container",
    children=[
        # Home link in white at the top right
        html.Div(
            html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
            style={"textAlign": "right", "padding": "10px"}
        ),
        html.H1("Molecules"),
        html.Div(
            className="card",
            children=[
                # Insert panel with inputs for name and SMILES
                dcc.Input(
                    id='input-name',
                    type='text',
                    placeholder='Enter Molecule UPAC Name',
                    style={"color": "black"}
                ),
                dcc.Input(
                    id='input-smiles',
                    type='text',
                    placeholder='Enter SMILES string',
                    style={"color": "black"}
                ),
                html.Button('Insert', id='insert-btn'),
                html.Div(id='insert-output'),
            ]
        ),
        html.Hr(),
        dash_table.DataTable(
            id='data-table',
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "MoleculeUpacName", "id": "MoleculeUpacName"},
                {"name": "SMILES", "id": "SMILES"}
            ],
            data=get_all_rows(),
            row_selectable='single',
            selected_rows=[],
            style_data={"color": "black"},
            style_data_conditional=[
                {"if": {"state": "selected"}, "color": "white"}
            ],
            style_table={
                "maxHeight": "300px",  # Approximately 10 rows visible
                "overflowY": "scroll"
            }
        ),
        # Div to display the molecule image for the selected row
        html.Div(id='image-display', style={"padding": "20px", "textAlign": "center"}),
        html.Br(),
        html.Div(
            className="card",
            children=[
                html.Button('Delete Selected', id='delete-btn'),
                dcc.Input(
                    id='update-name',
                    type='text',
                    placeholder='New Molecule UPAC Name',
                    style={"color": "black"}
                ),
                dcc.Input(
                    id='update-smiles',
                    type='text',
                    placeholder='New SMILES string',
                    style={"color": "black"}
                ),
                html.Button('Update Selected', id='update-btn'),
                html.Div(id='update-delete-output')
            ]
        )
    ]
)

@app.callback(
    Output('insert-output', 'children'),
    Output('update-delete-output', 'children'),
    Output('data-table', 'data'),
    Input('insert-btn', 'n_clicks'),
    Input('delete-btn', 'n_clicks'),
    Input('update-btn', 'n_clicks'),
    State('input-name', 'value'),
    State('input-smiles', 'value'),
    State('data-table', 'selected_rows'),
    State('data-table', 'data'),
    State('update-name', 'value'),
    State('update-smiles', 'value')
)
def manage_molecule(insert_clicks, delete_clicks, update_clicks,
                    input_name, input_smiles, selected_rows, current_data, update_name, update_smiles):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    insert_msg = ''
    update_delete_msg = ''

    if button_id == 'insert-btn':
        if not input_name or not input_smiles:
            insert_msg = "Please provide both a molecule name and a SMILES string."
        else:
            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (MoleculeUpacName, SMILES) VALUES (%s, %s)",
                    (input_name, input_smiles)
                )
                connection.commit()
                cursor.close()
                connection.close()
                insert_msg = f"Inserted: {input_name} with SMILES {input_smiles}"
            except Exception as e:
                insert_msg = f"Error inserting: {str(e)}"
    elif button_id == 'delete-btn':
        if not selected_rows:
            update_delete_msg = "Please select a row to delete."
        else:
            try:
                row_index = selected_rows[0]
                selected_row = current_data[row_index]
                id_to_delete = selected_row['id']

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (id_to_delete,))
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Deleted row with ID: {id_to_delete}"
            except Exception as e:
                update_delete_msg = f"Error deleting: {str(e)}"
    elif button_id == 'update-btn':
        if not selected_rows:
            update_delete_msg = "Please select a row to update."
        elif not update_name or not update_smiles:
            update_delete_msg = "Please provide both a new name and a new SMILES string for update."
        else:
            try:
                row_index = selected_rows[0]
                selected_row = current_data[row_index]
                id_to_update = selected_row['id']

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    f"UPDATE {TABLE_NAME} SET MoleculeUpacName = %s, SMILES = %s WHERE id = %s",
                    (update_name, update_smiles, id_to_update)
                )
                connection.commit()
                cursor.close()
                connection.close()
                update_delete_msg = f"Updated row with ID: {id_to_update} to {update_name} and SMILES {update_smiles}"
            except Exception as e:
                update_delete_msg = f"Error updating: {str(e)}"

    updated_data = get_all_rows()
    return insert_msg, update_delete_msg, updated_data

# Callback to display the image from the selected row using html.Img
@app.callback(
    Output('image-display', 'children'),
    Input('data-table', 'selected_rows'),
    State('data-table', 'data')
)
def display_image(selected_rows, data):
    if not selected_rows:
        return "Select a row to display its molecule image."
    row = data[selected_rows[0]]
    smiles = row.get("SMILES", "")
    if not smiles:
        return "No SMILES available."
    return html.Img(src=get_img_src(smiles), style={"width": "150px"})

if __name__ == '__main__':
    app.run_server(debug=True)
