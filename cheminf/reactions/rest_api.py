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
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

# ---------- Reaction Participants Endpoints ----------

@server.route("/api/reactions/<int:reaction_id>/participants", methods=["GET"])
def api_get_reactionparticipants(reaction_id):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

@server.route("/api/reactions/<int:reaction_id>/participants", methods=["POST"])
def api_create_reactionparticipant(reaction_id):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

@server.route("/api/participants/<int:reaction_id>/<int:molecule_id>/<role>", methods=["PUT"])
def api_update_reactionparticipant(reaction_id, molecule_id, role):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

@server.route("/api/participants/<int:reaction_id>/<int:molecule_id>/<role>", methods=["DELETE"])
def api_delete_reactionparticipant(reaction_id, molecule_id, role):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

@server.route("/api/reactions/overview/<int:reaction_id>", methods=["GET"])
def api_reaction_overview(reaction_id):
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return