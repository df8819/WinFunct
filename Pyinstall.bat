@echo off
cd %~dp0

REM Check if pyinstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Error: PyInstaller is not installed. Please install it using 'pip install pyinstaller'.
    pause
    exit /B 1
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

REM Move the generated executable to the root folder
echo Moving the generated executable to the root folder...
move /Y dist\WinFunct\WinFunct.exe .
if %errorlevel% NEQ 0 (
    echo Error: Failed to move the executable to the root folder.
    pause
    exit /B 1
)

REM Delete the dist folder
echo Deleting the dist folder...
rmdir /S /Q dist

REM Clean up temporary files
echo Cleaning up temporary files...
rmdir /S /Q build
rmdir /S /Q __pycache__

echo -------INFO------- Compilation complete. Please manually close this window. -------INFO-------
pause
