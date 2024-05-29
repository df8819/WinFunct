@echo off
:: BatchGotAdmin
echo Executing run.bat...
echo.
:-------------------------------------
REM --> Check for permissions
echo Checking for admin permissions...
>nul 2>&1 "%SYSTEMROOT%\system32\icacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Creating VBS script to get admin rights...
    echo.
    goto UACPrompt
) else (
    echo.
    echo Admin permissions are in close reach...
    echo.
    goto gotAdmin
)

:UACPrompt
    echo Executing VBS script...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    echo VBS script created. Executing...
    echo.
    "%temp%\getadmin.vbs"
    echo Deleting VBS script right away...
    echo.
    del "%temp%\getadmin.vbs"
    echo VBS script deleted. Exiting batch run.bat...
    echo.
    exit /B

:gotAdmin
    echo Admin permissions acquired. Executing .py file...
    echo.
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

:: Running the Python script with admin privileges
echo Running the Python app...
echo.
python WinFunct.py
if %errorlevel% NEQ 0 (
    echo Error: Failed to run the Python app.
    echo.
    exit /B %errorlevel%
)
echo Python app executed successfully...
echo.

:: Close the terminal window after the script finishes
exit
