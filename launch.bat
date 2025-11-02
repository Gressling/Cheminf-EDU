@echo off
echo =================================================================
echo ChemINF-EDU Launcher
echo =================================================================
echo.

REM Check if distribution directory exists
if not exist "distribution\ChemINF-EDU.exe" (
    echo ERROR: ChemINF-EDU executable not found!
    echo.
    echo To build the executable, run:
    echo   distribution\build_tools\build.bat
    echo.
    pause
    exit /b 1
)

echo Starting ChemINF-EDU...
echo Navigate to: http://localhost:8050 after startup
echo Press Ctrl+C to stop the server
echo.

cd distribution
start ChemINF-EDU.exe
echo.
echo ChemINF-EDU is starting...
echo Check http://localhost:8050 in your web browser
pause