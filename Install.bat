@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: Check Git
git --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: Git is not installed or not in PATH.
    pause
    exit /B 1
)

:: Pull latest
echo Pulling latest updates...
git pull
if %errorlevel% NEQ 0 (
    echo Error: git pull failed.
    pause
    exit /B 1
)

:: Check Python
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /B 1
)

:: Install deps
echo Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% NEQ 0 (
    echo Error: pip install failed.
    pause
    exit /B 1
)

:: Desktop shortcut
echo.
set /p CREATE_SHORTCUT="Create a Desktop Shortcut? (y/n): "
if /i "%CREATE_SHORTCUT%" NEQ "y" goto Done

powershell -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'WinFunct.lnk')); $s.TargetPath = '%~dp0Run.bat'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0WinFunct.ico'; $s.Save()"

if %errorlevel% NEQ 0 (
    echo Failed to create shortcut.
) else (
    echo Shortcut created.
)

:Done
echo.
echo Installation complete.
pause
exit /B 0
