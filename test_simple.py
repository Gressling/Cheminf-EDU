#!/usr/bin/env python3
"""
Simple SQLite Database Test Script
Tests the basic SQLite migration functionality.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from cheminf.db.db import get_db_connection, execute_query, get_all_rows

def main():
    print("=" * 60)
    print("SQLite Database Migration Test")
    print("=" * 60)
    
    try:
        # Test connection
        conn = get_db_connection()
        print("[OK] Database connection successful")
        conn.close()
        
        # Test molecules
        molecules = get_all_rows()
        print(f"[OK] Found {len(molecules)} molecules")
        
        # Test reactions
        reactions = execute_query("SELECT * FROM cheminf3_reactions")
        print(f"[OK] Found {len(reactions)} reactions")
        
        # Test inventory
        inventory = execute_query("SELECT * FROM cheminf3_inventory")
        print(f"[OK] Found {len(inventory)} inventory items")
        
        # Test experiments
        experiments = execute_query("SELECT * FROM cheminf3_experiments")
        print(f"[OK] Found {len(experiments)} experiments")
        
        # Test samples
        samples = execute_query("SELECT * FROM cheminf3_samples")
        print(f"[OK] Found {len(samples)} samples")
        
        # Test measurements
        measurements = execute_query("SELECT * FROM cheminf3_measurements")
        print(f"[OK] Found {len(measurements)} measurements")
        
        # Test projects
        projects = execute_query("SELECT * FROM cheminf3_project")
        print(f"[OK] Found {len(projects)} projects")
        
        # Test tasks
        tasks = execute_query("SELECT * FROM cheminf3_task")
        print(f"[OK] Found {len(tasks)} tasks")
        
        print("\n" + "=" * 60)
        print("SAMPLE DATA:")
        print("=" * 60)
        
        # Show some sample molecules
        print("First 3 molecules:")
        for i, mol in enumerate(molecules[:3], 1):
            smiles = mol.get('SMILES', 'No SMILES')
            print(f"  {i}. {mol['MoleculeUpacName']} - {smiles}")
        
        # Show inventory
        print(f"\nInventory ({len(inventory)} items):")
        for item in inventory:
            print(f"  - {item['MoleculeUpacName']}: {item['amount']} {item['unit']}")
        
        # Show reaction info
        if reactions:
            reaction = reactions[0]
            print(f"\nReaction: {reaction['ReactionName']}")
            print(f"Description: {reaction['ReactionDescription']}")
        
        print("\n" + "=" * 60)
        print("SUCCESS: SQLite migration completed successfully!")
        print("All tables created and populated with sample data.")
        print("Database ready for use.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)