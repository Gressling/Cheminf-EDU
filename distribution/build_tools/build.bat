@echo off
echo =================================================================
echo ChemINF-EDU Build Script
echo =================================================================
echo.

REM Change to the project root directory (parent of distribution)
cd /d "%~dp0\..\..\"
set PROJECT_ROOT=%CD%

echo Project root: %PROJECT_ROOT%
echo Distribution tools: %PROJECT_ROOT%\distribution\build_tools
echo.

REM Activate virtual environment
echo Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
    echo Virtual environment activated
) else (
    echo WARNING: Virtual environment not found at venv\Scripts\activate.bat
    echo Checking if Python is available in PATH...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python is not available and no virtual environment found
        echo Please either:
        echo   1. Create a virtual environment: python -m venv venv
        echo   2. Install Python and add it to PATH
        pause
        exit /b 1
    )
)

echo Python version:
python --version
echo.

REM Check if PyInstaller is available, install if needed
echo Checking PyInstaller installation...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install PyInstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
) else (
    echo PyInstaller is already installed
)
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "distribution\ChemINF-EDU.exe" del "distribution\ChemINF-EDU.exe"
if exist "distribution\_internal" rmdir /s /q "distribution\_internal"
echo.

REM Run PyInstaller with the spec file
echo Building executable...
pyinstaller "distribution\build_tools\cheminf-edu.spec" --noconfirm
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

REM Move the built files to the distribution directory
echo Organizing distribution files...
if exist "dist\ChemINF-EDU.exe" (
    move "dist\ChemINF-EDU.exe" "distribution\ChemINF-EDU.exe"
    echo.
    echo SUCCESS: One-file executable built and organized successfully!
    echo Location: %PROJECT_ROOT%\distribution\ChemINF-EDU.exe
    echo Size: 
    dir "distribution\ChemINF-EDU.exe" | findstr "ChemINF-EDU.exe"
    echo.
    echo Note: This is a ONE-FILE executable - no _internal directory needed!
) else (
    echo ERROR: Build completed but executable not found
    echo Checking for one-folder output...
    if exist "dist\ChemINF-EDU\ChemINF-EDU.exe" (
        echo Found one-folder output instead of one-file
        move "dist\ChemINF-EDU\ChemINF-EDU.exe" "distribution\ChemINF-EDU.exe"
        if exist "dist\ChemINF-EDU\_internal" (
            move "dist\ChemINF-EDU\_internal" "distribution\_internal"
        )
    ) else (
        echo No executable found in either format
        exit /b 1
    )
)

REM Clean temporary build directories
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo =================================================================
echo Build completed successfully!
echo Executable: distribution\ChemINF-EDU.exe
echo Documentation: distribution\docs\
echo Build tools: distribution\build_tools\
echo =================================================================
pause