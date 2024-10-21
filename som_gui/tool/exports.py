from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import SOMcreator
from SOMcreator.exporter.desite import bookmarks
from SOMcreator.exporter import allplan, card1, vestra
import SOMcreator.exporter.som_json
from SOMcreator.exporter.excel import core as excel_core
from SOMcreator.exporter.excel.tool import ExportExcel
from PySide6.QtWidgets import QFileDialog, QLineEdit, QWidget, QGridLayout, QLabel
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication
if TYPE_CHECKING:
    from som_gui.module.exports.prop import ExportProperties

class Exports(som_gui.core.tool.Exports):
    @classmethod
    def get_properties(cls) -> ExportProperties:
        return som_gui.ExportProperties

    @classmethod
    def set_action(cls, name, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name) -> QAction:
        return cls.get_properties().actions[name]

    @classmethod
    def export_bookmarks(cls, project: SOMcreator.Project, path: str):
        bookmarks.export_bookmarks(project, path)

    @classmethod
    def export_vestra(cls, project: SOMcreator.Project, parent_window, path):
        file_text = "Excel Files (*.xlsx);;"
        caption = QCoreApplication.translate("Export", "Template Excel")
        excel_path, answer = QFileDialog.getOpenFileName(parent_window, caption, path, file_text)
        if answer:
            caption = QCoreApplication.translate("Export", "Export Folder")
            export_folder = QFileDialog.getExistingDirectory(parent_window, caption, path)
            if export_folder:
                vestra.create_mapping(excel_path, export_folder, project)
                return export_folder

    @classmethod
    def export_card_1(cls, project: SOMcreator.Project, parent_window, path):
        file_text = "Excel Files (*.xlsx);;"
        caption = QCoreApplication.translate("Export", "Template Excel")
        src, answer = QFileDialog.getOpenFileName(parent_window, caption, path, file_text)
        if not answer:
            return
        caption = QCoreApplication.translate("Export", "CARD1 Excel")
        path = QFileDialog.getSaveFileName(parent_window, caption, path, file_text)[0]

        if path:
            card1.create_mapping(src, path, project)
            return path

    @classmethod
    def export_excel(cls, project: SOMcreator.Project, path: str):
        excel_core.export(project, path, ExportExcel)

    @classmethod
    def create_mapping_script(cls, project: SOMcreator.Project, name: str, path: str):
        SOMcreator.exporter.som_json.create_mapping_script(project, name, path)

    @classmethod
    def export_allplan(cls, project, path, name):
        allplan.create_mapping(project, path, name)

    @classmethod
    def create_settings_widget(cls, names):
        widget = QWidget()
        cls.get_properties().settings_widget = widget
        widget.setLayout(QGridLayout())
        layout: QGridLayout = widget.layout()
        for row, name in enumerate(names):
            layout.addWidget(QLabel(name), row, 0)
            layout.addWidget(QLineEdit(), row, 1)
        layout.setRowStretch(len(names), 1)
        return widget

    @classmethod
    def get_settings_widget(cls) -> QWidget:
        return cls.get_properties().settings_widget
