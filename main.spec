# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
added_files = [('C:/Users/ChristophMellueh/AppData/Local/miniconda3/envs/SOM-Toolkit/Lib/site-packages/SOMcreator','SOMcreator'),
               ('C:/Users/ChristophMellueh/AppData/Local/miniconda3/envs/SOM-Toolkit/Lib/site-packages/ifcopenshell/express','ifcopenshell/express'),
               ('som_gui/core','som_gui/core'),
               ('som_gui/tool','som_gui/tool'),
               ('som_gui/plugins','som_gui/plugins'),
                ('som_gui/module','som_gui/module'),
                ('som_gui/windows','som_gui/windows'),
                ('som_gui/widgets','som_gui/widgets'),
                ('som_gui/qt_designs','som_gui/qt_designs'),
                ('som_gui/data','som_gui/data'),
                ('som_gui/icons','som_gui/icons'),
                ('som_gui/settings/logging.conf','som_gui/settings/'),
               ]

hi = ['jinja2', 'lxml', 'SOMcreator', 'tqdm', 'openpyxl','som_gui','thefuzz.fuzz','SOMcreator.external_software','ifcopenshell','ifcopenshell.util','ifcopenshell.util.element','som_gui.settings']
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hi,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['som_gui.core','som_gui.tool','som_gui.plugins'],
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
    icon='som_gui/icons/icon.ico',
    manifest='app.manifest',
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
