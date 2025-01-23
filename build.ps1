conda activate SOM-Toolkit
$env:PYTHONPATH = "C:\Users\ChristophMellueh\Non-Sync-Data\SOM-Toolkit"
Write-Output "UPDATE TOOLS"
python som_gui/_update_tools.py
Set-Location som_gui/resources/translation
Write-Output ""
Write-Output "Create PyProject"

python _create_pyproject.py
Write-Output ""
Write-Output "LUpdate"


pyside6-project lupdate .
Write-Output ""
Write-Output "BUILD"

pyside6-project build .