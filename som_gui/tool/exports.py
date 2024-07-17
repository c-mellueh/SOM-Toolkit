import som_gui.core.tool
import SOMcreator
from SOMcreator.external_software.desite import bookmarks
from SOMcreator.external_software import vestra
from SOMcreator.external_software import card1
from SOMcreator.external_software import allplan
from SOMcreator.filehandling import create_mapping_script
from SOMcreator import excel as som_excel
from SOMcreator.tool import ExportExcel
from som_gui import settings
from som_gui.module.main_window.ui import MainWindow
from PySide6.QtWidgets import QFileDialog
import os


class Exports(som_gui.core.tool.Exports):
    @classmethod
    def get_path(cls, main_window: MainWindow, file_format: str) -> str:
        """ File Open Dialog with modifiable file_format"""
        path = settings.get_export_path()
        if path:
            basename = os.path.basename(path)
            split = os.path.splitext(basename)[0]
            filename_without_extension = os.path.splitext(split)[0]
            dirname = os.path.dirname(path)
            path = os.path.join(dirname, filename_without_extension)

        path = \
            QFileDialog.getSaveFileName(main_window, f"Save {file_format}", path,
                                        f"{file_format} Files (*.{file_format})")[0]
        if path:
            settings.set_export_path(path)
        return path

    @classmethod
    def get_folder(cls, main_window: MainWindow) -> str:
        """Folder Open Dialog"""
        path = settings.get_export_path()
        if path:
            path = os.path.basename(path)
        path = \
            QFileDialog.getExistingDirectory(parent=main_window, dir=path)
        return path

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
                settings.set_export_path(export_folder)

    @classmethod
    def export_card_1(cl, project: SOMcreator.Project, parent_window, path):
        file_text = "Excel Files (*.xlsx);;"
        src, answer = QFileDialog.getOpenFileName(parent_window, "Template Excel", path, file_text)
        if not answer:
            return
        path = QFileDialog.getSaveFileName(parent_window, "CARD1 Excel", path, file_text)[0]

        if path:
            card1.create_mapping(src, path, project)
            settings.set_export_path(path)

    @classmethod
    def export_excel(cls, project: SOMcreator.Project, path: str):
        som_excel.export(project, path, ExportExcel)

    @classmethod
    def create_mapping_script(cls, project: SOMcreator.Project, name: str, path: str):
        create_mapping_script(project, name, path)

    @classmethod
    def export_allplan(cls, project, path, name):
        allplan.create_mapping(project, path, name)
