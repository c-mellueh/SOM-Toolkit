import som_gui.core.tool
from som_gui.icons import get_icon
from PySide6.QtWidgets import QMessageBox


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
