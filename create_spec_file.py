# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# Get the name from environment variable if set
app_name = os.getenv('APP_NAME', 'WinFunct')

# Increase recursion limit
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)


block_cipher = None

a = Analysis(
    ['WinFunct.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'tensorflow', 'PIL', 'numpy', 'pandas', 'scipy', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='WinFunct.ico'
)
"""

with open("WinFunct.spec", "w") as spec_file:
    spec_file.write(spec_content)

print(f"WinFunct.spec file has been created successfully with name: {app_name}")