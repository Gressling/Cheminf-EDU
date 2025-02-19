from flask import request, jsonify
from cheminf.db.db import get_db_connection
from cheminf.config import DB_PREFIX, DB_NAME
from cheminf.app_server import server

# Construct full table names
PROJECT_TABLE = f"{DB_NAME}.{DB_PREFIX}project"
TASK_TABLE = f"{DB_NAME}.{DB_PREFIX}task"

# ---------- Projects Endpoints ----------

@server.route("/api/projects", methods=["GET"])
def api_get_projects():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {PROJECT_TABLE}")
        projects = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(projects)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/projects", methods=["POST"])
def api_create_project():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    project_name = data["name"]
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {PROJECT_TABLE} (name) VALUES (%s)", (project_name,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Project created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/projects/<int:id>", methods=["PUT"])
def api_update_project(id):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    project_name = data["name"]
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {PROJECT_TABLE} SET name = %s WHERE id = %s", (project_name, id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/projects/<int:id>", methods=["DELETE"])
def api_delete_project(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # Delete tasks first due to foreign key dependency
        cursor.execute(f"DELETE FROM {TASK_TABLE} WHERE project_id = %s", (id,))
        cursor.execute(f"DELETE FROM {PROJECT_TABLE} WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Project and associated tasks deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Tasks Endpoints ----------

@server.route("/api/projects/<int:project_id>/tasks", methods=["GET"])
def api_get_tasks(project_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {TASK_TABLE} WHERE project_id = %s", (project_id,))
        tasks = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/projects/<int:project_id>/tasks", methods=["POST"])
def api_create_task(project_id):
    data = request.get_json()
    if not data or "description" not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    description = data["description"]
    content = data.get("content", "")
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {TASK_TABLE} (project_id, description, content) VALUES (%s, %s, %s)",
                       (project_id, description, content))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Task created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/tasks/<int:id>", methods=["PUT"])
def api_update_task(id):
    data = request.get_json()
    if not data or "description" not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    description = data["description"]
    content = data.get("content", "")
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {TASK_TABLE} SET description = %s, content = %s WHERE id = %s",
                       (description, content, id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/tasks/<int:id>", methods=["DELETE"])
def api_delete_task(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {TASK_TABLE} WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500