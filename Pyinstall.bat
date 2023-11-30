@echo off
cd %~dp0
pyinstaller --onefile WinFunct.py
echo -------INFO------- Please manually close this window after update. Install-Script will always pause -------INFO-------
pause
