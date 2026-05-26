@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title WinFunct Terminal

:: Check admin
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Requesting admin privileges...
    PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit
)

:: Check Python
where python >nul 2>nul
if %errorlevel% NEQ 0 (
    echo Python not found in PATH. Please install Python 3.10+.
    pause
    exit /B 1
)

:: Check Git & update
where git >nul 2>nul
if %errorlevel% EQU 0 (
    echo Checking for updates...
    git fetch origin main >nul 2>&1
    git rev-parse HEAD > "%TEMP%\wf_local.txt"
    git rev-parse origin/main > "%TEMP%\wf_remote.txt"
    fc "%TEMP%\wf_local.txt" "%TEMP%\wf_remote.txt" >nul 2>&1
    if %errorlevel% NEQ 0 (
        echo Pulling updates...
        git pull
        pip install -r requirements.txt >nul
    ) else (
        echo Up to date.
    )
    del "%TEMP%\wf_local.txt" "%TEMP%\wf_remote.txt" 2>nul
)

:: Launch
if not exist "main.py" (
    echo Error: main.py not found.
    pause
    exit /B 1
)

echo Starting WinFunct...
python main.py
exit /B 0
