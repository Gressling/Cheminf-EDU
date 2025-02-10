from flask import request, jsonify
from cheminf.db import get_db_connection, get_all_rows
from cheminf.config import DB_NAME, DB_PREFIX
from cheminf.app_server import server  # Use the published Flask server

# Build the full table name with database name and prefix
TABLE_NAME = f"{DB_NAME}.{DB_PREFIX}molecules"

# Define base API route as a constant
BASE_API = "/api/molecules"

@server.route(f'{BASE_API}', methods=['GET'])
def api_get_molecules():
    try:
        rows = get_all_rows()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}', methods=['POST'])
def api_create_molecule():
    data = request.get_json()
    if not data or 'MoleculeUpacName' not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    molecule_name = data['MoleculeUpacName']
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {TABLE_NAME} (MoleculeUpacName) VALUES (%s)", (molecule_name,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Molecule created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/<int:id>', methods=['PUT'])
def api_update_molecule(id):
    data = request.get_json()
    if not data or 'MoleculeUpacName' not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    molecule_name = data['MoleculeUpacName']
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {TABLE_NAME} SET MoleculeUpacName = %s WHERE id = %s", (molecule_name, id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Molecule updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/<int:id>', methods=['DELETE'])
def api_delete_molecule(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Molecule deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    server.run(debug=True)