from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('SOMcreator.external_software', excludes=['__pyinstaller'])
datas += collect_data_files('SOMcreator.external_software.bim_collab_zoom')
datas += collect_data_files('SOMcreator.external_software.desite')
datas += collect_data_files('SOMcreator.external_software.ids')
datas += collect_data_files('SOMcreator.external_software.bsdd')
