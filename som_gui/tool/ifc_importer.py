from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING, Callable

import ifcopenshell

import som_gui
from som_gui import tool
import som_gui.core.tool
from som_gui.module.ifc_importer import ui
from PySide6.QtCore import QThreadPool, QObject, Signal, QRunnable, QSize
from PySide6.QtWidgets import QFileDialog, QPushButton, QSizePolicy, QLineEdit, QLabel
from som_gui.module.util.constants import PATH_SEPERATOR
if TYPE_CHECKING:
    from som_gui.module.ifc_importer.prop import IfcImportProperties
    from PySide6.QtWidgets import QLineEdit, QLabel


class Signaller(QObject):
    started = Signal()
    finished = Signal()


class IfcImportRunner(QRunnable):
    def __init__(self, path: os.PathLike | str, status_label: QLabel):
        super(IfcImportRunner, self).__init__()
        self.path = path
        self.ifc: ifcopenshell.file | None = None
        self.signaller = Signaller()
        self.status_label = status_label

    def run(self):
        self.signaller.started.emit()
        time.sleep(1)
        self.ifc = ifcopenshell.open(self.path)
        self.signaller.finished.emit()

class IfcImporter(som_gui.core.tool.IfcImporter):
    @classmethod
    def check_inputs(cls, ifc_paths, main_pset, main_attribute):
        for path in ifc_paths:
            if not os.path.isfile(path):
                tool.Popups.create_file_dne_warning(path)
                return False

        if not main_pset:
            tool.Popups.create_warning_popup(f"PropertySet Name ist nicht ausgefüllt")
            return False

        if not main_attribute:
            tool.Popups.create_warning_popup(f"Attribut Name ist nicht ausgefüllt")
            return False
        return True

    @classmethod
    def get_main_pset(cls, widget: ui.IfcImportWidget) -> str:
        return widget.widget.line_edit_ident_pset.text()

    @classmethod
    def get_main_attribute(cls, widget: ui.IfcImportWidget) -> str:
        return widget.widget.line_edit_ident_attribute.text()

    @classmethod
    def set_status(cls, widget: ui.IfcImportWidget, status: str):
        widget.widget.label_status.setText(status)

    @classmethod
    def set_progress(cls, widget: ui.IfcImportWidget, value: int):
        widget.widget.progress_bar.setValue(value)

    @classmethod
    def create_thread_pool(cls) -> QThreadPool:
        cls.get_properties().thread_pool = QThreadPool()
        return cls.get_properties().thread_pool

    @classmethod
    def get_properties(cls) -> IfcImportProperties:
        return som_gui.IfcImportProperties

    @classmethod
    def set_progressbar_visible(cls, widget: ui.IfcImportWidget, visible: bool):
        widget.widget.progress_bar.setVisible(visible)
        widget.widget.label_status.setVisible(visible)

    @classmethod
    def autofill_ifcpath(cls, line_edit: QLineEdit):
        from som_gui.core.ifc_importer import IFC_PATH
        ifc_path = tool.Appdata.get_path(IFC_PATH)
        if ifc_path:
            if isinstance(ifc_path, list):
                ifc_path = PATH_SEPERATOR.join(ifc_path)
            line_edit.setText(ifc_path)

    @classmethod
    def open_file_dialog(cls, window, base_path: os.PathLike):
        file_text = "IFC Files (*.ifc *.IFC);;"
        path = QFileDialog.getOpenFileNames(window, "IFC-Files", base_path, file_text)[0]
        return path

    @classmethod
    def get_ifc_paths(cls, widget: ui.IfcImportWidget) -> list[str]:
        path = widget.widget.line_edit_ifc.text()
        if PATH_SEPERATOR in path:
            paths = path.split(PATH_SEPERATOR)
        else:
            paths = [path]
        return paths

    @classmethod
    def create_importer(cls):
        widget = ui.IfcImportWidget()
        cls.autofill_ifcpath(widget.widget.line_edit_ifc)
        prop = cls.get_properties()
        prop.active_importer = widget
        som_gui.module.ifc_importer.trigger.connect_new_importer(widget)
        pset, attribute = tool.Project.get().get_main_attribute()
        cls.fill_main_attribute(widget, pset, attribute)
        cls.set_progressbar_visible(widget, False)
        return widget

    @classmethod
    def create_runner(cls, status_label: QLabel, path: os.PathLike | str):

        if not os.path.exists(path):
            return
        return IfcImportRunner(path, status_label)

    @classmethod
    def fill_main_attribute(cls, widget: ui.IfcImportWidget, pset: str, attribute: str):
        if not pset or not attribute:
            return

        widget.widget.line_edit_ident_pset.setText(pset)
        widget.widget.line_edit_ident_attribute.setText(attribute)

    @classmethod
    def create_export_line(cls, widget: ui.IfcImportWidget) -> tuple[QPushButton, QLineEdit]:
        export_line_edit = QLineEdit()
        export_line_edit.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))
        widget.widget.gridLayout.addWidget(QLabel("Export Pfad"), 5, 0, 1, 2)
        widget.widget.gridLayout.addWidget(export_line_edit, 6, 0, 1, 2)
        export_button = QPushButton()
        export_button.setMaximumSize(QSize(25, 16777215))
        widget.widget.gridLayout.addWidget(export_button, 6, 2, 1, 1)
        export_button.show()
        export_button.setText("...")
        return export_button, export_line_edit

    @classmethod
    def set_close_button_text(cls, widget: ui.IfcImportWidget, text: str):
        widget.widget.button_close.setText(widget.tr(text))

    @classmethod
    def set_run_button_enabled(cls, widget: ui.IfcImportWidget, enabled: bool):
        widget.widget.button_run.setEnabled(enabled)
