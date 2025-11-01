#!/usr/bin/env python3
"""
SQLite Migration Helper
This script updates all MySQL-style database calls to use SQLite-compatible functions.
"""

import os
import re
from pathlib import Path

# Files to update
files_to_update = [
    "cheminf/inventory/rest_api.py",
    "cheminf/projects/ui_projects.py", 
    "cheminf/projects/ui_tasks.py",
    "cheminf/projects/rest_api.py",
    "cheminf/reactions/ui_overview.py",
    "cheminf/reactions/ui_reactions.py", 
    "cheminf/reactions/ui_reactionparticipants.py",
    "cheminf/reactions/rest_api.py",
    "cheminf/lims_experiments/ui_experiments.py",
    "cheminf/lims_experiments/ui_samples.py",
    "cheminf/lims_experiments/ui_measurements.py",
    "cheminf/lims_experiments/rest_api.py"
]

def update_file_imports(filepath):
    """Update imports to use SQLite functions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update imports
    if "from cheminf.db.db import get_db_connection" in content:
        content = content.replace(
            "from cheminf.db.db import get_db_connection",
            "from cheminf.db.db import execute_query"
        )
    
    # Update MySQL-style database calls
    patterns = [
        # Pattern for simple SELECT queries with dictionary cursor
        (r'connection = get_db_connection\(\)\s*\n\s*cursor = connection\.cursor\(dictionary=True\)\s*\n\s*cursor\.execute\(([^)]+)\)\s*\n\s*rows = cursor\.fetchall\(\)\s*\n\s*cursor\.close\(\)\s*\n\s*connection\.close\(\)',
         r'rows = execute_query(\1)'),
        
        # Pattern for single row fetch
        (r'connection = get_db_connection\(\)\s*\n\s*cursor = connection\.cursor\(dictionary=True\)\s*\n\s*cursor\.execute\(([^)]+)\)\s*\n\s*row = cursor\.fetchone\(\)\s*\n\s*cursor\.close\(\)\s*\n\s*connection\.close\(\)',
         r'rows = execute_query(\1)\n        row = rows[0] if rows else None'),
         
        # Pattern for INSERT/UPDATE/DELETE operations
        (r'connection = get_db_connection\(\)\s*\n\s*cursor = connection\.cursor\(\)\s*\n\s*cursor\.execute\(([^)]+)\)\s*\n\s*connection\.commit\(\)\s*\n\s*cursor\.close\(\)\s*\n\s*connection\.close\(\)',
         r'execute_query(\1)'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Replace %s with ? for SQLite parameter placeholders
    content = re.sub(r'(%s)', r'?', content)
    
    # Update specific cursor calls
    content = re.sub(r'cursor = connection\.cursor\(dictionary=True\)', 
                    r'# Using execute_query instead', content)
    content = re.sub(r'cursor = conn\.cursor\(dictionary=True\)', 
                    r'# Using execute_query instead', content)
    
    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Main function to update all files."""
    print("SQLite Migration Helper")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    updated_files = []
    
    for file_path in files_to_update:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"Updating: {file_path}")
            if update_file_imports(str(full_path)):
                updated_files.append(file_path)
                print(f"  ✓ Updated")
            else:
                print(f"  - No changes needed")
        else:
            print(f"  ! File not found: {file_path}")
    
    print("\n" + "=" * 50)
    if updated_files:
        print(f"Updated {len(updated_files)} files:")
        for file in updated_files:
            print(f"  - {file}")
        print("\nNote: You may need to manually review and fix complex database operations.")
    else:
        print("No files needed updates.")

if __name__ == "__main__":
    main()