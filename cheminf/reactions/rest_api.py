from flask import request, jsonify
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX
from cheminf.app_server import server

# Construct full table names (if needed)
REACTIONS_TABLE = f"{DB_NAME}.{DB_PREFIX}reactions"
REACTIONPARTICIPANTS_TABLE = f"{DB_NAME}.{DB_PREFIX}reactionparticipants"
MOLECULES_TABLE = f"{DB_NAME}.{DB_PREFIX}molecules"

@server.route("/api/reactions", methods=["GET"])
def api_get_reactions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM {REACTIONS_TABLE}"
        cursor.execute(query)
        reactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(reactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@server.route("/api/reactions/overview/<int:reaction_id>", methods=["GET"])
def api_reaction_overview(reaction_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"""
        SELECT 
          r.ReactionName,
          r.ReactionDescription,
          CONCAT(
            'Reactants: ', GROUP_CONCAT(CASE WHEN rp.Role = 'reactant' 
                                              THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                              END SEPARATOR ' + '),
            ' | Products: ', GROUP_CONCAT(CASE WHEN rp.Role = 'product' 
                                              THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                              END SEPARATOR ' + '),
            ' | Catalysts: ', GROUP_CONCAT(CASE WHEN rp.Role = 'catalyst' 
                                              THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                              END SEPARATOR ', ')
          ) AS ReactionEquation
        FROM {REACTIONS_TABLE} r
        JOIN {REACTIONPARTICIPANTS_TABLE} rp ON r.ReactionID = rp.ReactionID
        JOIN {MOLECULES_TABLE} m ON rp.MoleculeID = m.id
        WHERE r.ReactionID = %s
        GROUP BY r.ReactionID, r.ReactionName, r.ReactionDescription;
        """
        cursor.execute(query, (reaction_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Reaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500