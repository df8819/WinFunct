@echo off
setlocal enabledelayedexpansion

echo Formatting image links for README.md...

for %%j in (*.png) do (
    echo ![Image](GUI_Pics/%%j^)
)

echo.
echo Copy the above lines and paste them into your README.md file.
echo Remember to adjust the path if necessary, depending on where your README.md is located.

pause
