import json
import os
from pathlib import Path

# Load settings from JSON file
SETTINGS_FILE = Path(__file__).parent.parent / "settings.json"

def load_settings():
    """Load settings from settings.json file"""
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {SETTINGS_FILE} not found, using defaults")
        return {
            "admin": {"username": "admin", "password": "admin123"},
            "database": {"prefix": "cheminf3_", "path": "cheminf_edu.db"},
            "server": {"host": "localhost", "port": 8050, "debug": True},
            "application": {"name": "ChemINF-EDU", "version": "2.0", "instance_name": "Local Development"}
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing {SETTINGS_FILE}: {e}")
        print("Using default settings")
        return {
            "admin": {"username": "admin", "password": "admin123"},
            "database": {"prefix": "cheminf3_", "path": "cheminf_edu.db"},
            "server": {"host": "localhost", "port": 8050, "debug": True},
            "application": {"name": "ChemINF-EDU", "version": "2.0", "instance_name": "Local Development"}
        }

# Load settings
SETTINGS = load_settings()

# SQLite configuration
DB_PATH = Path(__file__).parent.parent / SETTINGS["database"]["path"]
DB_PREFIX = SETTINGS["database"]["prefix"]

# Admin credentials
ADMIN_USERNAME = SETTINGS["admin"]["username"]
ADMIN_PASSWORD = SETTINGS["admin"]["password"]

# Server configuration
SERVER_HOST = SETTINGS["server"]["host"]
SERVER_PORT = SETTINGS["server"]["port"]
SERVER_DEBUG = SETTINGS["server"]["debug"]

# Application info
APP_NAME = SETTINGS["application"]["name"]
APP_VERSION = SETTINGS["application"]["version"]
INSTANCE_NAME = SETTINGS["application"]["instance_name"]

# Legacy MySQL configuration (kept for backward compatibility)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'cheminf_edu')