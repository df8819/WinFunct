@echo off
setlocal enabledelayedexpansion

:: Ensure the batch file runs in its own directory
cd /d "%~dp0"

:: BatchGotAdmin
title WinFunct Terminal

:: Check for admin permissions
echo Verifying admin permissions...
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Requesting administrative privileges...
    PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit
)

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% NEQ 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python and add it to your system PATH.
    exit 1
)

:: Check if git is installed
where git >nul 2>nul
if %errorlevel% NEQ 0 (
    echo Git is not installed or not in the system PATH.
    start "" pythonw WinFunct.py
    exit 1
)

:: Update checking
echo Checking for updates...
git fetch origin main >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Update check failed.
    echo Continuing with application launch...
    goto StartApp
)

git rev-parse HEAD > "%TEMP%\current_commit.txt"
git rev-parse origin/main > "%TEMP%\remote_commit.txt"

fc "%TEMP%\current_commit.txt" "%TEMP%\remote_commit.txt" >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Updates found. Pulling changes...
    git pull
    if %errorlevel% EQU 0 (
        echo Updates installed successfully.
        pip install -r requirements.txt
    ) else (
        echo Failed to pull updates.
    )
) else (
    echo No updates available.
)

del "%TEMP%\current_commit.txt" 2>nul
del "%TEMP%\remote_commit.txt" 2>nul

:StartApp

:: Check if the Python script exists
if not exist "WinFunct.py" (
    echo Error: WinFunct.py not found in the current directory.
    echo Please ensure the script is in the same folder as this batch file.
    exit 1
)

:: Running the Python script with admin privileges
echo Starting WinFunct application...
echo.
echo ...You can close this window now
start "" pythonw WinFunct.py
if %errorlevel% NEQ 0 (
    echo Error: Failed to execute the Python application.
    echo Error code: %errorlevel%
    exit %errorlevel%
)

:: Force-close this window, even if launched by double-click
exit
