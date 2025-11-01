from flask import request, jsonify
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME  # assuming DB_PREFIX is not needed here
from cheminf.app_server import server

EXPERIMENTS_TABLE = f"{DB_NAME}.cheminf3_experiments"
SAMPLES_TABLE = f"{DB_NAME}.cheminf3_samples"
MEASUREMENTS_TABLE = f"{DB_NAME}.cheminf3_measurements"

@server.route("/api/experiments", methods=["GET"])
def get_experiments():
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

@server.route("/api/samples", methods=["GET"])
def get_samples():
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return

@server.route("/api/measurements", methods=["GET"])
def get_measurements():
    """Temporarily disabled for SQLite migration"""
    return []  # Placeholder return