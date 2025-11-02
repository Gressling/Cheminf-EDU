#!/usr/bin/env python3
"""
ChemINF-EDU Application Entry Point
==================================

This is the main entry point for the ChemINF-EDU executable.
It provides a unified interface for running the application as a standalone executable.
"""

import sys
import os
import threading
import webbrowser
from pathlib import Path
import time

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_environment():
    """Setup the application environment for executable"""
    # Set up paths for PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundle
        bundle_dir = sys._MEIPASS
        
        # Set environment variables for the bundled app
        os.environ['CHEMINF_BUNDLE_MODE'] = '1'
        os.environ['CHEMINF_STATIC_PATH'] = os.path.join(bundle_dir, 'cheminf', 'static')
        
        # Ensure database is in the correct location (next to executable)
        exe_dir = os.path.dirname(sys.executable)
        db_path = os.path.join(exe_dir, 'cheminf_edu.db')
        
        # Copy database from bundle to executable directory if it doesn't exist
        bundle_db = os.path.join(bundle_dir, 'cheminf_edu.db')
        if os.path.exists(bundle_db) and not os.path.exists(db_path):
            import shutil
            shutil.copy2(bundle_db, db_path)
        
        os.environ['CHEMINF_DB_PATH'] = db_path
    
    return True

def check_database():
    """Check if database exists and initialize if needed"""
    try:
        from cheminf.db.db import get_db_connection
        
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        conn.close()
        
        if table_count == 0:
            print("Initializing database...")
            from cheminf.db.init_sqlite import create_database
            create_database()
            print("Database initialized successfully!")
        
        return True
    except Exception as e:
        print(f"Database check failed: {e}")
        try:
            print("Attempting to create database...")
            from cheminf.db.init_sqlite import create_database
            create_database()
            print("Database created successfully!")
            return True
        except Exception as e2:
            print(f"Failed to create database: {e2}")
            return False

def open_browser():
    """Open web browser after a short delay"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:8050')
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please open your browser and navigate to: http://localhost:8050")

def main():
    """Main application entry point"""
    print("=" * 60)
    print("ChemINF-EDU - Chemical Informatics Educational Platform")
    print("=" * 60)
    print("")
    
    # Setup environment for executable
    if not setup_environment():
        print("❌ Failed to setup environment")
        input("Press Enter to exit...")
        return 1
    
    # Check/initialize database
    print("Checking database...")
    if not check_database():
        print("❌ Database initialization failed")
        input("Press Enter to exit...")
        return 1
    
    print("✅ Database ready")
    
    try:
        # Import and start the Flask application
        print("Starting ChemINF-EDU server...")
        from cheminf.app import server
        
        # Start browser in background thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("")
        print("🚀 ChemINF-EDU is starting...")
        print("📊 Web interface will open automatically")
        print("🌐 Manual access: http://localhost:8050")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask server
        server.run(
            host='localhost',
            port=8050,
            debug=False,  # Disable debug mode for executable
            use_reloader=False,  # Disable reloader for executable
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 ChemINF-EDU stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)