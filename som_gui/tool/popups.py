import SOMcreator

import som_gui.core.tool
from som_gui.icons import get_icon
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QFileDialog
from som_gui import tool

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"


class Popups(som_gui.core.tool.Popups):
    @classmethod
    def create_warning_popup(cls, text):
        icon = get_icon()
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowIcon(icon)
        msg_box.exec()

    @classmethod
    def msg_unsaved(cls):
        icon = get_icon()
        msg_box = QMessageBox()
        msg_box.setText("Achtung Alle nicht gespeicherten Änderungen gehen verloren!")
        msg_box.setWindowTitle(" ")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg_box.setWindowIcon(icon)
        if msg_box.exec() == msg_box.StandardButton.Ok:
            return True
        else:
            return False

    @classmethod
    def get_project_name(cls):
        project_name = QInputDialog.getText(som_gui.MainUi.window, "New Project", "new Project Name:",
                                            QLineEdit.EchoMode.Normal,
                                            "")
        if project_name[1]:
            return project_name[0]
        else:
            return None

    @classmethod
    def get_save_path(cls, base_path: str):
        return QFileDialog.getSaveFileName(som_gui.MainUi.window, "Save Project", base_path, FILETYPE)[0]

    @classmethod
    def request_property_set_merge(cls, name: str):
        icon = get_icon()
        msg_box = QMessageBox()
        msg_box.setText(
            f"Es existiert ein PropertySet mit dem Namen '{name}' in den Vordefinierten PropertySets. Soll eine Verknüpfung hergestellt werden?")
        msg_box.setWindowTitle("Verdefiniertes PropertySet gefunden")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg_box.setWindowIcon(icon)
        answer = msg_box.exec()
        if answer == msg_box.StandardButton.Yes:
            return True
        elif answer == msg_box.StandardButton.No:
            return False
        else:
            return None
