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
set /p "version=Enter the version number (e.g., v1.234) and hit Enter: "
if "!version!"=="" (
    echo Version number cannot be empty.
    goto version_prompt
)

REM Prompt to rename the default name
set "newname=WinFunct"
set /p "rename_choice=Would you like to rename the default 'WinFunct' name? (y/n): "
if /i "!rename_choice!"=="y" (
    :rename_prompt
    set "newname="
    set /p "newname=Enter a new name for the app: "
    if "!newname!"=="" (
        echo Name cannot be empty.
        goto rename_prompt
    )
)

:option_prompt
REM Prompt for pyinstaller process option with default [2]
set "option=2"
echo.
echo ================================================================================
echo Please choose a PyInstaller process (Default is [2]):
echo.
echo [1] Includes a Python script to create and modify the spec file with exclusions.
echo [2] Runs pyinstaller without exclusions and only with the "--onefile" argument.
echo.
set /p "option=Type [1] or [2] and hit Enter: "
echo.
REM Default to 2 if the input is empty
if "%option%"=="" set "option=2"

REM Get start time
for /F "tokens=1-4 delims=:.," %%a in ("!time!") do (
    set /a start_time=%%a*3600 + %%b*60 + %%c
)

REM Validate the input and execute the appropriate PyInstaller command
if "%option%"=="1" (
    REM Create the spec file with the necessary exclusions using a Python script
    echo Creating the spec file with exclusions...
    python create_spec_file.py
    echo Compiling WinFunct.py into a single executable using PyInstaller with the spec file...
    pyinstaller WinFunct.spec
) else if "%option%"=="2" (
    echo Compiling WinFunct.py into a single executable using PyInstaller without spec file...
    pyinstaller --onefile --icon=WinFunct.ico WinFunct.py
) else (
    echo Invalid entry! Please select [1] or [2].
    goto option_prompt
)

if %errorlevel% NEQ 0 (
    echo Error: PyInstaller failed to compile the script. Please check the output for details.
    pause
    exit /B 1
)

REM Get end time
for /F "tokens=1-4 delims=:.," %%a in ("!time!") do (
    set /a end_time=%%a*3600 + %%b*60 + %%c
)

REM Calculate elapsed time
set /a elapsed_time=end_time-start_time

REM Move the generated executable to the root folder and rename it with the defined name and version
echo Moving the generated executable to the root folder...
if exist "!newname!_%version%.exe" (
    echo Warning: !newname!_%version%.exe already exists. Overwriting...
    del /F "!newname!_%version%.exe"
)

move /Y "dist\WinFunct.exe" "!newname!_%version%.exe"
if %errorlevel% NEQ 0 (
    echo Error: Failed to move and rename the executable to the root folder.
    pause
    exit /B 1
)

REM Clean up
echo Cleaning up temporary files and folders...
timeout /t 1 > nul
if exist dist rmdir /S /Q dist
if exist build rmdir /S /Q build

:retry
if exist __pycache__ (
    echo Attempting to delete __pycache__ again...
    rmdir /S /Q __pycache__
    timeout /t 1 > nul
    goto retry
)
if exist WinFunct.spec del /F WinFunct.spec

echo.
echo.
echo ===========================================================
echo Compilation complete. Process took %elapsed_time% seconds.
echo.
echo !newname!_%version%.exe created and moved to root directory.
echo The following has been cleaned up:
echo.
echo dist/
echo build/
echo __pycache__/
echo WinFunct.spec
echo ===========================================================
echo.
echo Press any key to exit...
pause > nul
exit /B 0
