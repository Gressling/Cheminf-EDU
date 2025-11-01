# Simplified Projects REST API for SQLite
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
