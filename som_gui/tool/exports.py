from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import SOMcreator
from SOMcreator.external_software.desite import bookmarks
from SOMcreator.io import allplan, card1, vestra
import SOMcreator.io.som_json
from SOMcreator import excel as som_excel
from SOMcreator.tool import ExportExcel
from PySide6.QtWidgets import QFileDialog, QLineEdit, QWidget, QGridLayout, QLabel
import som_gui

if TYPE_CHECKING:
    from som_gui.module.exports.prop import ExportProperties

class Exports(som_gui.core.tool.Exports):
    @classmethod
    def get_properties(cls) -> ExportProperties:
        return som_gui.ExportProperties

    @classmethod
    def export_bookmarks(cls, project: SOMcreator.Project, path: str):
        bookmarks.export_bookmarks(project, path)

    @classmethod
    def export_vestra(cls, project: SOMcreator.Project, parent_window, path):
        file_text = "Excel Files (*.xlsx);;"
        excel_path, answer = QFileDialog.getOpenFileName(parent_window, "Template Excel", path, file_text)
        if answer:
            export_folder = QFileDialog.getExistingDirectory(parent_window, "Export Folder", path)
            if export_folder:
                vestra.create_mapping(excel_path, export_folder, project)
                return export_folder

    @classmethod
    def export_card_1(cl, project: SOMcreator.Project, parent_window, path):
        file_text = "Excel Files (*.xlsx);;"
        src, answer = QFileDialog.getOpenFileName(parent_window, "Template Excel", path, file_text)
        if not answer:
            return
        path = QFileDialog.getSaveFileName(parent_window, "CARD1 Excel", path, file_text)[0]

        if path:
            card1.create_mapping(src, path, project)
            return path

    @classmethod
    def export_excel(cls, project: SOMcreator.Project, path: str):
        som_excel.export(project, path, ExportExcel)

    @classmethod
    def create_mapping_script(cls, project: SOMcreator.Project, name: str, path: str):
        SOMcreator.io.som_json.create_mapping_script(project, name, path)

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
