@echo off
cd %~dp0

echo Pulling latest updates from Git...
git pull
if %errorlevel% NEQ 0 (
    echo Error: Failed to pull updates from Git. Please check your network connection and repository status.
    pause
    exit /B 1
)

echo Installing required Python packages...
pip install -r requirements.txt
if %errorlevel% NEQ 0 (
    echo Error: Failed to install required Python packages. Please check your Python environment and requirements.txt file.
    pause
    exit /B 1
)

echo -------INFO------- UPDATE COMPLETE. Please manually close this window after update. -------INFO-------
pause
