@echo off
cd %~dp0

echo Pulling latest updates from Git...
git pull

echo Installing required Python packages...
pip install -r requirements.txt

echo Running the WinFunct Python script...
python WinFunct.py

echo -------INFO------- Please manually close this window after update. Update-Script will always pause -------INFO-------
pause
