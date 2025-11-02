# ChemINF-EDU Distribution

This directory contains the compiled distribution and build tools for ChemINF-EDU.

## Directory Structure

```
distribution/
├── ChemINF-EDU.exe          # Self-contained executable (created after build)
├── build_tools/             # Build configuration and scripts
│   ├── main.py             # PyInstaller entry point
│   ├── cheminf-edu.spec    # PyInstaller specification
│   └── build.bat           # Build automation script
└── docs/                   # Build documentation
    └── BUILD_INFO.md       # Detailed build information
```

## Building the Executable

From the project root directory, run:
```bash
distribution\build_tools\build.bat
```

Or from the build_tools directory:
```bash
cd distribution\build_tools
build.bat
```

## Running the Application

After building, you can run the executable in several ways:

### From Project Root (Recommended)
```bash
launch.bat
```

### Directly from Distribution Directory
```bash
cd distribution
ChemINF-EDU.exe
```

### Manual Launch
1. Navigate to the `distribution` folder
2. Double-click `ChemINF-EDU.exe`
3. Open your web browser to http://localhost:8050

## Build Requirements

- Python 3.8+ with all project dependencies installed
- PyInstaller (will be installed automatically if missing)
- Approximately 500MB free disk space for build process

## Distribution Size

The self-contained executable is approximately 200-300MB and includes:
- Python 3.12+ runtime
- All ChemINF-EDU modules and dependencies
- Web framework assets (Dash, Plotly, Flask)
- Static files and configuration

## Troubleshooting

- If the build fails, ensure all Python dependencies are installed
- For import errors, check that you're running from the correct directory
- The one-file executable is completely self-contained - no additional files needed

See `docs/BUILD_INFO.md` for detailed build configuration information.