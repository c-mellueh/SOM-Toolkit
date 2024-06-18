# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
added_files = [('som_gui','som_gui'),
               ('C:/Users/ChristophMellueh/AppData/Local/miniconda3/envs/SOM-Toolkit/Lib/site-packages/SOMcreator','SOMcreator'),
               ('C:/Users/ChristophMellueh/AppData/Local/miniconda3/envs/SOM-Toolkit/Lib/site-packages/ifcopenshell','ifcopenshell'),
               ]

hi = ['jinja2', 'lxml', 'SOMcreator', 'ifcopenshell', 'tqdm', 'openpyxl','som_gui','thefuzz.fuzz','SOMcreator.external_software','ifcopenshell',]
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hi,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['som_gui.core','som_gui.tool'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SOM-Toolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='som_gui/icons/icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=f"SOM-Toolkit",
)
