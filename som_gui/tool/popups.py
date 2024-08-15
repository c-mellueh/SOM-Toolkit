import os.path

import SOMcreator

import som_gui.core.tool
from som_gui.icons import get_icon
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QFileDialog, QListWidgetItem
from PySide6.QtCore import Qt
from som_gui import tool
from som_gui.module.popups import ui

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"


class Popups(som_gui.core.tool.Popups):

    @classmethod
    def get_open_path(cls, file_format: str, window, path=None, title=None) -> str:
        return cls._get_path(file_format, window, path, False, title)

    @classmethod
    def get_save_path(cls, file_format: str, window, path=None, title=None) -> str:
        window = tool.MainWindow.get()
        return cls._get_path(file_format, window, path, True, title)

    @classmethod
    def _get_path(cls, file_format: str, window, path=None, save: bool = False, title=None) -> str:
        """ File Open Dialog with modifiable file_format"""
        if path:
            basename = os.path.basename(path)
            split = os.path.splitext(basename)[0]
            filename_without_extension = os.path.splitext(split)[0]
            dirname = os.path.dirname(path)
            path = os.path.join(dirname, filename_without_extension)
        if title is None:
            title = f"Save {file_format}" if save else f"Open {file_format}"

        if save:
            path = QFileDialog.getSaveFileName(window, title, path, f"{file_format} Files (*.{file_format})")[0]
        else:
            path = QFileDialog.getOpenFileName(window, title, path, f"{file_format} Files (*.{file_format})")[0]
        if path:
            tool.Settings.set_export_path(path)
        return path

    @classmethod
    def get_folder(cls, window, path: str) -> str:
        """Folder Open Dialog"""
        if path:
            path = os.path.basename(path)
        path = \
            QFileDialog.getExistingDirectory(parent=window, dir=path)
        return path

    @classmethod
    def _request_text_input(cls, title: str, request_text, prefill, parent=None):
        if parent is None:
            parent = tool.MainWindow.get()
        answer = QInputDialog.getText(parent, title, request_text,
                                      QLineEdit.EchoMode.Normal,
                                      prefill)
        if answer[1]:
            return answer[0]
        else:
            return None

    @classmethod
    def request_attribute_name(cls, old_name, parent):
        return cls._request_text_input("Attribut umbenennen", "Neuer Name für Attribut:", old_name, parent)

    @classmethod
    def request_save_before_exit(cls):
        icon = get_icon()
        text = "Möchten Sie ihr Projekt vor dem Verlassen speichern?"
        msg_box = QMessageBox(QMessageBox.Icon.Question,
                              "Vor verlassen speichern?",
                              text,
                              QMessageBox.StandardButton.Cancel |
                              QMessageBox.StandardButton.Save |
                              QMessageBox.StandardButton.No)

        msg_box.setWindowIcon(icon)
        reply = msg_box.exec()
        if reply == msg_box.StandardButton.Save:
            return True
        elif reply == msg_box.StandardButton.No:
            return False
        return None

    @classmethod
    def create_warning_popup(cls, text, title="Warning"):
        icon = get_icon()
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowIcon(icon)
        msg_box.exec()

    @classmethod
    def create_info_popup(cls, text, title="Info"):
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
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.setDetailedText(detail)
        result = msg_box.exec()
        return result == QMessageBox.StandardButton.Ok

    @classmethod
    def create_file_dne_warning(cls, path):
        base_name = os.path.basename(path)
        text = f"Datei '{base_name}' existiert nicht an angegebenem Ort"
        cls.create_warning_popup(text)

    @classmethod
    def create_folder_dne_warning(cls, path):
        base_name = os.path.basename(path)
        text = f"Ordner '{base_name}' existiert nicht an angegebenem Ort"
        cls.create_warning_popup(text)

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
        return cls._request_text_input("Neues Projekt", "Projekt Name", "")

    @classmethod
    def get_new_use_case_name(cls, old_name: str = "", parent=None):
        return cls._request_text_input("Anwendungsfall umbenennen", "Neuer Name", old_name, parent)

    @classmethod
    def get_phase_name(cls, old_name: str = "", parent=None):
        return cls._request_text_input("Leistungsphase umbenennen", "Neuer Name", old_name, parent)



    @classmethod
    def request_property_set_merge(cls, name: str, mode):
        icon = get_icon()
        msg_box = QMessageBox()
        if mode == 1:
            text = f"Es existiert ein PropertySet mit dem Namen '{name}' in den Vordefinierten PropertySets. Soll eine Verknüpfung hergestellt werden?"
        if mode == 2:
            text = f"Es existiert ein PropertySet mit dem Namen '{name}' in einem übergeordneten Objekt. Soll eine Verknüpfung hergestellt werden?"
        msg_box.setText(text)
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

    @classmethod
    def req_export_pset_name(cls, parent_window):
        return QInputDialog.getText(parent_window, "PropertySet name", "What's the name of the Export PropertySet?")

    @classmethod
    def req_delete_items(cls, string_list, item_type=1) -> (bool, bool):
        """
            item_type 1= Object,2= Node, 3 = PropertySet, 4 = Attribute
            """
        dialog = ui.DeleteRequestDialog()
        widget = dialog.widget
        if len(string_list) <= 1:
            if item_type == 1:
                widget.label.setText("Dieses Objekt löschen?")
            if item_type == 2:
                widget.label.setText("Diese Node löschen?")
            if item_type == 3:
                widget.label.setText("Dieses PropertySet löschen?")
            if item_type == 4:
                widget.label.setText("Dieses Attribut löschen?")
        else:
            if item_type == 1:
                widget.label.setText("Diese Objekte löschen?")
            if item_type == 2:
                widget.label.setText("Diese Nodes löschen?")
            if item_type == 3:
                widget.label.setText("Diese PropertySets löschen?")
            if item_type == 4:
                widget.label.setText("Diese Attribute löschen?")

        for text in string_list:
            widget.listWidget.addItem(QListWidgetItem(text))
        result = dialog.exec()
        check_box_state = True if widget.check_box_recursion.checkState() == Qt.CheckState.Checked else False
        return bool(result), check_box_state
