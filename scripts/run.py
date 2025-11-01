#!/usr/bin/env python3
"""
Cheminf-EDU Application Runner
=============================

This script provides an easy way to start the Cheminf-EDU application with various options.
It handles database initialization, environment setup, and application launching.

Usage:
    python scripts/run.py                    # Start main application
    python scripts/run.py --module molecules # Start specific module
    python scripts/run.py --init-db         # Initialize database only
    python scripts/run.py --test-db         # Test database connection
    python scripts/run.py --help            # Show help

Requirements:
    - Virtual environment activated (venv)
    - SQLite database (automatically created if missing)
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def check_environment():
    """Check if the environment is properly set up."""
    print("Checking environment...")
    
    # Check if we're in virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected. Please activate venv:")
        print("   .\\venv\\Scripts\\Activate.ps1  (PowerShell)")
        print("   .\\venv\\Scripts\\activate.bat  (Command Prompt)")
        return False
    
    print("✅ Virtual environment: Active")
    
    # Check if database exists
    db_path = PROJECT_ROOT / "cheminf_edu.db"
    if not db_path.exists():
        print("⚠️  SQLite database not found. Creating database...")
        return init_database()
    
    print("✅ SQLite database: Found")
    return True

def init_database():
    """Initialize the SQLite database."""
    try:
        print("Initializing SQLite database...")
        from cheminf.db.init_sqlite import create_database
        create_database()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def test_database():
    """Test database connection and show basic info."""
    try:
        print("Testing database connection...")
        from cheminf.db.db import get_db_connection, execute_query, get_all_rows
        
        # Test connection
        conn = get_db_connection()
        print("✅ Database connection successful")
        conn.close()
        
        # Get basic statistics
        molecules = get_all_rows()
        reactions = execute_query("SELECT COUNT(*) as count FROM cheminf3_reactions")
        inventory = execute_query("SELECT COUNT(*) as count FROM cheminf3_inventory")
        experiments = execute_query("SELECT COUNT(*) as count FROM cheminf3_experiments")
        
        print("\n📊 Database Statistics:")
        print(f"   Molecules: {len(molecules)}")
        print(f"   Reactions: {reactions[0]['count']}")
        print(f"   Inventory Items: {inventory[0]['count']}")
        print(f"   Experiments: {experiments[0]['count']}")
        
        print("\n✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_main_app():
    """Start the main Cheminf-EDU application."""
    try:
        print("Starting Cheminf-EDU main application...")
        
        # Try to import the main app
        try:
            from cheminf.app import server
            app_type = "Flask"
        except ImportError as e1:
            print(f"   Could not import main Flask app: {e1}")
            try:
                print("   Trying molecules module as fallback...")
                from cheminf.molecules.molecules import app as server
                app_type = "Dash"
            except ImportError as e2:
                print(f"❌ Failed to import any application: {e2}")
                print("   Make sure all dependencies are installed:")
                print("     pip install -r requirements.txt")
                return False
        
        print(f"\n🚀 {app_type} application starting...")
        print("   URL: http://localhost:8050")
        print("   Press Ctrl+C to stop")
        print("-" * 50)
        
        if app_type == "Flask":
            server.run(debug=True, host='localhost', port=8050)
        else:
            server.run(debug=True, host='localhost', port=8050)
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_module(module_name):
    """Start a specific module."""
    module_map = {
        'molecules': 'cheminf.molecules.molecules',
        'reactions': 'cheminf.reactions.rest_api',
        'inventory': 'cheminf.inventory.rest_api',
        'experiments': 'cheminf.lims_experiments.rest_api',
        'projects': 'cheminf.projects.rest_api'
    }
    
    if module_name not in module_map:
        print(f"❌ Unknown module: {module_name}")
        print(f"Available modules: {', '.join(module_map.keys())}")
        return False
    
    try:
        print(f"Starting {module_name} module...")
        module_path = module_map[module_name]
        
        if module_name == 'molecules':
            from cheminf.molecules.molecules import app
            print(f"\n🚀 {module_name.title()} module starting...")
            print("   URL: http://localhost:8050")
            print("   Press Ctrl+C to stop")
            print("-" * 50)
            app.run(debug=True, host='localhost', port=8050)
        else:
            print(f"   Module: {module_path}")
            print("   Note: This module may need additional setup.")
            __import__(module_path)
            
    except ImportError as e:
        print(f"❌ Failed to import {module_name} module: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to start {module_name} module: {e}")
        return False

def show_help():
    """Show detailed help information."""
    help_text = """
Cheminf-EDU Application Runner
=============================

COMMANDS:
    python scripts/run.py                    Start main application (default)
    python scripts/run.py --module NAME     Start specific module
    python scripts/run.py --init-db         Initialize database only
    python scripts/run.py --test-db         Test database connection
    python scripts/run.py --help            Show this help

MODULES:
    molecules    - Molecule management interface
    reactions    - Chemical reactions module
    inventory    - Chemical inventory system
    experiments  - LIMS experiments module
    projects     - Project management

EXAMPLES:
    # Start main application
    python scripts/run.py

    # Start molecules module only
    python scripts/run.py --module molecules

    # Initialize database
    python scripts/run.py --init-db

    # Test database connection
    python scripts/run.py --test-db

REQUIREMENTS:
    1. Activate virtual environment:
       .\\venv\\Scripts\\Activate.ps1     (PowerShell)
       .\\venv\\Scripts\\activate.bat     (Command Prompt)

    2. Install dependencies:
       pip install -r requirements.txt

    3. Database will be created automatically if missing

TROUBLESHOOTING:
    - If database is missing: Use --init-db to recreate
    - If modules fail to load: Check dependencies with --test-db
    - For import errors: Ensure virtual environment is active

DATABASE:
    Location: cheminf_edu.db (SQLite)
    Tables: 9 tables with sample chemistry data
    Backup: Simply copy the .db file

For more information, see README_SQLite_Migration.md
"""
    print(help_text)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Cheminf-EDU Application Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--module', '-m',
        type=str,
        help='Start specific module (molecules, reactions, inventory, experiments, projects)'
    )
    
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize SQLite database and exit'
    )
    
    parser.add_argument(
        '--test-db',
        action='store_true',
        help='Test database connection and show statistics'
    )
    
    parser.add_argument(
        '--help-detailed',
        action='store_true',
        help='Show detailed help information'
    )
    
    args = parser.parse_args()
    
    # Show detailed help
    if args.help_detailed:
        show_help()
        return
    
    print("=" * 60)
    print("Cheminf-EDU Application Runner")
    print("=" * 60)
    
    # Check environment first (unless just showing help)
    if not args.help_detailed:
        if not check_environment():
            sys.exit(1)
    
    # Handle specific commands
    if args.init_db:
        if init_database():
            print("\n✅ Database initialization complete!")
        else:
            sys.exit(1)
        return
    
    if args.test_db:
        if test_database():
            print("\n✅ Database test complete!")
        else:
            sys.exit(1)
        return
    
    if args.module:
        if not start_module(args.module):
            sys.exit(1)
        return
    
    # Default: start main application
    if not start_main_app():
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)