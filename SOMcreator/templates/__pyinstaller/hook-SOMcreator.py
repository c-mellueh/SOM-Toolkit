from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('SOMcreator.templates', excludes=['__pyinstaller'])
datas += collect_data_files('SOMcreator.templates.js_templates')
