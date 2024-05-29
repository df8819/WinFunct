@echo off
:: BatchGotAdmin
:-------------------------------------
REM --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\icacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Creating VBS script to request admin rights... >> admin_log.txt
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    echo VBS script created. Executing... >> admin_log.txt
    "%temp%\getadmin.vbs"
    echo Deleting VBS script... >> admin_log.txt
    del "%temp%\getadmin.vbs"
    echo VBS script deleted. Exiting batch file. >> admin_log.txt
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

:: Running the Python script with admin privileges
python WinFunct.py
if %errorlevel% NEQ 0 (
    echo Error: Failed to run the Python script. >> admin_log.txt
    exit /B %errorlevel%
)
