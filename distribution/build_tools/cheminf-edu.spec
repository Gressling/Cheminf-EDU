# -*- mode: python ; coding: utf-8 -*-
"""
ChemINF-EDU PyInstaller Specification File
==========================================

This specification file defines how to build ChemINF-EDU into a standalone
Windows executable using PyInstaller.

Build Command:
    pyinstaller cheminf-edu.spec --clean --noconfirm

Output:
    - Executable: dist/ChemINF-EDU/ChemINF-EDU.exe
    - Dependencies: dist/ChemINF-EDU/_internal/
    - Size: ~200MB (includes Python runtime + all dependencies)
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Project configuration
PROJECT_NAME = "ChemINF-EDU"
PROJECT_VERSION = "2.0"
PROJECT_DESCRIPTION = "Chemical Informatics Educational Platform"

# Get the path to the project (navigate up from distribution/build_tools to project root)
spec_dir = os.path.dirname(os.path.abspath(SPEC))
project_path = os.path.dirname(os.path.dirname(spec_dir))
print(f"Building {PROJECT_NAME} v{PROJECT_VERSION}")
print(f"Spec directory: {spec_dir}")
print(f"Project path: {project_path}")

# Add project root to Python path for imports
sys.path.insert(0, project_path)

# ============================================================================
# DATA FILES COLLECTION
# ============================================================================

datas = []

print("Collecting data files...")

# Dash and Plotly web framework assets
print("  - Dash framework assets")
datas += collect_data_files('dash')
datas += collect_data_files('plotly')

# Note: dash_core_components, dash_html_components, dash_table are now part of dash
# The collect_data_files calls for these generate warnings but don't break the build

# ChemINF application files
print("  - ChemINF static assets")
cheminf_static_path = os.path.join(project_path, 'cheminf', 'static')
if os.path.exists(cheminf_static_path):
    datas += [(cheminf_static_path, 'cheminf/static')]

# Database file (if exists)
print("  - Database file")
db_path = os.path.join(project_path, 'cheminf_edu.db')
if os.path.exists(db_path):
    datas += [(db_path, '.')]
    print(f"    Database found: {db_path}")
else:
    print("    Database not found - will be created on first run")

# Configuration files
print("  - Configuration files")
config_files = ['settings.json', 'swagger.yaml']
for config_file in config_files:
    config_path = os.path.join(project_path, config_file)
    if os.path.exists(config_path):
        datas += [(config_path, '.')]
        print(f"    Added: {config_file}")
    else:
        print(f"    Missing: {config_file}")

# Documentation files
print("  - Documentation")
doc_files = ['README.md', 'LICENSE', 'BUILD_SUMMARY.md']
for doc_file in doc_files:
    doc_path = os.path.join(project_path, doc_file)
    if os.path.exists(doc_path):
        datas += [(doc_path, '.')]
        print(f"    Added: {doc_file}")

print(f"Total data files collected: {len(datas)}")

# ============================================================================
# HIDDEN IMPORTS
# ============================================================================

print("Configuring hidden imports...")

hiddenimports = []

# Core web framework components
print("  - Web framework modules")
web_framework_imports = [
    'dash.dependencies',
    'dash._callback',
    'dash._utils',
    'dash.exceptions',
    'flask.helpers',
    'flask.json.provider',
    'werkzeug.serving',
    'werkzeug.security',
    'jinja2.ext',
]

# Plotly visualization modules
print("  - Plotly visualization modules")
plotly_imports = [
    'plotly.graph_objects',
    'plotly.express',
    'plotly.io',
    'plotly.colors',
    'plotly.figure_factory',
    'plotly.subplots',
]

# Data processing and analysis
print("  - Data processing modules")
data_processing_imports = [
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.tslibs.timezones',
    'pandas.io.formats.format',
    'numpy.core._methods',
    'numpy.lib.format',
]

# Database and I/O
print("  - Database and I/O modules")
database_imports = [
    'sqlite3',
    'json',
    'csv',
    'io',
    'xml.etree.ElementTree',
    'xml.dom.minidom',
]

# ChemINF application modules
print("  - ChemINF application modules")
cheminf_modules = [
    # Core application
    'cheminf.app',
    'cheminf.app_server',
    'cheminf.config',
    
    # Database layer
    'cheminf.db.db',
    'cheminf.db.init_sqlite',
    
    # Molecules module
    'cheminf.molecules.molecules',
    'cheminf.molecules.rest_api',
    'cheminf.molecules.ui',
    
    # Inventory module
    'cheminf.inventory.rest_api',
    'cheminf.inventory.ui',
    
    # Projects module
    'cheminf.projects.rest_api',
    'cheminf.projects.ui_projects',
    'cheminf.projects.ui_tasks',
    
    # Reactions module
    'cheminf.reactions.rest_api',
    'cheminf.reactions.ui_reactions',
    'cheminf.reactions.ui_reactionparticipants',
    'cheminf.reactions.ui_overview',
    
    # LIMS module
    'cheminf.lims_experiments.rest_api',
    'cheminf.lims_experiments.ui_experiments',
    'cheminf.lims_experiments.ui_samples',
    'cheminf.lims_experiments.ui_measurements',
    
    # Time series module
    'cheminf.time_series.rest_api',
    'cheminf.time_series.ui_timeseries',
]

# Combine all imports
hiddenimports = (
    web_framework_imports +
    plotly_imports +
    data_processing_imports +
    database_imports +
    cheminf_modules
)

print(f"Total hidden imports: {len(hiddenimports)}")

# Optional imports that may not be present (don't fail if missing)
optional_imports = [
    'engineio.async_drivers.threading',
    'pandas._libs.skiplist',
]

for opt_import in optional_imports:
    try:
        __import__(opt_import)
        hiddenimports.append(opt_import)
        print(f"  - Added optional import: {opt_import}")
    except ImportError:
        print(f"  - Skipped missing optional import: {opt_import}")

# ============================================================================
# EXCLUDED MODULES
# ============================================================================

print("Configuring excluded modules...")

# Exclude modules that are not needed to reduce executable size
excludes = [
    # GUI frameworks not used
    'tkinter', 'tk', 'tcl',
    
    # Development and testing tools
    'matplotlib', 'IPython', 'jupyter', 'notebook',
    'sphinx', 'pytest', 'unittest2',
    'setuptools', 'pip', 'wheel',
    
    # Documentation tools
    'pydoc', 'doctest',
    
    # Optional scientific packages not used
    'scipy', 'sklearn', 'seaborn',
    
    # Large packages we don't need
    'PIL.ImageTk', 'PIL.ImageQt',
]

print(f"Excluding {len(excludes)} modules to reduce size")

# ============================================================================
# PYINSTALLER ANALYSIS CONFIGURATION
# ============================================================================

print(f"\nConfiguring PyInstaller Analysis for {PROJECT_NAME}...")

block_cipher = None

a = Analysis(
    # Entry point (relative to spec directory)
    [os.path.join(spec_dir, 'main.py')],
    
    # Python path
    pathex=[project_path],
    
    # Binary files (none for this project)
    binaries=[],
    
    # Data files
    datas=datas,
    
    # Hidden imports
    hiddenimports=hiddenimports,
    
    # Hook paths (none needed)
    hookspath=[],
    
    # Hook configuration
    hooksconfig={},
    
    # Runtime hooks (none needed)
    runtime_hooks=[],
    
    # Modules to exclude
    excludes=excludes,
    
    # Windows-specific settings
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    
    # Security
    cipher=block_cipher,
    
    # Archive settings
    noarchive=False,
)

# ============================================================================
# BUILD CONFIGURATION
# ============================================================================

print("Configuring build settings...")

# Create Python ZIP archive
print("  - Creating Python ZIP archive")
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Configure executable
print(f"  - Configuring {PROJECT_NAME} executable (ONE-FILE)")
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,                        # Include binaries for one-file
    a.zipfiles,                        # Include zip files for one-file  
    a.datas,                           # Include data files for one-file
    [],
    name=PROJECT_NAME,
    debug=False,                        # Set to True for debugging
    bootloader_ignore_signals=False,
    strip=False,                        # Keep debug symbols for now
    upx=True,                          # Enable UPX compression
    console=True,                      # Keep console for logging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,                         # TODO: Add icon file if available
    version_info=None,                 # TODO: Add version info if available
)

# Note: COLLECT is not needed for one-file distribution
# One-file executable is created directly by EXE()

# ============================================================================
# BUILD SUMMARY
# ============================================================================

print(f"""
{'='*60}
{PROJECT_NAME} PyInstaller Build Configuration
{'='*60}

Project: {PROJECT_DESCRIPTION}
Version: {PROJECT_VERSION}
Entry Point: main.py

Output Structure:
  dist/{PROJECT_NAME}/
  ├── {PROJECT_NAME}.exe          # Main executable
  ├── _internal/                  # Dependencies
  │   ├── base_library.zip        # Python stdlib
  │   ├── *.dll                   # System libraries
  │   └── [package files]         # Application dependencies
  └── [data files]                # Config, docs, database

Build Features:
  ✓ One-folder distribution
  ✓ UPX compression enabled
  ✓ Console mode (for logging)
  ✓ All ChemINF modules included
  ✓ Web assets bundled
  ✓ Database included (if present)
  ✓ Configuration files included

Build Command:
  pyinstaller cheminf-edu.spec --clean --noconfirm

{'='*60}
""")