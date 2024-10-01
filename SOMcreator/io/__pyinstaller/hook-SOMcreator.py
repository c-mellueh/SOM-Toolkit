from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('SOMcreator.io', excludes=['__pyinstaller'])
datas += collect_data_files('SOMcreator.io.desite')
datas += collect_data_files('SOMcreator.io.bim_collab_zoom')
datas += collect_data_files('SOMcreator.io.ids')
datas += collect_data_files('SOMcreator.io.bsdd')
