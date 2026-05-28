#!/bin/bash
set -e
cd "$(dirname "$0")"

# Root check
if [ "$EUID" -ne 0 ]; then
    echo "Re-running as root..."
    exec sudo bash "$0" "$@"
fi

# Validate
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found."
    exit 1
fi

# Version
while true; do
    read -rp "Version number (e.g. v2.000): " version
    [ -n "$version" ] && break
done

# Name
appname="WinFunct"
read -rp "Rename from 'WinFunct'? (y/n): " rename
if [[ "$rename" =~ ^[Yy]$ ]]; then
    read -rp "New name: " appname
fi

# Zip option
read -rp "Create zip archive? (y/n): " zip

# Build
echo ""
echo "Compiling..."
if [ -f ".venv/bin/pyinstaller" ]; then
    PYINSTALLER=".venv/bin/pyinstaller"
elif command -v pyinstaller &>/dev/null; then
    PYINSTALLER="pyinstaller"
else
    echo "pyinstaller not found. Installing into .venv..."
    python3 -m venv .venv
    .venv/bin/pip install pyinstaller -q
    PYINSTALLER=".venv/bin/pyinstaller"
fi

$PYINSTALLER --clean --noconfirm --onefile \
    --icon=WinFunct.ico \
    --add-data "WinFunct.ico:." \
    --add-data "UI_themes.json:." \
    --add-data "gui:gui" \
    --add-data "core:core" \
    --add-data "config.py:." \
    --name "$appname" \
    main.py

# Move & rename (with .exe extension)
mv -f "dist/${appname}" "./${appname}_${version}.exe"

# Zip
if [[ "$zip" =~ ^[Yy]$ ]]; then
    zip "./${appname}_${version}.zip" "./${appname}_${version}.exe"
fi

# Cleanup
rm -rf dist build
rm -f *.spec

echo ""
echo "Done: ${appname}_${version}.exe"
