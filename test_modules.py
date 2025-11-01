#!/usr/bin/env python3
"""
Simple test to verify the molecules module works
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_molecules_import():
    """Test importing molecules module."""
    try:
        print("Testing molecules module import...")
        from cheminf.molecules.molecules import app, get_all_rows
        
        print("✓ Successfully imported molecules module")
        print(f"✓ App type: {type(app)}")
        
        # Test database connection
        molecules = get_all_rows()
        print(f"✓ Database connection works: {len(molecules)} molecules found")
        
        # Show available methods
        methods = [method for method in dir(app) if not method.startswith('_')]
        print(f"✓ App has {len(methods)} public methods")
        
        return True
        
    except Exception as e:
        print(f"✗ Error importing molecules module: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_dash_app():
    """Create a simple Dash app to test if Dash works."""
    try:
        print("\nTesting simple Dash app...")
        import dash
        from dash import html
        
        simple_app = dash.Dash(__name__)
        simple_app.layout = html.Div([
            html.H1("Test Dash App"),
            html.P("If you can see this, Dash is working!")
        ])
        
        print("✓ Simple Dash app created successfully")
        print("✓ Starting test server on port 8051...")
        
        # Start the app (will run until stopped)
        simple_app.run(debug=False, host='localhost', port=8051)
        
    except Exception as e:
        print(f"✗ Error with simple Dash app: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cheminf-EDU Module Test")
    print("=" * 60)
    
    if test_molecules_import():
        print("\n" + "=" * 60)
        print("Starting simple test app...")
        print("Open browser to: http://localhost:8051")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        test_simple_dash_app()
    else:
        print("\n✗ Module import failed. Cannot start test app.")
        sys.exit(1)