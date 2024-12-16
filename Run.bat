@echo off
setlocal enabledelayedexpansion

:: BatchGotAdmin
title WinFunct Terminal

:-------------------------------------
:: Check for permissions
echo Verifying admin permissions...
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% NEQ 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python and add it to your system PATH.
    pause
    exit /B 1
)

:: Check if git is installed
where git >nul 2>nul
if %errorlevel% NEQ 0 (
    echo Git is not installed or not in the system PATH.
    python WinFunct.py
    exit /B 1
)

:: Attempt git pull with timeout
echo Checking for updates...
git pull > "%TEMP%\git_pull_output.txt" 2>&1
if %errorlevel% NEQ 0 (
    echo Update check failed.
    echo Continuing with application launch...
) else (
    findstr /C:"Already up to date." "%TEMP%\git_pull_output.txt" >nul
    if %errorlevel% NEQ 0 (
        echo Updates pulled. Installing new requirements...
        pip install -r requirements.txt
    ) else (
        echo No updates available.
    )
)

del "%TEMP%\git_pull_output.txt"

:: Check if the Python script exists
if not exist "WinFunct.py" (
    echo Error: WinFunct.py not found in the current directory.
    echo Please ensure the script is in the same folder as this batch file.
    pause
    exit /B 1
)

:: Running the Python script with admin privileges
echo Starting WinFunct application...
python WinFunct.py
if %errorlevel% NEQ 0 (
    echo Error: Failed to execute the Python application.
    echo Error code: %errorlevel%
    exit /B %errorlevel%
)

echo Python application executed successfully.
exit /B 0
