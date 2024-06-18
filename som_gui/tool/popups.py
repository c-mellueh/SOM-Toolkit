import os.path

import SOMcreator

import som_gui.core.tool
from som_gui.icons import get_icon
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QFileDialog
from som_gui import tool

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"


class Popups(som_gui.core.tool.Popups):
    @classmethod
    def get_path(cls, file_format: str, window) -> str:
        """ File Open Dialog with modifiable file_format"""
        path = tool.Settings.get_export_path()
        if path:
            basename = os.path.basename(path)
            split = os.path.splitext(basename)[0]
            filename_without_extension = os.path.splitext(split)[0]
            dirname = os.path.dirname(path)
            path = os.path.join(dirname, filename_without_extension)

        path = \
            QFileDialog.getSaveFileName(window, f"Save {file_format}", path,
                                        f"{file_format} Files (*.{file_format})")[0]
        if path:
            tool.Settings.set_export_path(path)
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
    def get_save_path(cls, base_path: str):
        window = tool.MainWindow.get()
        return QFileDialog.getSaveFileName(window, "Save Project", base_path, FILETYPE)[0]

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
    def error_convert_double():
        msg_box = QMessageBox()
        msg_box.setText("Wert kann nicht in Dezimalzahl umgewandelt werden!")
        msg_box.setWindowTitle(" ")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.exec()

    @classmethod
    def error_convert_integer():
        msg_box = QMessageBox()
        msg_box.setText("Wert kann nicht in Ganzzahl umgewandelt werden!")
        msg_box.setWindowTitle(" ")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.exec()

    @classmethod
    def req_export_pset_name(cls, parent_window):
        return QInputDialog.getText(parent_window, "PropertySet name", "What's the name of the Export PropertySet?")
