import os.path

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QLineEdit,
    QListWidgetItem,
    QMessageBox,
)

import som_gui.core.tool
from som_gui import tool
from som_gui.module.popups import ui
from som_gui.resources.icons import get_icon

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"


class Popups(som_gui.core.tool.Popups):

    @classmethod
    def get_open_path(cls, file_format: str, window, path=None, title=None) -> str:
        return cls._get_path(file_format, window, path, False, title)

    @classmethod
    def get_save_path(cls, file_format: str, window, path=None, title=None) -> str:
        return cls._get_path(file_format, window, path, True, title)

    @classmethod
    def _get_path(
        cls, file_format: str, window, path=None, save: bool = False, title=None
    ) -> str:
        """File Open Dialog with modifiable file_format"""
        if path:
            basename = os.path.basename(path)
            split = os.path.splitext(basename)[0]
            filename_without_extension = os.path.splitext(split)[0]
            dirname = os.path.dirname(path)
            path = os.path.join(dirname, filename_without_extension)
        if title is None:
            title = f"Save {file_format}" if save else f"Open {file_format}"

        if save:
            path = QFileDialog.getSaveFileName(
                window, title, path, f"{file_format} Files (*.{file_format})"
            )[0]
        else:
            path = QFileDialog.getOpenFileName(
                window, title, path, f"{file_format} Files (*.{file_format})"
            )[0]
        return path

    @classmethod
    def get_folder(cls, window, path: str) -> str:
        """Folder Open Dialog"""
        if path:
            path = os.path.basename(path)
        path = QFileDialog.getExistingDirectory(parent=window, dir=path)
        return path

    @classmethod
    def _request_text_input(cls, title: str, request_text, prefill, parent=None):
        if parent is None:
            parent = tool.MainWindow.get()
        answer = QInputDialog.getText(
            parent, title, request_text, QLineEdit.EchoMode.Normal, prefill
        )
        if answer[1]:
            return answer[0]
        else:
            return None

    @classmethod
    def request_property_name(cls, old_name, parent):
        title = QCoreApplication.translate("Popups", "Rename Property")
        text = QCoreApplication.translate("Popups", "New name:")

        return cls._request_text_input(title, text, old_name, parent)

    @classmethod
    def request_save_before_exit(cls):
        icon = get_icon()
        title = QCoreApplication.translate("Popups", "Save before exit")
        text = QCoreApplication.translate(
            "Popups", "Do you want to save the project before leaving?"
        )
        msg_box = QMessageBox(
            QMessageBox.Icon.Question,
            title,
            text,
            QMessageBox.StandardButton.Cancel
            | QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.No,
        )

        msg_box.setWindowIcon(icon)
        reply = msg_box.exec()
        if reply == msg_box.StandardButton.Save:
            return True
        elif reply == msg_box.StandardButton.No:
            return False
        return None

    @classmethod
    def create_warning_popup(
        cls, text, window_title: str = None, text_title: str = None
    ):
        if window_title is None:
            window_title = QCoreApplication.translate("Popups", "Warning")
        if text_title is None:
            text_title = QCoreApplication.translate("Popups", "Warning")
        icon = get_icon()
        msg_box = QMessageBox()
        msg_box.setText(text_title)
        msg_box.setWindowTitle(window_title)
        msg_box.setDetailedText(text)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowIcon(icon)
        msg_box.exec()

    @classmethod
    def create_info_popup(cls, text, title: str = None):
        if title is None:
            title = QCoreApplication.translate("Popups", "Info")
        icon = get_icon()
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowIcon(icon)
        msg_box.exec()

    @classmethod
    def file_in_use_warning(cls, title, text, detail=""):
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowIcon(get_icon())
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        msg_box.setDetailedText(detail)
        result = msg_box.exec()
        return result == QMessageBox.StandardButton.Ok

    @classmethod
    def create_file_dne_warning(cls, path):
        base_name = os.path.basename(path)
        text = QCoreApplication.translate("Popups", "File '{}' doesn't exist").format(
            base_name
        )
        cls.create_warning_popup(text)

    @classmethod
    def create_folder_dne_warning(cls, path):
        base_name = os.path.basename(path)
        text = QCoreApplication.translate("Popups", "Folder '{}' doesn't exist").format(
            base_name
        )
        cls.create_warning_popup(text)

    @classmethod
    def msg_unsaved(cls):
        icon = get_icon()
        msg_box = QMessageBox()
        text = QCoreApplication.translate(
            "Popups", "Warning! All unsaved changes will be lost!"
        )
        msg_box.setText(text)
        msg_box.setWindowTitle(" ")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg_box.setWindowIcon(icon)
        if msg_box.exec() == msg_box.StandardButton.Ok:
            return True
        else:
            return False

    @classmethod
    def get_project_name(cls):
        title = QCoreApplication.translate("Popups", "New Project")
        text = QCoreApplication.translate("Popups", "Project Name")

        return cls._request_text_input(title, text, "")

    @classmethod
    def request_property_set_merge(cls, name: str, mode):
        icon = get_icon()
        msg_box = QMessageBox()

        title = QCoreApplication.translate("Popups", "PropertySet found")
        if mode == 1:
            text = QCoreApplication.translate(
                "Popups",
                "A PropertySet with the name '{}' allready exists as Predefined PSet. Do you want to create a link?",
            )
            # text = f"Es existiert ein PropertySet mit dem Namen '{name}' in den Vordefinierten PropertySets. Soll eine Verknüpfung hergestellt werden?"
        elif mode == 2:
            text = QCoreApplication.translate(
                "Popups",
                "A PropertySet with the name '{}' allready exists in a parent class. Do you want to create a link?",
            )
            # text = f"Es existiert ein PropertySet mit dem Namen '{name}' in einem übergeordneten Objekt. Soll eine Verknüpfung hergestellt werden?"
        else:
            text = "{}"
        msg_box.setText(text.format(name))
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.Cancel
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg_box.setWindowIcon(icon)
        answer = msg_box.exec()
        if answer == msg_box.StandardButton.Yes:
            return True
        elif answer == msg_box.StandardButton.No:
            return False
        else:
            return None

    @classmethod
    def req_export_pset_name(cls, parent_window):
        label = QCoreApplication.translate(
            "Export", "What's the name of the Export PropertySet?"
        )
        title = QCoreApplication.translate("Export", "PropertySet name")
        return QInputDialog.getText(parent_window, title, label)

    @classmethod
    def req_delete_items(cls, string_list, item_type=1) -> (bool, bool):
        """
        item_type 1= Class,2= Node, 3 = PropertySet, 4 = Property
        """
        dialog = ui.DeleteRequestDialog()
        widget = dialog.widget
        if len(string_list) <= 1:
            if item_type == 1:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete Class?")
                )
            if item_type == 2:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete Node?")
                )
            if item_type == 3:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete PropertySet?")
                )
            if item_type == 4:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete Property?")
                )
        else:
            if item_type == 1:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete Classes?")
                )
            if item_type == 2:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete Nodes?")
                )
            if item_type == 3:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete PropertySets?")
                )
            if item_type == 4:
                widget.label.setText(
                    QCoreApplication.translate("Popups", "Delete Properties?")
                )

        for text in string_list:
            widget.listWidget.addItem(QListWidgetItem(text))
        result = dialog.exec()
        check_box_state = (
            True
            if widget.check_box_recursion.checkState() == Qt.CheckState.Checked
            else False
        )
        return bool(result), check_box_state
