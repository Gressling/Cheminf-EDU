import os
import sqlite3
from pathlib import Path

# Try to load dotenv, but continue if not available
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass  # dotenv not available, continue without it

# SQLite database configuration
DB_PATH = Path(__file__).parent.parent.parent / "cheminf_edu.db"
DB_PREFIX = os.environ.get('DB_PREFIX', 'cheminf3_')

TABLE_NAME = f"{DB_PREFIX}molecules"

def get_db_connection():
    """Get SQLite database connection with row factory for dictionary-like access."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # This allows dictionary-like access to rows
    return connection

def get_all_rows():
    """Get all rows from molecules table."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = [dict(row) for row in cursor.fetchall()]  # Convert Row objects to dictionaries
    cursor.close()
    connection.close()
    return rows

def execute_query(query, params=None):
    """Execute a query and return results."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
            return results
        else:
            connection.commit()
            return cursor.rowcount
    finally:
        cursor.close()
        connection.close()

def execute_many(query, params_list):
    """Execute a query with multiple parameter sets."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.executemany(query, params_list)
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()