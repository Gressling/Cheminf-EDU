@echo off
REM Cheminf-EDU Quick Launcher for Windows
REM This batch file activates the virtual environment and runs the application

echo ================================================
echo Cheminf-EDU Application Launcher
echo ================================================

REM Change to project root directory
cd /d "%~dp0\.."

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please create virtual environment first:
    echo   python -m venv venv
    echo   .\venv\Scripts\Activate.ps1
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment and run application
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Cheminf-EDU...
echo.
python scripts\run.py %*

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Press any key to close...
    pause > nul
)