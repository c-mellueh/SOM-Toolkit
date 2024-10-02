from __future__ import annotations

import logging
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
        self.is_aborted = False

    def run(self):
        self.signaller.started.emit()
        time.sleep(1)
        self.ifc = ifcopenshell.open(self.path)
        logging.info("Importer finished")

        if not self.is_aborted:
            self.signaller.finished.emit()
        else:
            logging.info("Import is aborted so Importer will notify noone")

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
    def import_is_running(cls) -> bool:
        return cls.get_threadpool().activeThreadCount() > 0

    @classmethod
    def get_main_pset(cls, widget: ui.IfcImportWidget) -> str:
        return widget.widget.main_attribute_widget.ui.le_pset_name.text()

    @classmethod
    def get_main_attribute(cls, widget: ui.IfcImportWidget) -> str:
        return widget.widget.main_attribute_widget.ui.le_attribute_name.text()

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
    def get_threadpool(cls) -> QThreadPool:
        return cls.get_properties().thread_pool

    @classmethod
    def get_properties(cls) -> IfcImportProperties:
        return som_gui.IfcImportProperties

    @classmethod
    def set_progressbar_visible(cls, widget: ui.IfcImportWidget, visible: bool):
        widget.widget.progress_bar.setVisible(visible)
        widget.widget.label_status.setVisible(visible)

    @classmethod
    def get_ifc_paths(cls, widget: ui.IfcImportWidget) -> list[str]:
        return tool.Util.get_path_from_fileselector(widget.widget.file_selector_widget)

    @classmethod
    def create_importer(cls):
        widget = ui.IfcImportWidget()
        from som_gui.core.ifc_importer import IFC_PATH
        file_extension = "IFC Files (*.ifc *.IFC);;"
        tool.Util.fill_file_selector(widget.widget.file_selector_widget, "Ifc File", file_extension, IFC_PATH)
        prop = cls.get_properties()
        prop.active_importer = widget
        cls.set_progressbar_visible(widget, False)
        return widget

    @classmethod
    def create_runner(cls, status_label: QLabel, path: os.PathLike | str):
        if not os.path.exists(path):
            return
        return IfcImportRunner(path, status_label)



    @classmethod
    def create_export_line(cls, widget: ui.IfcImportWidget) -> tuple[QPushButton, QLineEdit]:
        widget = tool.Util.create_file_selector(name="", file_extension="*.xlsx", appdata_text="ModelcheckExport",
                                                request_save=True)
        return widget.ui.pushButton, widget.ui.lineEdit

    @classmethod
    def set_close_button_text(cls, widget: ui.IfcImportWidget, text: str):
        widget.widget.button_close.setText(widget.tr(text))

    @classmethod
    def set_run_button_enabled(cls, widget: ui.IfcImportWidget, enabled: bool):
        widget.widget.button_run.setEnabled(enabled)
