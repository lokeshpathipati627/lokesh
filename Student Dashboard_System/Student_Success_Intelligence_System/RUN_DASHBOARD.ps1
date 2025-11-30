#!/usr/bin/env powershell

# ============================================================================
# STUDENT SUCCESS INTELLIGENCE SYSTEM - QUICK START SCRIPT
# ============================================================================
# 
# This script automates the setup and execution of the Student Dashboard
#
# Usage: .\RUN_DASHBOARD.ps1
#
# ============================================================================

param(
    [switch]$SkipVenv = $false,
    [switch]$SkipInstall = $false,
    [switch]$Port = 8501
)

# Colors for console output
$Colors = @{
    Green = [System.ConsoleColor]::Green
    Yellow = [System.ConsoleColor]::Yellow
    Red = [System.ConsoleColor]::Red
    Cyan = [System.ConsoleColor]::Cyan
}

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $color = $Colors.Cyan
    if ($Status -eq "SUCCESS") { $color = $Colors.Green }
    if ($Status -eq "ERROR") { $color = $Colors.Red }
    if ($Status -eq "WARNING") { $color = $Colors.Yellow }
    
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] [$Status] " -ForegroundColor $color -NoNewline
    Write-Host $Message
}

# ============================================================================
# STEP 1: CHECK PYTHON
# ============================================================================

Write-Status "Checking Python installation..." "INFO"

try {
    $pythonVersion = python --version 2>&1
    Write-Status "Found: $pythonVersion" "SUCCESS"
} catch {
    Write-Status "Python not found! Please install Python 3.8+: https://python.org" "ERROR"
    exit 1
}

# ============================================================================
# STEP 2: NAVIGATE TO PROJECT DIRECTORY
# ============================================================================

Write-Status "Setting up project directory..." "INFO"

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

Write-Status "Working directory: $projectPath" "SUCCESS"

# ============================================================================
# STEP 3: CREATE VIRTUAL ENVIRONMENT
# ============================================================================

if (-not $SkipVenv) {
    Write-Status "Creating virtual environment..." "INFO"
    
    if (-not (Test-Path "venv")) {
        python -m venv venv
        Write-Status "Virtual environment created" "SUCCESS"
    } else {
        Write-Status "Virtual environment already exists" "SUCCESS"
    }

    # Activate virtual environment
    Write-Status "Activating virtual environment..." "INFO"
    & ".\venv\Scripts\Activate.ps1"
    Write-Status "Virtual environment activated" "SUCCESS"
} else {
    Write-Status "Skipping virtual environment setup" "WARNING"
}

# ============================================================================
# STEP 4: INSTALL DEPENDENCIES
# ============================================================================

if (-not $SkipInstall) {
    Write-Status "Installing dependencies from requirements.txt..." "INFO"
    
    pip install -r requirements.txt --quiet
    
    Write-Status "Dependencies installed successfully" "SUCCESS"
} else {
    Write-Status "Skipping dependency installation" "WARNING"
}

# ============================================================================
# STEP 5: VERIFY DATA FILES
# ============================================================================

Write-Status "Verifying data files..." "INFO"

if (Test-Path "data\student_performance_dataset.csv") {
    Write-Status "Found CSV data file" "SUCCESS"
} else {
    Write-Status "CSV not found - app will use mock data" "WARNING"
}

# ============================================================================
# STEP 6: RUN STREAMLIT APP
# ============================================================================

Write-Status "Starting Streamlit application..." "INFO"
Write-Status "Dashboard will open at http://localhost:$Port" "INFO"
Write-Status "Press Ctrl+C to stop the server" "WARNING"

Write-Host "`n" 

streamlit run app.py --server.port $Port

# ============================================================================
# CLEANUP
# ============================================================================

Write-Status "Application stopped" "INFO"
