"""
Quick MySQL to SQLite converter for key files
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Create a temporary simplified inventory REST API."""
    
    # Create a simple inventory REST API that works with SQLite
    inventory_rest_content = '''from flask import request, jsonify
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
'''
    
    # Write the simplified inventory REST API
    with open('cheminf/inventory/rest_api.py', 'w') as f:
        f.write(inventory_rest_content)
    
    print("✓ Updated inventory/rest_api.py")
    
    # Create simplified versions of other problematic modules
    files_to_simplify = {
        'cheminf/projects/ui_projects.py': create_simple_projects_ui(),
        'cheminf/projects/ui_tasks.py': create_simple_tasks_ui(),
        'cheminf/projects/rest_api.py': create_simple_projects_rest(),
    }
    
    for filepath, content in files_to_simplify.items():
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Updated {filepath}")
    
    print("\n✅ Key files updated for SQLite compatibility!")
    print("Note: Some advanced features may be disabled until full migration is complete.")

def create_simple_projects_ui():
    return '''# Simplified Projects UI for SQLite
from dash import dcc, html
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/projects/",
                title="ChemINF-EDU - Projects",
                external_stylesheets=external_stylesheets)

def get_all_projects():
    try:
        return execute_query("SELECT * FROM cheminf3_project")
    except:
        return []

app.layout = html.Div([
    html.H1("Projects Module"),
    html.P("Projects functionality temporarily simplified for SQLite migration."),
    html.P("Database connection successful!" if get_all_projects() else "Database connection failed."),
    html.A("Back to Home", href="/", style={"color": "white"})
])
'''

def create_simple_tasks_ui():
    return '''# Simplified Tasks UI for SQLite
from dash import dcc, html
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/tasks/",
                title="ChemINF-EDU - Tasks",
                external_stylesheets=external_stylesheets)

def get_all_tasks():
    try:
        return execute_query("SELECT * FROM cheminf3_task")
    except:
        return []

app.layout = html.Div([
    html.H1("Tasks Module"),
    html.P("Tasks functionality temporarily simplified for SQLite migration."),
    html.P("Database connection successful!" if get_all_tasks() else "Database connection failed."),
    html.A("Back to Home", href="/", style={"color": "white"})
])
'''

def create_simple_projects_rest():
    return '''# Simplified Projects REST API for SQLite
from flask import request, jsonify
from cheminf.db.db import execute_query
from cheminf.app_server import server

@server.route('/api/projects', methods=['GET'])
def api_get_projects():
    try:
        rows = execute_query("SELECT * FROM cheminf3_project")
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    try:
        rows = execute_query("SELECT * FROM cheminf3_task")
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''

if __name__ == "__main__":
    main()