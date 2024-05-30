spec_content = """
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(['WinFunct.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'networkx', 'tensorflow'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=False,  # Include binaries to ensure functionality
          name='WinFunct',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,  # Disable UPX for consistency with defaults
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,  # Disable UPX for consistency with defaults
               upx_exclude=[],
               name='WinFunct')
"""

with open("WinFunct.spec", "w") as spec_file:
    spec_file.write(spec_content)
