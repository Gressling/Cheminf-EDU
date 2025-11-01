# Scripts Directory

This directory contains launcher scripts and utilities for the Cheminf-EDU application.

## Files

### `run.py` - Main Python Launcher
The primary application launcher with full functionality.

**Usage:**
```bash
# Start main application
python scripts/run.py

# Start specific module
python scripts/run.py --module molecules

# Initialize database
python scripts/run.py --init-db

# Test database
python scripts/run.py --test-db

# Show help
python scripts/run.py --help
```

**Features:**
- ✅ Environment checking
- ✅ Automatic database initialization
- ✅ Module-specific launching
- ✅ Database testing and statistics
- ✅ Comprehensive error handling

### `run.bat` - Windows Batch Launcher
Quick launcher for Windows Command Prompt users.

**Usage:**
```cmd
# From project root:
scripts\run.bat

# Or from scripts directory:
cd scripts
.\run.bat

# Pass arguments
scripts\run.bat --module molecules
.\run.bat --test-db
```

### `run.ps1` - PowerShell Launcher  
Enhanced launcher for PowerShell users with better formatting.

**Usage:**
```powershell
# From project root:
.\scripts\run.ps1

# Or from scripts directory:
cd scripts
.\run.ps1

# Pass arguments
.\scripts\run.ps1 --module molecules
.\run.ps1 --test-db
```

## Quick Start

### Option 1: Python (Recommended)
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run application
python scripts/run.py
```

### Option 2: Windows Batch
```cmd
# Just double-click run.bat or:
scripts\run.bat
```

### Option 3: PowerShell
```powershell
# From PowerShell:
.\scripts\run.ps1
```

## Available Modules

| Module | Description | Port |
|--------|-------------|------|
| `molecules` | Molecule management interface | 8050 |
| `reactions` | Chemical reactions module | 8050 |
| `inventory` | Chemical inventory system | 8050 |
| `experiments` | LIMS experiments module | 8050 |
| `projects` | Project management | 8050 |

## Environment Requirements

1. **Virtual Environment**: Must be activated
   ```bash
   .\venv\Scripts\Activate.ps1  # PowerShell
   .\venv\Scripts\activate.bat  # Command Prompt
   ```

2. **Dependencies**: Installed via pip
   ```bash
   pip install -r requirements.txt
   ```

3. **Database**: SQLite database (auto-created if missing)
   - File: `cheminf_edu.db`
   - Tables: 9 tables with sample data

## Troubleshooting

### Virtual Environment Issues
```bash
# Create new virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Database Issues
```bash
# Test database
python scripts/run.py --test-db

# Reinitialize database
python scripts/run.py --init-db
```

### Module Import Errors
```bash
# Check environment
python scripts/run.py --test-db

# Verify dependencies
pip list

# Reinstall if needed
pip install -r requirements.txt
```

## Examples

### Start Main Application
```bash
python scripts/run.py
# Opens at: http://localhost:8050
```

### Start Molecules Module Only
```bash
python scripts/run.py --module molecules
# Opens at: http://localhost:8050
```

### Database Operations
```bash
# Test database connection
python scripts/run.py --test-db

# Initialize fresh database
python scripts/run.py --init-db
```

### Development Workflow
```bash
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Test database
python scripts/run.py --test-db

# 3. Start development server
python scripts/run.py --module molecules

# 4. Open browser to http://localhost:8050
```

For more information, see the main project documentation and `SQLite_Migration_Guide.md`.