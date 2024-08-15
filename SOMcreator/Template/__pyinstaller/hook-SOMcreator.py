from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('SOMcreator.Template', excludes=['__pyinstaller'])
datas += collect_data_files('SOMcreator.Template.js_templates')
