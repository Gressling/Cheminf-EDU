from flask import request, jsonify
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX
from cheminf.app_server import server

# Build the table name with prefix
INVENTORY_TABLE = f"{DB_PREFIX}inventory"

# Define base API route as a constant
BASE_API = "/api/inventory"

@server.route(f'{BASE_API}', methods=['GET'])
def api_get_inventory():
    try:
        rows = execute_query(f"SELECT * FROM {INVENTORY_TABLE}")
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
    unit = data.get('unit', 'ml')  # Default unit
    
    try:
        execute_query(
            f"INSERT INTO {INVENTORY_TABLE} (MoleculeUpacName, amount, unit) VALUES (?, ?, ?)",
            (molecule_name, amount, unit)
        )
        return jsonify({"message": "Inventory item created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/<int:id>', methods=['PUT'])
def api_update_inventory(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request payload"}), 400
    
    molecule_name = data.get('MoleculeUpacName')
    amount = data.get('amount')
    unit = data.get('unit')
    
    try:
        execute_query(
            f"UPDATE {INVENTORY_TABLE} SET MoleculeUpacName = ?, amount = ?, unit = ? WHERE id = ?",
            (molecule_name, amount, unit, id)
        )
        return jsonify({"message": "Inventory item updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route(f'{BASE_API}/<int:id>', methods=['DELETE'])
def api_delete_inventory(id):
    try:
        execute_query(f"DELETE FROM {INVENTORY_TABLE} WHERE id = ?", (id,))
        return jsonify({"message": "Inventory item deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
