import som_gui.core.tool
from som_gui.icons import get_icon
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit
from som_gui import tool

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
        msg_box.setText("Warning, unsaved changes will be lost!")
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
