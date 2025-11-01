#!/usr/bin/env python3
"""
SQLite Database Test Script
This script tests all the basic database operations to ensure the SQLite migration was successful.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from cheminf.db.db import get_db_connection, execute_query, get_all_rows

def test_database_connection():
    """Test basic database connection."""
    print("=" * 50)
    print("TESTING DATABASE CONNECTION")
    print("=" * 50)
    
    try:
        conn = get_db_connection()
        print("[OK] Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False

def test_molecules_table():
    """Test molecules table operations."""
    print("\n" + "=" * 50)
    print("TESTING MOLECULES TABLE")
    print("=" * 50)
    
    try:
        # Get all molecules
        molecules = get_all_rows()
        print(f"[OK] Retrieved {len(molecules)} molecules")
        
        # Show first few molecules
        print("\nFirst 5 molecules:")
        for i, mol in enumerate(molecules[:5], 1):
            print(f"  {i}. ID:{mol['id']} - {mol['MoleculeUpacName']} ({mol.get('SMILES', 'No SMILES')})")
        
        return True
    except Exception as e:
        print(f"[ERROR] Molecules table test failed: {e}")
        return False

def test_reactions_table():
    """Test reactions table."""
    print("\n" + "=" * 50)
    print("TESTING REACTIONS TABLE")
    print("=" * 50)
    
    try:
        reactions = execute_query("SELECT * FROM cheminf3_reactions")
        print(f"[OK] Retrieved {len(reactions)} reactions")
        
        for reaction in reactions:
            print(f"  - {reaction['ReactionName']}: {reaction['ReactionDescription']}")
        
        # Test reaction participants
        participants = execute_query("""
            SELECT rp.*, m.MoleculeUpacName 
            FROM cheminf3_reactionparticipants rp 
            JOIN cheminf3_molecules m ON rp.MoleculeID = m.id 
            WHERE rp.ReactionID = 1
        """)
        print(f"[OK] Retrieved {len(participants)} reaction participants")
        
        for part in participants:
            print(f"    {part['Role']}: {part['MoleculeUpacName']} (coeff: {part['StoichiometricCoefficient']})")
        
        return True
    except Exception as e:
        print(f"[ERROR] Reactions table test failed: {e}")
        return False

def test_inventory_table():
    """Test inventory table."""
    print("\n" + "=" * 50)
    print("TESTING INVENTORY TABLE")
    print("=" * 50)
    
    try:
        inventory = execute_query("SELECT * FROM cheminf3_inventory")
        print(f"✓ Retrieved {len(inventory)} inventory items")
        
        for item in inventory:
            print(f"  - {item['MoleculeUpacName']}: {item['amount']} {item['unit']}")
        
        return True
    except Exception as e:
        print(f"✗ Inventory table test failed: {e}")
        return False

def test_lims_tables():
    """Test LIMS experiments, samples, and measurements tables."""
    print("\n" + "=" * 50)
    print("TESTING LIMS TABLES")
    print("=" * 50)
    
    try:
        # Test experiments
        experiments = execute_query("SELECT * FROM cheminf3_experiments")
        print(f"✓ Retrieved {len(experiments)} experiments")
        
        # Test samples
        samples = execute_query("SELECT * FROM cheminf3_samples")
        print(f"✓ Retrieved {len(samples)} samples")
        
        # Test measurements
        measurements = execute_query("SELECT * FROM cheminf3_measurements")
        print(f"✓ Retrieved {len(measurements)} measurements")
        
        # Show sample data
        print("\nSample experiments:")
        for exp in experiments[:3]:
            print(f"  - {exp['experiment_name']}: {exp['description']}")
        
        return True
    except Exception as e:
        print(f"✗ LIMS tables test failed: {e}")
        return False

def test_projects_table():
    """Test projects and tasks tables."""
    print("\n" + "=" * 50)
    print("TESTING PROJECTS TABLE")
    print("=" * 50)
    
    try:
        projects = execute_query("SELECT * FROM cheminf3_project")
        print(f"✓ Retrieved {len(projects)} projects")
        
        tasks = execute_query("SELECT * FROM cheminf3_task")
        print(f"✓ Retrieved {len(tasks)} tasks")
        
        for project in projects:
            print(f"  Project: {project['name']}")
            project_tasks = execute_query("SELECT * FROM cheminf3_task WHERE project_id = ?", (project['id'],))
            for task in project_tasks:
                print(f"    - Task: {task['description']}")
        
        return True
    except Exception as e:
        print(f"✗ Projects table test failed: {e}")
        return False

def run_all_tests():
    """Run all database tests."""
    print("SQLite Database Migration Verification")
    print("Started at:", Path(__file__).parent / "cheminf_edu.db")
    
    tests = [
        test_database_connection,
        test_molecules_table,
        test_reactions_table,
        test_inventory_table,
        test_lims_tables,
        test_projects_table
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Passed: {passed}/{len(tests)} tests")
    
    if passed == len(tests):
        print("[SUCCESS] ALL TESTS PASSED! SQLite migration was successful!")
        print("\nYour database is ready for use:")
        print(f"  Database: {Path(__file__).parent / 'cheminf_edu.db'}")
        print(f"  Tables: 9 tables created with sample data")
        print(f"  Status: [OK] Ready for development")
    else:
        print(f"[ERROR] {len(tests) - passed} tests failed. Please check the errors above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)