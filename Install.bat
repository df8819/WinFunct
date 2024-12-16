@echo off
setlocal enabledelayedexpansion

:: Change to the script's directory
cd /d "%~dp0"

:: Initialize error level variable
set "LAST_ERROR=0"

:: Check if Git is installed
git --version >nul 2>&1
set "LAST_ERROR=!errorlevel!"
if !LAST_ERROR! NEQ 0 (
    echo Error: Git is not installed or not in the system PATH.
    pause
    exit /B 2
)

:: Pull the latest updates from Git
echo Pulling latest updates from Git...
git pull
set "LAST_ERROR=!errorlevel!"
if !LAST_ERROR! NEQ 0 (
    echo Error: Failed to pull updates from Git. Please check your network connection and repository status.
    pause
    exit /B 1
)

:: Check if Python is installed
python --version >nul 2>&1
set "LAST_ERROR=!errorlevel!"
if !LAST_ERROR! NEQ 0 (
    echo Error: Python is not installed or not in the system PATH.
    pause
    exit /B 3
)

:: Install required Python packages
echo Installing required Python packages...
pip install -r requirements.txt
set "LAST_ERROR=!errorlevel!"
if !LAST_ERROR! NEQ 0 (
    echo Error: Failed to install required Python packages. Please check your Python environment and requirements.txt file.
    pause
    exit /B 1
)

:: Create PowerShell script to create shortcut
set "PS_SCRIPT=CreateShortcut.ps1"
(
    echo $WshShell = New-Object -ComObject WScript.Shell
    echo $DesktopPath = [Environment]::GetFolderPath('Desktop'^)
    echo $ShortcutPath = Join-Path -Path $DesktopPath -ChildPath 'WinFunct.lnk'
    echo $Shortcut = $WshShell.CreateShortcut($ShortcutPath^)
    echo $Shortcut.TargetPath = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
    echo $Shortcut.Arguments = "-ExecutionPolicy Bypass -NoProfile -Command ""& '$PSScriptRoot\Run.bat'"""
    echo $Shortcut.WorkingDirectory = $PSScriptRoot
    echo $Shortcut.IconLocation = "$PSScriptRoot\WinFunct.ico"
    echo $Shortcut.Save(^)
) > "%PS_SCRIPT%"

:: Execute PowerShell script to create shortcut
powershell.exe -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
set "LAST_ERROR=!errorlevel!"

:: Clean up temporary PowerShell script
if exist "%PS_SCRIPT%" del "%PS_SCRIPT%"

if !LAST_ERROR! NEQ 0 (
    echo Error: Failed to create desktop shortcut.
    pause
    exit /B 1
)

:: Success message
echo.
echo.
echo ***********************************************
echo *                                             *
echo *    Installation/Update complete.            *
echo *                                             *
echo *    Thank you for using WinFunct :)          *
echo *                                             *
echo ***********************************************
echo.
echo Desktop Shortcut created.
echo Press any key to exit the WinFunct installer...
pause > nul 2>&1
exit /B 0
