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

:: Create a shortcut with PowerShell and custom icon
echo $WshShell = New-Object -ComObject WScript.Shell > CreateShortcut.ps1
echo $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\WinFunct.lnk") >> CreateShortcut.ps1
echo $Shortcut.TargetPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" >> CreateShortcut.ps1
echo $Shortcut.Arguments = "-ExecutionPolicy Bypass -NoProfile -Command ""& '%~dp0Run.bat'""" >> CreateShortcut.ps1
echo $Shortcut.WorkingDirectory = "%~dp0" >> CreateShortcut.ps1
echo $Shortcut.IconLocation = "%~dp0WinFunct.ico" >> CreateShortcut.ps1
echo $Shortcut.Save() >> CreateShortcut.ps1
powershell.exe -ExecutionPolicy Bypass -File CreateShortcut.ps1
del CreateShortcut.ps1

:: Success message
echo.
echo.
echo ***********************************************
echo *                                             *
echo *    Installation/Update complete.            *
echo *                                             *
echo *    You can use the "Update WinFunct"        *
echo *    button in the App for future updates.    *
echo *                                             *
echo *    Thank you for using WinFunct :)          *
echo *                                             *
echo ***********************************************
echo.
echo Desktop Shortcut created.
echo Press any button to exit the WinFunct installer...
pause > nul 2>&1
exit /B 0
