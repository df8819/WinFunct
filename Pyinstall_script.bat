@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: Admin check
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /B
)

:: Validate
if not exist "main.py" (
    echo Error: main.py not found.
    pause
    exit /B 1
)

:: Version
:version_prompt
set /p "version=Version number (e.g. v2.000): "
if "!version!"=="" goto version_prompt

:: Name
set "appname=WinFunct"
set /p "rename=Rename from 'WinFunct'? (y/n): "
if /i "!rename!"=="y" (
    set /p "appname=New name: "
)

:: Zip option
set /p "zip=Create zip archive? (y/n): "

:: Build
echo.
echo Compiling...
pip install pyinstaller >nul 2>&1

pyinstaller --clean --noconfirm --onefile ^
    --icon=WinFunct.ico ^
    --add-data "WinFunct.ico;." ^
    --add-data "UI_themes.json;." ^
    --add-data "gui;gui" ^
    --add-data "core;core" ^
    --add-data "config.py;." ^
    --name "!appname!" ^
    main.py

if %errorlevel% NEQ 0 (
    echo Build failed.
    pause
    exit /B 1
)

:: Move & rename
move /Y "dist\!appname!.exe" "!appname!_!version!.exe"

:: Zip
if /i "!zip!"=="y" (
    powershell -Command "Compress-Archive -Path '.\!appname!_!version!.exe' -DestinationPath '.\!appname!_!version!.zip' -Force"
)

:: Cleanup
rmdir /S /Q dist build 2>nul
del /F /Q *.spec 2>nul

echo.
echo Done: !appname!_!version!.exe
pause
exit /B 0
