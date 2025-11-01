# Cheminf-EDU Quick Launcher for PowerShell
# This script activates the virtual environment and runs the application

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Cheminf-EDU Application Launcher" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan

# Change to project root directory
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    Read-Host "Press Enter to continue"
    exit 1
}

# Check if already in virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "Virtual environment already active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

Write-Host "Starting Cheminf-EDU..." -ForegroundColor Green
Write-Host ""

# Pass all arguments to the Python script
& python scripts\run.py @args

# Handle exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Application exited with error code: $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to close"
}