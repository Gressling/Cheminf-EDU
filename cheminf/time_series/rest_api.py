from flask import request, jsonify, send_file
from cheminf.db.db import execute_query
from cheminf.config import DB_PREFIX
from cheminf.app_server import server
from datetime import datetime
import json
import csv
import io
from functools import wraps

# API Response wrapper for consistent formatting
def api_response(success=True, data=None, message=None, error=None, status_code=200):
    """Standardized API response format"""
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": data,
        "message": message,
        "error": error
    }
    return jsonify(response), status_code

def handle_api_errors(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return api_response(success=False, error=f"Invalid input: {str(e)}", status_code=400)
        except Exception as e:
            return api_response(success=False, error=f"Internal server error: {str(e)}", status_code=500)
    return decorated_function

# Time Series API endpoints
@server.route("/api/v1/timeseries/experiments", methods=["GET"])
@handle_api_errors
def get_timeseries_experiments():
    """
    Get all experiments that have time series data
    
    Query Parameters:
    - format: json (default), csv, xml
    - include_metadata: true/false (default: true)
    - limit: maximum number of results (default: 100)
    - offset: pagination offset (default: 0)
    """
    # Parse query parameters
    format_type = request.args.get('format', 'json').lower()
    include_metadata = request.args.get('include_metadata', 'true').lower() == 'true'
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    
    # Validate parameters
    if limit > 1000:
        raise ValueError("Limit cannot exceed 1000")
    if offset < 0:
        raise ValueError("Offset cannot be negative")
    if format_type not in ['json', 'csv', 'xml']:
        raise ValueError("Format must be json, csv, or xml")
    
    # Build query with metadata
    if include_metadata:
        query = f"""
        SELECT DISTINCT e.experiment_id, e.experiment_name, e.description,
               e.start_date, e.end_date,
               COUNT(ts.series_id) as series_count,
               COUNT(DISTINCT ts.parameter_name) as parameter_count,
               MIN(ts.timestamp) as data_start_time,
               MAX(ts.timestamp) as data_end_time
        FROM {DB_PREFIX}experiments e
        JOIN {DB_PREFIX}time_series ts ON e.experiment_id = ts.experiment_id
        GROUP BY e.experiment_id, e.experiment_name, e.description, e.start_date, e.end_date
        ORDER BY e.experiment_name
        LIMIT ? OFFSET ?
        """
    else:
        query = f"""
        SELECT DISTINCT e.experiment_id, e.experiment_name, e.description,
               COUNT(ts.series_id) as series_count
        FROM {DB_PREFIX}experiments e
        JOIN {DB_PREFIX}time_series ts ON e.experiment_id = ts.experiment_id
        GROUP BY e.experiment_id, e.experiment_name, e.description
        ORDER BY e.experiment_name
        LIMIT ? OFFSET ?
        """
    
    rows = execute_query(query, (limit, offset))
    
    # Handle different output formats
    if format_type == 'csv':
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        csv_data = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(csv_data, 
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'experiments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    elif format_type == 'xml':
        xml_data = "<experiments>\n"
        for row in rows:
            xml_data += "  <experiment>\n"
            for key, value in row.items():
                xml_data += f"    <{key}>{value}</{key}>\n"
            xml_data += "  </experiment>\n"
        xml_data += "</experiments>"
        
        return xml_data, 200, {'Content-Type': 'application/xml'}
    
    # Default JSON response
    return api_response(
        success=True,
        data={
            "experiments": rows,
            "metadata": {
                "total_returned": len(rows),
                "limit": limit,
                "offset": offset,
                "include_metadata": include_metadata
            }
        },
        message=f"Retrieved {len(rows)} experiments with time series data"
    )

@server.route("/api/v1/timeseries/experiments/<int:experiment_id>/series", methods=["GET"])
@handle_api_errors
def get_experiment_series(experiment_id):
    """
    Get all time series for a specific experiment
    
    Path Parameters:
    - experiment_id: ID of the experiment
    
    Query Parameters:
    - format: json (default), csv, xml
    - include_statistics: true/false (default: true)
    - parameter: filter by specific parameter name (can be used multiple times)
    """
    format_type = request.args.get('format', 'json').lower()
    include_statistics = request.args.get('include_statistics', 'true').lower() == 'true'
    filter_parameters = request.args.getlist('parameter')
    
    if format_type not in ['json', 'csv', 'xml']:
        raise ValueError("Format must be json, csv, or xml")
    
    # Build query with optional parameter filtering
    if include_statistics:
        if filter_parameters:
            placeholders = ','.join(['?' for _ in filter_parameters])
            query = f"""
            SELECT DISTINCT series_name, parameter_name, unit,
                   COUNT(*) as data_points,
                   MIN(timestamp) as start_time,
                   MAX(timestamp) as end_time,
                   MIN(value) as min_value,
                   MAX(value) as max_value,
                   AVG(value) as avg_value,
                   ROUND((MAX(value) - MIN(value)) / COUNT(*), 4) as value_range_per_point
            FROM {DB_PREFIX}time_series
            WHERE experiment_id = ? AND parameter_name IN ({placeholders})
            GROUP BY series_name, parameter_name, unit
            ORDER BY parameter_name
            """
            params = [experiment_id] + filter_parameters
        else:
            query = f"""
            SELECT DISTINCT series_name, parameter_name, unit,
                   COUNT(*) as data_points,
                   MIN(timestamp) as start_time,
                   MAX(timestamp) as end_time,
                   MIN(value) as min_value,
                   MAX(value) as max_value,
                   AVG(value) as avg_value,
                   ROUND((MAX(value) - MIN(value)) / COUNT(*), 4) as value_range_per_point
            FROM {DB_PREFIX}time_series
            WHERE experiment_id = ?
            GROUP BY series_name, parameter_name, unit
            ORDER BY parameter_name
            """
            params = [experiment_id]
    else:
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
        params = [experiment_id]
    
    rows = execute_query(query, params)
    
    if not rows:
        return api_response(
            success=False,
            error=f"No time series data found for experiment {experiment_id}",
            status_code=404
        )
    
    # Handle different output formats
    if format_type == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        
        csv_data = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(csv_data,
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'experiment_{experiment_id}_series_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    elif format_type == 'xml':
        xml_data = f"<experiment_series experiment_id=\"{experiment_id}\">\n"
        for row in rows:
            xml_data += "  <series>\n"
            for key, value in row.items():
                xml_data += f"    <{key}>{value}</{key}>\n"
            xml_data += "  </series>\n"
        xml_data += "</experiment_series>"
        
        return xml_data, 200, {'Content-Type': 'application/xml'}
    
    # Default JSON response
    return api_response(
        success=True,
        data={
            "experiment_id": experiment_id,
            "series": rows,
            "metadata": {
                "series_count": len(rows),
                "include_statistics": include_statistics,
                "filtered_parameters": filter_parameters if filter_parameters else None
            }
        },
        message=f"Retrieved {len(rows)} time series for experiment {experiment_id}"
    )

@server.route("/api/v1/timeseries/experiments/<int:experiment_id>/data", methods=["GET"])
@handle_api_errors
def get_timeseries_data(experiment_id):
    """
    Get time series data for specific experiment and parameters
    
    Path Parameters:
    - experiment_id: ID of the experiment
    
    Query Parameters:
    - parameters: comma-separated list of parameter names to include
    - format: json (default), csv, xml, plotly_json
    - time_range_start: ISO timestamp for start time filter
    - time_range_end: ISO timestamp for end time filter
    - sampling: all (default), every_nth, time_interval
    - sampling_value: used with sampling parameter
    - aggregation: none (default), hourly, daily, custom
    - limit: maximum data points per parameter (default: 10000)
    """
    # Parse parameters
    parameters_str = request.args.get('parameters', '')
    parameters = [p.strip() for p in parameters_str.split(',') if p.strip()] if parameters_str else []
    
    format_type = request.args.get('format', 'json').lower()
    time_start = request.args.get('time_range_start')
    time_end = request.args.get('time_range_end')
    sampling = request.args.get('sampling', 'all').lower()
    sampling_value = request.args.get('sampling_value', '1')
    aggregation = request.args.get('aggregation', 'none').lower()
    limit = int(request.args.get('limit', 10000))
    
    # Validation
    if format_type not in ['json', 'csv', 'xml', 'plotly_json']:
        raise ValueError("Format must be json, csv, xml, or plotly_json")
    if limit > 50000:
        raise ValueError("Limit cannot exceed 50000 data points per parameter")
    if sampling not in ['all', 'every_nth', 'time_interval']:
        raise ValueError("Sampling must be all, every_nth, or time_interval")
    
    # Build base query
    base_query = f"""
    SELECT series_name, parameter_name, time_step, timestamp, value, unit, notes
    FROM {DB_PREFIX}time_series
    WHERE experiment_id = ?
    """
    
    params = [experiment_id]
    
    # Add parameter filtering
    if parameters:
        placeholders = ','.join(['?' for _ in parameters])
        base_query += f" AND parameter_name IN ({placeholders})"
        params.extend(parameters)
    
    # Add time range filtering
    if time_start:
        base_query += " AND timestamp >= ?"
        params.append(time_start)
    if time_end:
        base_query += " AND timestamp <= ?"
        params.append(time_end)
    
    # Add sampling
    if sampling == 'every_nth':
        nth = int(sampling_value)
        base_query += f" AND (time_step - 1) % {nth} = 0"
    elif sampling == 'time_interval':
        # For time interval sampling, we would need more complex logic
        pass
    
    # Add ordering and limit
    base_query += " ORDER BY parameter_name, time_step"
    
    # Execute query
    rows = execute_query(base_query, params)
    
    if not rows:
        return api_response(
            success=False,
            error=f"No time series data found for experiment {experiment_id}",
            status_code=404
        )
    
    # Apply limit per parameter if needed
    if limit < len(rows):
        # Group by parameter and limit each
        parameter_data = {}
        for row in rows:
            param = row['parameter_name']
            if param not in parameter_data:
                parameter_data[param] = []
            if len(parameter_data[param]) < limit:
                parameter_data[param].append(row)
        
        # Flatten back to list
        rows = []
        for param_rows in parameter_data.values():
            rows.extend(param_rows)
    
    # Handle different output formats
    if format_type == 'csv':
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        csv_data = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(csv_data,
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'experiment_{experiment_id}_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    elif format_type == 'xml':
        xml_data = f"<timeseries_data experiment_id=\"{experiment_id}\">\n"
        for row in rows:
            xml_data += "  <datapoint>\n"
            for key, value in row.items():
                xml_data += f"    <{key}>{value}</{key}>\n"
            xml_data += "  </datapoint>\n"
        xml_data += "</timeseries_data>"
        
        return xml_data, 200, {'Content-Type': 'application/xml'}
    
    elif format_type == 'plotly_json':
        # Format for direct use with Plotly
        plotly_data = {}
        for row in rows:
            param = row['parameter_name']
            if param not in plotly_data:
                plotly_data[param] = {
                    'x': [],
                    'y': [],
                    'name': f"{param} ({row['unit']})",
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'unit': row['unit']
                }
            plotly_data[param]['x'].append(row['time_step'])
            plotly_data[param]['y'].append(row['value'])
        
        return api_response(
            success=True,
            data={
                "plotly_traces": list(plotly_data.values()),
                "layout_suggestions": {
                    "title": f"Time Series Data - Experiment {experiment_id}",
                    "xaxis": {"title": "Time Step"},
                    "yaxis": {"title": "Value"}
                }
            },
            message="Data formatted for Plotly visualization"
        )
    
    # Default JSON response
    return api_response(
        success=True,
        data={
            "experiment_id": experiment_id,
            "timeseries_data": rows,
            "metadata": {
                "total_points": len(rows),
                "parameters_included": parameters if parameters else "all",
                "sampling": sampling,
                "format": format_type,
                "time_range": {
                    "start": time_start,
                    "end": time_end
                } if time_start or time_end else None
            }
        },
        message=f"Retrieved {len(rows)} time series data points for experiment {experiment_id}"
    )

@server.route("/api/v1/timeseries/experiments/<int:experiment_id>/statistics", methods=["GET"])
@handle_api_errors
def get_timeseries_statistics(experiment_id):
    """
    Get statistical summary of time series data
    
    Path Parameters:
    - experiment_id: ID of the experiment
    
    Query Parameters:
    - parameters: comma-separated list of parameter names to analyze
    - advanced_stats: true/false (default: false) - include percentiles, std dev, etc.
    - format: json (default), csv, xml
    """
    parameters_str = request.args.get('parameters', '')
    parameters = [p.strip() for p in parameters_str.split(',') if p.strip()] if parameters_str else []
    advanced_stats = request.args.get('advanced_stats', 'false').lower() == 'true'
    format_type = request.args.get('format', 'json').lower()
    
    if format_type not in ['json', 'csv', 'xml']:
        raise ValueError("Format must be json, csv, or xml")
    
    # Build query with optional advanced statistics
    if advanced_stats:
        # SQLite doesn't have built-in percentile functions, so we'll calculate basic stats plus some derived metrics
        base_query = f"""
        SELECT parameter_name, unit,
               COUNT(*) as data_points,
               MIN(value) as min_value,
               MAX(value) as max_value,
               AVG(value) as avg_value,
               (MAX(value) - MIN(value)) as value_range,
               MIN(timestamp) as start_time,
               MAX(timestamp) as end_time,
               GROUP_CONCAT(value) as all_values
        FROM {DB_PREFIX}time_series
        WHERE experiment_id = ?
        """
    else:
        base_query = f"""
        SELECT parameter_name, unit,
               COUNT(*) as data_points,
               MIN(value) as min_value,
               MAX(value) as max_value,
               AVG(value) as avg_value,
               (MAX(value) - MIN(value)) as value_range,
               MIN(timestamp) as start_time,
               MAX(timestamp) as end_time
        FROM {DB_PREFIX}time_series
        WHERE experiment_id = ?
        """
    
    params = [experiment_id]
    
    if parameters:
        placeholders = ','.join(['?' for _ in parameters])
        base_query += f" AND parameter_name IN ({placeholders})"
        params.extend(parameters)
    
    base_query += " GROUP BY parameter_name, unit ORDER BY parameter_name"
    
    rows = execute_query(base_query, params)
    
    if not rows:
        return api_response(
            success=False,
            error=f"No time series data found for experiment {experiment_id}",
            status_code=404
        )
    
    # Calculate advanced statistics if requested
    if advanced_stats:
        enhanced_rows = []
        for row in rows:
            enhanced_row = dict(row)
            if 'all_values' in enhanced_row:
                values = [float(v) for v in enhanced_row['all_values'].split(',')]
                values.sort()
                n = len(values)
                
                # Calculate percentiles
                enhanced_row['median'] = values[n//2] if n % 2 == 1 else (values[n//2-1] + values[n//2]) / 2
                enhanced_row['q1'] = values[n//4]
                enhanced_row['q3'] = values[3*n//4]
                enhanced_row['iqr'] = enhanced_row['q3'] - enhanced_row['q1']
                
                # Calculate standard deviation
                mean = enhanced_row['avg_value']
                variance = sum((v - mean) ** 2 for v in values) / n
                enhanced_row['std_deviation'] = variance ** 0.5
                enhanced_row['coefficient_of_variation'] = enhanced_row['std_deviation'] / mean if mean != 0 else 0
                
                # Remove the raw values field
                del enhanced_row['all_values']
            
            enhanced_rows.append(enhanced_row)
        rows = enhanced_rows
    
    # Handle different output formats
    if format_type == 'csv':
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        csv_data = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(csv_data,
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'experiment_{experiment_id}_statistics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    elif format_type == 'xml':
        xml_data = f"<statistics experiment_id=\"{experiment_id}\">\n"
        for row in rows:
            xml_data += "  <parameter_stats>\n"
            for key, value in row.items():
                xml_data += f"    <{key}>{value}</{key}>\n"
            xml_data += "  </parameter_stats>\n"
        xml_data += "</statistics>"
        
        return xml_data, 200, {'Content-Type': 'application/xml'}
    
    # Default JSON response
    return api_response(
        success=True,
        data={
            "experiment_id": experiment_id,
            "statistics": rows,
            "metadata": {
                "parameters_analyzed": len(rows),
                "advanced_statistics_included": advanced_stats,
                "parameters_filter": parameters if parameters else "all"
            }
        },
        message=f"Statistical analysis completed for {len(rows)} parameters in experiment {experiment_id}"
    )

# POST endpoints for data ingestion
@server.route("/api/v1/timeseries/experiments/<int:experiment_id>/data", methods=["POST"])
@handle_api_errors
def post_timeseries_data(experiment_id):
    """
    Add new time series data points to an experiment
    
    Path Parameters:
    - experiment_id: ID of the experiment
    
    Request Body (JSON):
    {
        "data_points": [
            {
                "parameter_name": "Temperature",
                "value": 85.5,
                "unit": "°C",
                "timestamp": "2024-10-15T09:05:00Z",
                "time_step": 1,
                "series_name": "Temperature-Series-1",
                "notes": "Optional notes"
            }
        ],
        "metadata": {
            "source": "external_sensor",
            "batch_id": "batch_001"
        }
    }
    """
    if not request.is_json:
        raise ValueError("Request must be JSON")
    
    data = request.get_json()
    
    if 'data_points' not in data or not isinstance(data['data_points'], list):
        raise ValueError("Request must contain 'data_points' array")
    
    data_points = data['data_points']
    metadata = data.get('metadata', {})
    
    if len(data_points) == 0:
        raise ValueError("At least one data point is required")
    
    if len(data_points) > 10000:
        raise ValueError("Cannot insert more than 10000 data points in a single request")
    
    # Validate and prepare data for insertion
    insert_data = []
    required_fields = ['parameter_name', 'value', 'timestamp']
    
    for i, point in enumerate(data_points):
        # Validate required fields
        for field in required_fields:
            if field not in point:
                raise ValueError(f"Data point {i+1} missing required field: {field}")
        
        # Prepare insert tuple
        insert_tuple = (
            experiment_id,
            point.get('series_name', f"{point['parameter_name']}-Series"),
            point['parameter_name'],
            point.get('time_step', i + 1),
            point['timestamp'],
            float(point['value']),
            point.get('unit', ''),
            point.get('notes', '')
        )
        insert_data.append(insert_tuple)
    
    # Insert data
    insert_query = f"""
    INSERT INTO {DB_PREFIX}time_series 
    (experiment_id, series_name, parameter_name, time_step, timestamp, value, unit, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # Use execute_many for bulk insert
    from cheminf.db.db import execute_many
    execute_many(insert_query, insert_data)
    
    return api_response(
        success=True,
        data={
            "experiment_id": experiment_id,
            "inserted_points": len(data_points),
            "metadata": metadata
        },
        message=f"Successfully inserted {len(data_points)} data points into experiment {experiment_id}",
        status_code=201
    )

# Bulk data export endpoint
@server.route("/api/v1/timeseries/export", methods=["GET"])
@handle_api_errors
def export_timeseries_bulk():
    """
    Bulk export time series data across multiple experiments
    
    Query Parameters:
    - experiment_ids: comma-separated list of experiment IDs
    - parameters: comma-separated list of parameter names
    - format: csv, json, xml (default: csv)
    - date_from: ISO timestamp for start date filter
    - date_to: ISO timestamp for end date filter
    """
    experiment_ids_str = request.args.get('experiment_ids', '')
    experiment_ids = [int(id.strip()) for id in experiment_ids_str.split(',') if id.strip().isdigit()] if experiment_ids_str else []
    
    parameters_str = request.args.get('parameters', '')
    parameters = [p.strip() for p in parameters_str.split(',') if p.strip()] if parameters_str else []
    
    format_type = request.args.get('format', 'csv').lower()
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    if not experiment_ids:
        raise ValueError("At least one experiment_id is required")
    
    if len(experiment_ids) > 50:
        raise ValueError("Cannot export more than 50 experiments at once")
    
    if format_type not in ['json', 'csv', 'xml']:
        raise ValueError("Format must be json, csv, or xml")
    
    # Build query
    placeholders = ','.join(['?' for _ in experiment_ids])
    query = f"""
    SELECT e.experiment_name, ts.experiment_id, ts.series_name, ts.parameter_name, 
           ts.time_step, ts.timestamp, ts.value, ts.unit, ts.notes
    FROM {DB_PREFIX}time_series ts
    JOIN {DB_PREFIX}experiments e ON ts.experiment_id = e.experiment_id
    WHERE ts.experiment_id IN ({placeholders})
    """
    
    params = experiment_ids
    
    if parameters:
        param_placeholders = ','.join(['?' for _ in parameters])
        query += f" AND ts.parameter_name IN ({param_placeholders})"
        params.extend(parameters)
    
    if date_from:
        query += " AND ts.timestamp >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND ts.timestamp <= ?"
        params.append(date_to)
    
    query += " ORDER BY ts.experiment_id, ts.parameter_name, ts.time_step"
    
    rows = execute_query(query, params)
    
    if not rows:
        return api_response(
            success=False,
            error="No data found for specified criteria",
            status_code=404
        )
    
    # Handle different output formats
    if format_type == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        
        csv_data = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(csv_data,
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'timeseries_bulk_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    elif format_type == 'xml':
        xml_data = "<bulk_export>\n"
        current_exp = None
        
        for row in rows:
            if row['experiment_id'] != current_exp:
                if current_exp is not None:
                    xml_data += "  </experiment>\n"
                xml_data += f"  <experiment id=\"{row['experiment_id']}\" name=\"{row['experiment_name']}\">\n"
                current_exp = row['experiment_id']
            
            xml_data += "    <datapoint>\n"
            for key, value in row.items():
                if key not in ['experiment_id', 'experiment_name']:
                    xml_data += f"      <{key}>{value}</{key}>\n"
            xml_data += "    </datapoint>\n"
        
        if current_exp is not None:
            xml_data += "  </experiment>\n"
        xml_data += "</bulk_export>"
        
        return xml_data, 200, {'Content-Type': 'application/xml'}
    
    # Default JSON response
    return api_response(
        success=True,
        data={
            "export_data": rows,
            "metadata": {
                "total_points": len(rows),
                "experiments_included": experiment_ids,
                "parameters_included": parameters if parameters else "all",
                "date_range": {
                    "from": date_from,
                    "to": date_to
                } if date_from or date_to else None
            }
        },
        message=f"Bulk export completed with {len(rows)} data points"
    )