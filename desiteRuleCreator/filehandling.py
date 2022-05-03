from lxml import etree
from . import __version__ as project_version
from PySide6.QtWidgets import QFileDialog,QInputDialog,QLineEdit
from .io_messages import msg_unsaved

def save_as_clicked(window):
    if window.save_path is not None:
        path = \
            QFileDialog.getSaveFileName(window, "Save XML", window.save_path, "xml Files (*.xml *.DRCxml)")[0]
    else:
        path = QFileDialog.getSaveFileName(window, "Save XML", "", "xml Files (*.xml *.DRCxml)")[0]

    if path:
        window.save(path)
    return path

def save(self, path):
    project = etree.Element('Project')
    project.set("name", self.project_name)
    project.set("version", project_version)

    # TODO
    self.save_path = path
    print(f"Path: {path}")

def save_clicked(window):
    if window.save_path is None:
        path = window.save_as_clicked()
    else:
        save(window.save_path)
        path = window.save_path
    return path

def new_file(self):
    new_file = msg_unsaved(self.icon)
    if new_file:

        project_name = QInputDialog.getText(self, "New Project", "new Project Name:",QLineEdit.Normal, "")

        if project_name[1]:
            self.setWindowTitle(project_name[0])
            self.project_name = project_name[0]
            self.clear_all()

