from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable

import ifcopenshell

import som_gui
from som_gui import tool
import som_gui.core.tool
from som_gui.module.ifc_importer import ui
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QFileDialog

if TYPE_CHECKING:
    from som_gui.module.ifc_importer.prop import IfcImportProperties
    from PySide6.QtWidgets import QLineEdit, QLabel


class IfcImporter(som_gui.core.tool.IfcImporter):
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
    def _format_importer(cls, importer: ui.IfcImportWidget):
        importer.widget.label_ifc_missing.hide()
        importer.widget.label_export_missing.hide()
        importer.widget.label_export_missing.setStyleSheet("QLabel { color : red; }")
        importer.widget.label_ifc_missing.setStyleSheet("QLabel { color : red; }")
        importer.widget.line_edit_ifc.textEdited.connect(importer.widget.label_ifc_missing.hide)
        importer.widget.line_edit_export.textEdited.connect(importer.widget.label_export_missing.hide)
        importer.widget.progress_bar.hide()
        importer.widget.label_status.hide()
        cls.autofill_ifcpath(importer.widget.line_edit_ifc)

    @classmethod
    def autofill_ifcpath(cls, line_edit: QLineEdit):
        ifc_path = tool.Settings.get_ifc_path()
        if ifc_path:
            if isinstance(ifc_path, list):
                ifc_path = tool.Settings.PATH_SEPERATOR.join(ifc_path)
            line_edit.setText(ifc_path)

    @classmethod
    def open_file_dialog(cls, window, base_path: os.PathLike):
        file_text = "IFC Files (*.ifc *.IFC);;"
        path = QFileDialog.getOpenFileNames(window, "IFC-Files", base_path, file_text)[0]
        return path

    @classmethod
    def get_ifc_paths(cls, widget: ui.IfcImportWidget) -> list[str]:
        path = widget.widget.line_edit_ifc.text()
        seperator = tool.Settings.get_seperator()
        if seperator in path:
            paths = path.split(seperator)
        else:
            paths = [path]
        return paths

    @classmethod
    def create_importer(cls):
        widget = ui.IfcImportWidget()
        cls._format_importer(widget)
        prop = cls.get_properties()
        prop.active_importer = widget
        som_gui.module.ifc_importer.trigger.connect_new_importer(widget)
        pset, attribute = tool.Project.get().get_main_attribute()
        cls.fill_main_attribute(widget, pset, attribute)
        return widget

    @classmethod
    def create_runner(cls, status_label: QLabel, path: os.PathLike | str):
        if not os.path.exists(path):
            return
        runner = ui.IfcImportRunner(path, status_label)
        return runner

    @classmethod
    def fill_main_attribute(cls, widget: ui.IfcImportWidget, pset: str, attribute: str):
        if not pset or not attribute:
            return

        widget.widget.line_edit_ident_pset.setText(pset)
        widget.widget.line_edit_ident_attribute.setText(attribute)
