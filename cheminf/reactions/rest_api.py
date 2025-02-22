from flask import request, jsonify
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX
from cheminf.app_server import server

# Construct full table name for reaction participants.
REACTIONPARTICIPANTS_TABLE = f"{DB_NAME}.{DB_PREFIX}reactionparticipants"

# ---------- Reaction Participants Endpoints ----------

@server.route("/api/reactions/<int:reaction_id>/participants", methods=["GET"])
def api_get_reactionparticipants(reaction_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {REACTIONPARTICIPANTS_TABLE} WHERE ReactionID = %s"
        cursor.execute(query, (reaction_id,))
        participants = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(participants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/reactions/<int:reaction_id>/participants", methods=["POST"])
def api_create_reactionparticipant(reaction_id):
    data = request.get_json()
    if not data or "molecule_id" not in data or "role" not in data or "stoichiometric_coefficient" not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    molecule_id = data["molecule_id"]
    role = data["role"]
    stoich = data["stoichiometric_coefficient"]
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"INSERT INTO {REACTIONPARTICIPANTS_TABLE} (ReactionID, MoleculeID, Role, StoichiometricCoefficient) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (reaction_id, molecule_id, role, stoich))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Reaction participant created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/participants/<int:reaction_id>/<int:molecule_id>/<role>", methods=["PUT"])
def api_update_reactionparticipant(reaction_id, molecule_id, role):
    data = request.get_json()
    if not data or "stoichiometric_coefficient" not in data:
        return jsonify({"error": "Invalid request payload"}), 400
    stoich = data["stoichiometric_coefficient"]
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"UPDATE {REACTIONPARTICIPANTS_TABLE} SET StoichiometricCoefficient = %s WHERE ReactionID = %s AND MoleculeID = %s AND Role = %s"
        cursor.execute(query, (stoich, reaction_id, molecule_id, role))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Reaction participant updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/participants/<int:reaction_id>/<int:molecule_id>/<role>", methods=["DELETE"])
def api_delete_reactionparticipant(reaction_id, molecule_id, role):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"DELETE FROM {REACTIONPARTICIPANTS_TABLE} WHERE ReactionID = %s AND MoleculeID = %s AND Role = %s"
        cursor.execute(query, (reaction_id, molecule_id, role))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Reaction participant deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500