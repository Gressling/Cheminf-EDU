from flask import request, jsonify
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX
from cheminf.app_server import server

# Time Series API endpoints
@server.route("/api/timeseries/experiments", methods=["GET"])
def get_timeseries_experiments():
    """Get all experiments that have time series data"""
    try:
        query = f"""
        SELECT DISTINCT e.experiment_id, e.experiment_name, e.description,
               COUNT(ts.series_id) as series_count
        FROM {DB_PREFIX}experiments e
        JOIN {DB_PREFIX}time_series ts ON e.experiment_id = ts.experiment_id
        GROUP BY e.experiment_id, e.experiment_name, e.description
        ORDER BY e.experiment_name
        """
        rows = execute_query(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/timeseries/series/<int:experiment_id>", methods=["GET"])
def get_experiment_series(experiment_id):
    """Get all time series for a specific experiment"""
    try:
        query = f"""
        SELECT DISTINCT series_name, parameter_name, unit,
               COUNT(*) as data_points,
               MIN(timestamp) as start_time,
               MAX(timestamp) as end_time
        FROM {DB_PREFIX}time_series
        WHERE experiment_id = ?
        GROUP BY series_name, parameter_name, unit
        ORDER BY parameter_name
        """
        rows = execute_query(query, (experiment_id,))
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/timeseries/data/<int:experiment_id>", methods=["GET"])
def get_timeseries_data(experiment_id):
    """Get time series data for specific experiment and parameters"""
    try:
        parameters = request.args.getlist('parameters')
        
        if parameters:
            placeholders = ','.join(['?' for _ in parameters])
            query = f"""
            SELECT series_name, parameter_name, time_step, timestamp, value, unit
            FROM {DB_PREFIX}time_series
            WHERE experiment_id = ? AND parameter_name IN ({placeholders})
            ORDER BY parameter_name, time_step
            """
            params = [experiment_id] + parameters
        else:
            query = f"""
            SELECT series_name, parameter_name, time_step, timestamp, value, unit
            FROM {DB_PREFIX}time_series
            WHERE experiment_id = ?
            ORDER BY parameter_name, time_step
            """
            params = [experiment_id]
        
        rows = execute_query(query, params)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/api/timeseries/statistics/<int:experiment_id>", methods=["GET"])
def get_timeseries_statistics(experiment_id):
    """Get statistical summary of time series data"""
    try:
        query = f"""
        SELECT parameter_name, unit,
               COUNT(*) as data_points,
               MIN(value) as min_value,
               MAX(value) as max_value,
               AVG(value) as avg_value,
               MIN(timestamp) as start_time,
               MAX(timestamp) as end_time
        FROM {DB_PREFIX}time_series
        WHERE experiment_id = ?
        GROUP BY parameter_name, unit
        ORDER BY parameter_name
        """
        rows = execute_query(query, (experiment_id,))
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500