# -*- mode: python ; coding: utf-8 -*-
import importlib.util
import os

path = os.path.join(os.path.join(os.path.abspath(os.curdir), "som_gui"), "__init__.py")
spec = importlib.util.spec_from_file_location("som_gui", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

block_cipher = None
added_files = [('som_gui/icons', 'som_gui/icons'),
               ('som_gui/logs', 'som_gui/logs'),
               ]

a = Analysis(
    ['cli.py', ],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['jinja2', 'lxml', 'SOMcreator', 'ifcopenshell', 'tqdm', 'openpyxl', 'ifcopenshell.express.rules',
                   'ifcopenshell.express', 'ifcopenshell.express.express_parser', 'ifcopenshell.express.rules.IFC2X3'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name=f"SOM-Toolkit_v{module.__version__}",
)
