from flask import request, jsonify
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME  # assuming DB_PREFIX is not needed here
from cheminf.app_server import server

EXPERIMENTS_TABLE = f"{DB_NAME}.cheminf3_experiments"
SAMPLES_TABLE = f"{DB_NAME}.cheminf3_samples"
MEASUREMENTS_TABLE = f"{DB_NAME}.cheminf3_measurements"

@server.route("/api/experiments", methods=["GET"])
def get_experiments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {EXPERIMENTS_TABLE}")
    experiments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(experiments), 200

@server.route("/api/samples", methods=["GET"])
def get_samples():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {SAMPLES_TABLE}")
    samples = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(samples), 200

@server.route("/api/measurements", methods=["GET"])
def get_measurements():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {MEASUREMENTS_TABLE}")
    measurements = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(measurements), 200