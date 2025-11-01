# Cheminf-EDU

ChemINF-EDU is a educational cheminformatics system designed to support a wide range of chemical data management tasks. It combines powerful user interfaces with robust RESTful APIs to provide seamless integration across various modules.

## 🚀 Quick Start

**Start the application in 3 easy steps:**

1. **Setup** (first time only):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it (Windows PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Install dependencies  
   pip install -r requirements.txt
   ```

2. **Run** the application:
   ```bash
   # Easy launcher (recommended)
   python scripts/run.py
   
   # Or use platform launchers
   .\scripts\run.ps1        # PowerShell
   scripts\run.bat          # Command Prompt  
   ```

3. **Open** your browser to: **http://localhost:8050**

## 📋 Modules

This platform offers the following modules:

* **Molecules**: Manage and view detailed information about chemical molecules with SMILES data
* **Inventory**: Track and manage chemical inventory data including amounts and storage details
* **Projects Maintenance**: Organize and monitor projects related to chemical research and analysis
* **Tasks Maintenance**: Manage individual tasks and workflows within larger projects
* **Reactions Maintenance**: Define, view, and update chemical reaction data and kinetics
* **Reaction Participants Maintenance**: Oversee reaction components including reactants, products, and catalysts with their respective stoichiometric details
* **Reaction Overview**: Generate comprehensive overviews and chemical equations from aggregated reaction data
* **REST API**: Leverage a suite of RESTful endpoints for easy integration, automation, and data sharing across various applications

## 🗄️ Database

**SQLite Database** (Zero Configuration Required):
- **Location**: `cheminf_edu.db` (automatically created)
- **Tables**: 9 tables with sample chemistry data
- **Data**: 40 molecules, reactions, inventory, experiments, and more
- **Backup**: Simply copy the `.db` file

## 🛠️ Advanced Usage

```bash
# Start specific modules
python scripts/run.py --module molecules
python scripts/run.py --module reactions
python scripts/run.py --module inventory

# Database operations  
python scripts/run.py --test-db      # Test database
python scripts/run.py --init-db      # Initialize database

# Get help
python scripts/run.py --help
```

## 📁 Project Structure

```
cheminf-edu/
├── cheminf/                 # Main application package
│   ├── db/                  # Database layer (SQLite)
│   ├── molecules/           # Molecule management
│   ├── reactions/           # Chemical reactions  
│   ├── inventory/           # Chemical inventory
│   ├── lims_experiments/    # Laboratory experiments
│   └── projects/            # Project management
├── scripts/                 # Launcher scripts
│   ├── run.py              # Main launcher (Python)
│   ├── run.ps1             # PowerShell launcher
│   └── run.bat             # Windows batch launcher
├── cheminf_edu.db          # SQLite database (auto-created)
└── requirements.txt        # Python dependencies
```

![image](https://github.com/user-attachments/assets/94137914-9bfa-4b01-b835-911885278c1e)
