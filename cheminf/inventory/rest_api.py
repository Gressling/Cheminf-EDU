from flask import request, jsonify
from cheminf.db import get_db_connection, get_all_rows
from cheminf.config import DB_NAME, DB_PREFIX
from cheminf.app_server import server  # Use the published Flask server

# Build the full table name with database name and prefix
INVENTORY_TABLE = f"{DB_NAME}.{DB_PREFIX}inventory"

# Define base API route as a constant
BASE_API = "/api/inventory"

@server.route(f'{BASE_API}', methods=['GET'])
def api_get_inventory():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {INVENTORY_TABLE}")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}', methods=['POST'])
def api_create_inventory():
    data = request.get_json()
    if not data or 'MoleculeUpacName' not in data or 'amount' not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    molecule_name = data['MoleculeUpacName']
    amount = data['amount']
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {INVENTORY_TABLE} (MoleculeUpacName, amount) VALUES (%s, %s)", (molecule_name, amount))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Inventory entry created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/<int:id>', methods=['PUT'])
def api_update_inventory(id):
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    amount = data['amount']
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {INVENTORY_TABLE} SET amount = %s WHERE id = %s", (amount, id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Inventory entry updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/<int:id>', methods=['DELETE'])
def api_delete_inventory(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {INVENTORY_TABLE} WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Inventory entry deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/search', methods=['GET'])
def api_search_inventory():
    # Retrieve the 'q' query parameter to search for substrings in MoleculeUpacName.
    query = request.args.get('q', '')
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # Use a LIKE clause with the provided query.
        search_pattern = f"%{query}%"
        cursor.execute(f"SELECT * FROM {INVENTORY_TABLE} WHERE MoleculeUpacName LIKE %s", (search_pattern,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500