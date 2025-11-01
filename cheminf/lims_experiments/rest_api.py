from flask import request, jsonify
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX
from cheminf.app_server import server

# Experiments API endpoints
@server.route("/api/lims/experiments", methods=["GET"])
def get_experiments():
    """Get all experiments"""
    try:
        rows = execute_query(f"SELECT * FROM {DB_PREFIX}experiments ORDER BY experiment_id")
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/lims/experiments", methods=["POST"])
def create_experiment():
    """Create a new experiment"""
    try:
        data = request.get_json()
        if not data or 'experiment_name' not in data:
            return jsonify({"error": "Experiment name is required"}), 400
        
        execute_query(
            f"INSERT INTO {DB_PREFIX}experiments (experiment_name, description, start_date, end_date) VALUES (?, ?, ?, ?)",
            (data['experiment_name'], data.get('description', ''), data.get('start_date'), data.get('end_date'))
        )
        return jsonify({"message": "Experiment created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/lims/experiments/<int:experiment_id>", methods=["DELETE"])
def delete_experiment(experiment_id):
    """Delete an experiment"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}experiments WHERE experiment_id = ?", (experiment_id,))
        return jsonify({"message": "Experiment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Samples API endpoints
@server.route("/api/lims/samples", methods=["GET"])
def get_samples():
    """Get all samples with experiment info"""
    try:
        query = f"""
        SELECT s.sample_id, s.sample_code, s.sample_type, s.collection_date, 
               s.experiment_id, e.experiment_name
        FROM {DB_PREFIX}samples s
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        ORDER BY s.sample_id
        """
        rows = execute_query(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/lims/samples", methods=["POST"])
def create_sample():
    """Create a new sample"""
    try:
        data = request.get_json()
        if not data or 'experiment_id' not in data or 'sample_code' not in data:
            return jsonify({"error": "Experiment ID and sample code are required"}), 400
        
        execute_query(
            f"INSERT INTO {DB_PREFIX}samples (experiment_id, sample_code, sample_type, collection_date) VALUES (?, ?, ?, ?)",
            (data['experiment_id'], data['sample_code'], data.get('sample_type', ''), data.get('collection_date'))
        )
        return jsonify({"message": "Sample created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/lims/samples/<int:sample_id>", methods=["DELETE"])
def delete_sample(sample_id):
    """Delete a sample"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}samples WHERE sample_id = ?", (sample_id,))
        return jsonify({"message": "Sample deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Measurements API endpoints
@server.route("/api/lims/measurements", methods=["GET"])
def get_measurements():
    """Get all measurements with sample and experiment info"""
    try:
        query = f"""
        SELECT m.measurement_id, m.parameter, m.value, m.unit, m.measurement_date,
               s.sample_code, e.experiment_name, m.sample_id
        FROM {DB_PREFIX}measurements m
        JOIN {DB_PREFIX}samples s ON m.sample_id = s.sample_id
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        ORDER BY m.measurement_id
        """
        rows = execute_query(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/lims/measurements", methods=["POST"])
def create_measurement():
    """Create a new measurement"""
    try:
        data = request.get_json()
        if not data or 'sample_id' not in data or 'parameter' not in data or 'value' not in data:
            return jsonify({"error": "Sample ID, parameter, and value are required"}), 400
        
        execute_query(
            f"INSERT INTO {DB_PREFIX}measurements (sample_id, parameter, value, unit, measurement_date) VALUES (?, ?, ?, ?, ?)",
            (data['sample_id'], data['parameter'], data['value'], data.get('unit', ''), data.get('measurement_date'))
        )
        return jsonify({"message": "Measurement created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/lims/measurements/<int:measurement_id>", methods=["DELETE"])
def delete_measurement(measurement_id):
    """Delete a measurement"""
    try:
        execute_query(f"DELETE FROM {DB_PREFIX}measurements WHERE measurement_id = ?", (measurement_id,))
        return jsonify({"message": "Measurement deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Experiment samples endpoint
@server.route("/api/lims/experiments/<int:experiment_id>/samples", methods=["GET"])
def get_experiment_samples(experiment_id):
    """Get all samples for a specific experiment"""
    try:
        query = f"""
        SELECT s.sample_id, s.sample_code, s.sample_type, s.collection_date, 
               s.experiment_id, e.experiment_name
        FROM {DB_PREFIX}samples s
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        WHERE s.experiment_id = ?
        ORDER BY s.sample_id
        """
        rows = execute_query(query, (experiment_id,))
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Sample measurements endpoint
@server.route("/api/lims/samples/<int:sample_id>/measurements", methods=["GET"])
def get_sample_measurements(sample_id):
    """Get all measurements for a specific sample"""
    try:
        query = f"""
        SELECT m.measurement_id, m.parameter, m.value, m.unit, m.measurement_date,
               s.sample_code, e.experiment_name, m.sample_id
        FROM {DB_PREFIX}measurements m
        JOIN {DB_PREFIX}samples s ON m.sample_id = s.sample_id
        JOIN {DB_PREFIX}experiments e ON s.experiment_id = e.experiment_id
        WHERE m.sample_id = ?
        ORDER BY m.measurement_id
        """
        rows = execute_query(query, (sample_id,))
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500