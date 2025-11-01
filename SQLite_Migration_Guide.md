# SQLite Migration Guide

## Overview
This document outlines the migration from MySQL to SQLite for the Cheminf-EDU project.

## Changes Made

### 1. Database Files
- **NEW**: `cheminf/db/init_sqlite.py` - Database initialization script
- **UPDATED**: `cheminf/db/db.py` - Database connection module (MySQL → SQLite)
- **UPDATED**: `cheminf/config.py` - Configuration (MySQL → SQLite)
- **UPDATED**: `requirements.txt` - Removed mysql-connector-python

### 2. Database Location
- **Database file**: `cheminf_edu.db` (in project root)
- **Path**: Automatically resolved using `pathlib.Path`

### 3. Schema Conversion
All MySQL tables converted to SQLite equivalents:

#### Tables Created:
- `cheminf3_molecules` (40 molecules with SMILES data)
- `cheminf3_reactions` (1 aspirin synthesis reaction)
- `cheminf3_reactionparticipants` (5 reaction participants)
- `cheminf3_inventory` (5 inventory items)
- `cheminf3_project` (1 project)
- `cheminf3_task` (3 tasks)
- `cheminf3_experiments` (4 experiments)
- `cheminf3_samples` (20 samples)
- `cheminf3_measurements` (20 measurements)

### 4. Key Differences: MySQL vs SQLite

| Feature | MySQL | SQLite |
|---------|--------|--------|
| AUTO_INCREMENT | `INT AUTO_INCREMENT` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Connection | Network-based | File-based |
| Setup | Requires server | No setup required |
| Foreign Keys | Always enabled | Must enable with `PRAGMA foreign_keys = ON` |
| Data Types | Strict typing | Dynamic typing |

### 5. API Changes

#### New Functions in `db.py`:
- `execute_query(query, params=None)` - Execute any SQL query
- `execute_many(query, params_list)` - Execute query with multiple parameter sets

#### Updated Functions:
- `get_db_connection()` - Now returns SQLite connection with row factory
- `get_all_rows()` - Returns dictionary objects (compatible with previous MySQL format)

## Usage

### Initialize Database
```python
from cheminf.db.init_sqlite import create_database
create_database()
```

### Query Database
```python
from cheminf.db.db import get_db_connection, execute_query

# Get all molecules
molecules = execute_query("SELECT * FROM cheminf3_molecules")

# Insert new molecule
execute_query(
    "INSERT INTO cheminf3_molecules (MoleculeUpacName, SMILES) VALUES (?, ?)",
    ("Test Molecule", "C")
)
```

## Migration Steps Completed

1. ✅ Created SQLite database schema
2. ✅ Migrated all existing data
3. ✅ Updated database connection layer
4. ✅ Added backward-compatible API
5. ✅ Updated dependencies
6. ✅ Tested database functionality

## Benefits of SQLite Migration

1. **Simplified Setup**: No database server required
2. **Portability**: Single file database
3. **Zero Configuration**: Works out of the box
4. **Reliability**: ACID compliant, battle-tested
5. **Performance**: Excellent for small to medium datasets
6. **Development Friendly**: Easy to backup, copy, and version

## Next Steps

1. Update any existing application code that directly uses MySQL-specific features
2. Test all application modules with the new SQLite database
3. Update documentation to reflect SQLite usage
4. Consider adding database versioning/migration scripts for future changes

## Rollback Plan

If needed to revert to MySQL:
1. Restore original `db.py` and `config.py` files
2. Add `mysql-connector-python` back to requirements.txt
3. Set up MySQL server and import data using original SQL files

## Files to Review

The following files may need updates to work with the new SQLite database:
- `cheminf/molecules/rest_api.py`
- `cheminf/reactions/rest_api.py`
- `cheminf/inventory/rest_api.py`
- `cheminf/lims_experiments/rest_api.py`
- `cheminf/projects/rest_api.py`
- Any other files that import from `cheminf.db.db`