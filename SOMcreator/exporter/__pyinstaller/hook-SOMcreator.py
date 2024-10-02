from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('SOMcreator.io', excludes=['__pyinstaller'])
datas += collect_data_files('SOMcreator.exporter.desite')
datas += collect_data_files('SOMcreator.exporter.bim_collab_zoom')
datas += collect_data_files('SOMcreator.exporter.ids')
datas += collect_data_files('SOMcreator.exporter.bsdd')
