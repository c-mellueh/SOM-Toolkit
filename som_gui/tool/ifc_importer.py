from __future__ import annotations

import os
from typing import TYPE_CHECKING

import ifcopenshell

import som_gui
from som_gui import tool
import som_gui.core.tool
from som_gui.module.ifc_importer import ui
from PySide6.QtCore import QRunnable

if TYPE_CHECKING:
    from som_gui.module.ifc_importer.prop import IfcImportProperties
    from PySide6.QtWidgets import QLineEdit


class IfcImporter(som_gui.core.tool.IfcImporter):

    @classmethod
    def get_properties(cls) -> IfcImportProperties:
        return som_gui.IfcImportProperties

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
    def create_importer(cls):
        widget = ui.IfcImportWidget()
        cls._format_importer(widget)
        prop = cls.get_properties()
        prop.active_importer = widget
        return widget

    @classmethod
    def create_runner(cls, path):
        class Runner(QRunnable):
            def __init__(self, path):
                super().__init__()
                self.path = path
                self.ifc = None

            def run(self):
                self.ifc = ifcopenshell.open(self.path)

        return Runner(path)

    @classmethod
    def import_ifc_file(cls, path: os.PathLike | str):
        runner = cls.create_runner(path)
        runner.run()
        return runner.ifc
