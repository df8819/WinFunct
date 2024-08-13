@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: Python is not installed or not in the system PATH.
    pause
    exit /B 1
)

REM Check if pyinstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: PyInstaller is not installed. Please install it using 'pip install pyinstaller'.
    pause
    exit /B 1
)

REM Prompt for version number with validation
:version_prompt
set "version="
set /p "version=Enter the version number (e.g., v1.234): "
if "!version!"=="" (
    echo Version number cannot be empty.
    goto version_prompt
)

REM Create the spec file with the necessary exclusions using a Python script
echo Creating the spec file with exclusions...
python create_spec_file.py
if %errorlevel% NEQ 0 (
    echo Error: Failed to create the spec file.
    pause
    exit /B 1
)

echo Compiling WinFunct.py into a single executable using PyInstaller with the spec file...
pyinstaller WinFunct.spec
if %errorlevel% NEQ 0 (
    echo Error: PyInstaller failed to compile the script. Please check the output for details.
    pause
    exit /B 1
)

REM Move the generated executable to the root folder and rename it with the version number
echo Moving the generated executable to the root folder...
if exist "WinFunct_%version%.exe" (
    echo Warning: WinFunct_%version%.exe already exists. Overwriting...
    del /F "WinFunct_%version%.exe"
)
move /Y "dist\WinFunct.exe" "WinFunct_%version%.exe"
if %errorlevel% NEQ 0 (
    echo Error: Failed to move and rename the executable to the root folder.
    pause
    exit /B 1
)

REM Clean up
echo Cleaning up temporary files and folders...
if exist dist rmdir /S /Q dist
if exist build rmdir /S /Q build
if exist __pycache__ rmdir /S /Q __pycache__
if exist WinFunct.spec del /F WinFunct.spec

echo.
echo --------------------------------------------------------------------------
echo Compilation complete. The file has been renamed to WinFunct_%version%.exe.
echo Please manually close this window.
echo --------------------------------------------------------------------------
echo.
pause

endlocal
