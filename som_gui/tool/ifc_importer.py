from __future__ import annotations

import logging
import os
import time
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import QCoreApplication, QObject, QRunnable, QThreadPool, Signal

import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.ifc_importer import ui

if TYPE_CHECKING:
    from som_gui.module.ifc_importer.prop import IfcImportProperties
    from PySide6.QtWidgets import QLabel
    from som_gui.module.util.ui import Progressbar

class Signaller(QObject):
    started = Signal()
    finished = Signal()


class IfcImportRunner(QRunnable):
    def __init__(self, path: os.PathLike | str,progress_bar = None):
        super(IfcImportRunner, self).__init__()
        self.path = path
        self.ifc: ifcopenshell.file | None = None
        self.signaller = Signaller()
        self.is_aborted = False
        self.progress_bar:Progressbar|None = progress_bar

    @property
    def status_label(self):
        return self.progress_bar.ui.label

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
            text = QCoreApplication.translate("IfcImporter", "PropertySet Name is empty")
            tool.Popups.create_warning_popup(text)
            return False

        if not main_attribute:
            text = QCoreApplication.translate("IfcImporter", "Attribute Name is empty")

            tool.Popups.create_warning_popup(text)
            return False
        return True

    @classmethod
    def import_is_running(cls) -> bool:
        return cls.get_threadpool().activeThreadCount() > 0

    @classmethod
    def get_main_pset(cls, widget: ui.IfcImportWidget) -> str:
        return widget.ui.main_attribute_widget.ui.le_pset_name.text()

    @classmethod
    def get_main_attribute(cls, widget: ui.IfcImportWidget) -> str:
        return widget.ui.main_attribute_widget.ui.le_attribute_name.text()

    @classmethod
    def set_status(cls, progress_bar:Progressbar, status: str):
        progress_bar.ui.label.setText(status)

    @classmethod
    def set_progress(cls, progress_bar:Progressbar, value: int):
       progress_bar.ui.progressBar.setValue(value)

    @classmethod
    def create_thread_pool(cls) -> QThreadPool:
        cls.get_properties().thread_pool = QThreadPool()
        return cls.get_properties().thread_pool

    @classmethod
    def get_threadpool(cls) -> QThreadPool:
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
        return cls.get_properties().thread_pool

    @classmethod
    def get_properties(cls) -> IfcImportProperties:
        return som_gui.IfcImportProperties

    @classmethod
    def set_progressbars_visible(cls, widget: ui.IfcImportWidget, visible: bool):
        widget.ui.scrollArea.setVisible(visible)

    @classmethod
    def get_ifc_paths(cls, widget: ui.IfcImportWidget) -> list[str]:
        return tool.Util.get_path_from_fileselector(widget.ui.file_selector_widget)

    @classmethod
    def create_importer(cls):
        widget = ui.IfcImportWidget()
        from som_gui.core.ifc_importer import IFC_PATH
        file_extension = "IFC Files (*.ifc *.IFC);;"
        tool.Util.fill_file_selector(widget.ui.file_selector_widget, "Ifc File", file_extension, IFC_PATH)
        prop = cls.get_properties()
        cls.set_progressbars_visible(widget, False)
        return widget

    @classmethod
    def create_runner(cls, progress_bar: Progressbar, path: os.PathLike | str):
        if not os.path.exists(path):
            return
        return IfcImportRunner(path, progress_bar)

    @classmethod
    def set_close_button_text(cls, widget: ui.IfcImportWidget, text: str):
        widget.ui.button_close.setText(widget.tr(text))

    @classmethod
    def set_run_button_enabled(cls, widget: ui.IfcImportWidget, enabled: bool):
        widget.ui.button_run.setEnabled(enabled)

    @classmethod
    def add_progress_bar(cls,widget:ui.IfcImportWidget,progress_bar:Progressbar):
        widget.ui.layout_progress_bar.addWidget(progress_bar)

    @classmethod
    def clear_progress_bars(cls,widget:ui.IfcImportWidget):
        layout = widget.ui.layout_progress_bar
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()