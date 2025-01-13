@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check for admin rights
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Requesting administrative privileges...
    PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /B
)

REM Check Python version
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set "pyver=%%a"
if "%pyver:~0,1%" LSS "3" (
    echo Error: Python 3.x is required ^(Found version: %pyver%^)
    pause
    exit /B 1
)

REM Check if pyinstaller is installed and get version
for /f "tokens=2 delims= " %%a in ('pyinstaller --version 2^>^&1') do set "pyinstver=%%a"
if %errorlevel% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if !errorlevel! NEQ 0 (
        echo Error: Failed to install PyInstaller.
        pause
        exit /B 1
    )
)

REM Validate required files exist
if not exist "WinFunct.py" (
    echo Error: WinFunct.py not found in current directory.
    pause
    exit /B 1
)
if not exist "WinFunct.ico" (
    echo Error: WinFunct.ico not found in current directory.
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

REM Add zip archive prompt here
set /p "zip_choice=Would you like to create a zip archive of the executable? (y/n): "

:option_prompt
REM Prompt for pyinstaller process option with default [1]
set "option=1"
echo.
echo ================================================================================
echo Please choose a PyInstaller process (Default is [1]):
echo.
echo [1] Includes a Python script to create and modify the spec file with exclusions.
echo [2] Runs pyinstaller without exclusions and only with the "--onefile" argument.
echo.
set /p "option=Type [1] or [2] and hit Enter: "
echo.
REM Default to 1 if the input is empty
if "%option%"=="" set "option=1"

REM Get start time
for /F "tokens=1-4 delims=:.," %%a in ("!time!") do (
    set /a start_time=%%a*3600 + %%b*60 + %%c
)

REM Validate the input and execute the appropriate PyInstaller command
if "%option%"=="1" (
    echo Creating the spec file with exclusions...
    set "APP_NAME=!newname!"
    python create_spec_file.py
    echo Compiling WinFunct.py into a single executable...
    pyinstaller --clean ^
                --log-level INFO ^
                --noconfirm ^
                WinFunct.spec
) else if "%option%"=="2" (
    echo Compiling WinFunct.py into a single executable...
    pyinstaller --clean ^
                --log-level INFO ^
                --noconfirm ^
                --onefile ^
                --icon=WinFunct.ico ^
                --add-data "WinFunct.ico;." ^
                --name "!newname!" ^
                WinFunct.py
)

REM Add error log creation if PyInstaller fails
if %errorlevel% NEQ 0 (
    echo Error: PyInstaller failed to compile the script.
    echo Creating error log...
    pyinstaller --clean --onefile WinFunct.py > pyinstaller_error.log 2>&1
    echo Error log created as pyinstaller_error.log
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

if "%option%"=="1" (
    move /Y "dist\WinFunct.exe" "!newname!_%version%.exe"
) else (
    move /Y "dist\!newname!.exe" "!newname!_%version%.exe"
)

if %errorlevel% NEQ 0 (
    echo Error: Failed to move and rename the executable to the root folder.
    pause
    exit /B 1
)

REM Create zip archive if requested
if /i "!zip_choice!"=="y" (
    echo Creating zip archive...
    powershell -Command "Compress-Archive -Path '.\!newname!_%version%.exe' -DestinationPath '.\!newname!_%version%.zip' -Force"
    if !errorlevel! EQU 0 (
        echo Zip archive created successfully: !newname!_%version%.zip
    ) else (
        echo Failed to create zip archive using PowerShell.
    )
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

REM Additional cleanup
echo Cleaning up additional files...
del /F /Q *.pyc 2>nul
del /F /Q *.pyo 2>nul
del /F /Q *.log 2>nul

REM Verify the executable was created successfully
if not exist "!newname!_%version%.exe" (
    echo Error: Executable was not created successfully.
    pause
    exit /B 1
)

echo.
echo.
echo ===========================================================
echo Compilation complete. Process took %elapsed_time% seconds.
echo.
echo !newname!_%version%.exe created and moved to root directory.
if /i "!zip_choice!"=="y" (
    echo !newname!_%version%.zip created in root directory.
)
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