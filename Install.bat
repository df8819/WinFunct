@echo off
setlocal enabledelayedexpansion

:: Change to the script's directory
cd /d "%~dp0"

:: Check if Git is installed
git --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: Git is not installed or not in the system PATH.
    pause
    exit /B 2
)

:: Pull the latest updates from Git
echo Pulling latest updates from Git...
git pull
if %errorlevel% NEQ 0 (
    echo Error: Failed to pull updates from Git. Please check your network connection and repository status.
    pause
    exit /B 1
)

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: Python is not installed or not in the system PATH.
    pause
    exit /B 3
)

:: Install required Python packages
echo Installing required Python packages...
pip install -r requirements.txt
if %errorlevel% NEQ 0 (
    echo Error: Failed to install required Python packages. Please check your Python environment and requirements.txt file.
    pause
    exit /B 1
)

:: Success message
echo.
echo.
echo -------------------------------------------
echo Installation/Update complete.
echo.
echo You can use the "Update" button in the App 
echo for future updates.
echo.
echo Thank you for using WinFunct :)
echo -------------------------------------------
echo.
timeout /t 30
exit /B 0
