from flask import request, jsonify
from cheminf.db.db import execute_query
from cheminf.app_server import server
from cheminf.config import DB_PREFIX

# Projects API endpoints
@server.route('/api/projects', methods=['GET'])
def api_get_projects():
    """Get all projects"""
    try:
        rows = execute_query(f"SELECT * FROM {DB_PREFIX}project ORDER BY id")
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/projects', methods=['POST'])
def api_create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Project name is required"}), 400
        
        execute_query(f"INSERT INTO {DB_PREFIX}project (name) VALUES (?)", (data['name'],))
        return jsonify({"message": "Project created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/projects/<int:project_id>', methods=['PUT'])
def api_update_project(project_id):
    """Update a project"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Project name is required"}), 400
        
        execute_query(f"UPDATE {DB_PREFIX}project SET name = ? WHERE id = ?", 
                     (data['name'], project_id))
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/projects/<int:project_id>', methods=['DELETE'])
def api_delete_project(project_id):
    """Delete a project"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}project WHERE id = ?", (project_id,))
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tasks API endpoints
@server.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """Get all tasks with project information"""
    try:
        query = f"""
        SELECT t.id, t.description, t.content, t.project_id, p.name as project_name
        FROM {DB_PREFIX}task t
        JOIN {DB_PREFIX}project p ON t.project_id = p.id
        ORDER BY t.id
        """
        rows = execute_query(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/tasks', methods=['POST'])
def api_create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        if not data or 'project_id' not in data or 'description' not in data:
            return jsonify({"error": "Project ID and description are required"}), 400
        
        execute_query(
            f"INSERT INTO {DB_PREFIX}task (project_id, description, content) VALUES (?, ?, ?)",
            (data['project_id'], data['description'], data.get('content', ''))
        )
        return jsonify({"message": "Task created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """Update a task"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400
        
        execute_query(
            f"UPDATE {DB_PREFIX}task SET project_id = ?, description = ?, content = ? WHERE id = ?",
            (data.get('project_id'), data.get('description'), data.get('content'), task_id)
        )
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """Delete a task"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}task WHERE id = ?", (task_id,))
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/projects/<int:project_id>/tasks', methods=['GET'])
def api_get_project_tasks(project_id):
    """Get all tasks for a specific project"""
    try:
        query = f"""
        SELECT t.id, t.description, t.content, t.project_id, p.name as project_name
        FROM {DB_PREFIX}task t
        JOIN {DB_PREFIX}project p ON t.project_id = p.id
        WHERE t.project_id = ?
        ORDER BY t.id
        """
        rows = execute_query(query, (project_id,))
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
