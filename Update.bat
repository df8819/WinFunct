@echo off
cd %~dp0

echo Pulling latest updates from Git...
git pull

echo Installing required Python packages...
pip install -r requirements.txt

echo -------INFO------- UPDATE COMPLETE. Please manually close this window after update. -------INFO-------
pause
