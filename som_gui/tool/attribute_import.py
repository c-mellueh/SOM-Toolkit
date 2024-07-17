from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
from som_gui.module.attribute_import import ui, trigger
from som_gui import tool
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QRunnable, QObject, Signal, QThreadPool
import ifcopenshell

if TYPE_CHECKING:
    from som_gui.module.attribute_import.prop import AttributeImportProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget


class AttributeImportRunner(QRunnable):
    def __init__(self, ifc_file: ifcopenshell.file):
        super().__init__()
        self.file = ifc_file
        self.signaller = Signaller()

    def run(self):
        trigger.start_attribute_import(self.file)
        self.signaller.finished.emit()


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class AttributeImport(som_gui.core.tool.AttributeImport):
    @classmethod
    def get_properties(cls) -> AttributeImportProperties:
        return som_gui.AttributeImportProperties

    @classmethod
    def connect_import_buttons(cls):
        trigger.connect_import_buttons(cls.get_properties().run_button, cls.get_properties().abort_button)

    @classmethod
    def add_attribute_import_widget_to_window(cls, attribute_import_widget):
        cls.get_window().layout().addWidget(attribute_import_widget)
        attribute_import_widget.hide()

    @classmethod
    def add_ifc_importer_to_window(cls, ifc_importer):
        cls.get_properties().ifc_importer = ifc_importer
        cls.get_properties().ifc_button = ifc_importer.widget.button_ifc
        cls.get_properties().run_button = ifc_importer.widget.button_run
        cls.get_properties().abort_button = ifc_importer.widget.button_close
        cls.get_properties().status_label = ifc_importer.widget.label_status
        cls.get_window().layout().addWidget(ifc_importer)

    @classmethod
    def is_window_allready_build(cls) -> bool:
        return cls.get_attribute_widget() is not None

    @classmethod
    def get_attribute_widget(cls) -> ui.AttributeImportWidget:
        return cls.get_properties().attribute_import_widget

    @classmethod
    def get_window(cls):
        return cls.get_properties().active_window

    @classmethod
    def create_window(cls) -> ui.AttributeImportWindow:
        prop = cls.get_properties()
        prop.active_window = ui.AttributeImportWindow()
        return prop.active_window

    @classmethod
    def create_import_widget(cls) -> ui.AttributeImportWidget:
        prop = cls.get_properties()
        prop.attribute_import_widget = ui.AttributeImportWidget()
        return prop.attribute_import_widget

    @classmethod
    def get_ifc_import_widget(cls):
        return cls.get_properties().ifc_importer


    @classmethod
    def connect_buttons(cls, button_list: list[QPushButton]):
        trigger.connect_import_buttons(*button_list)

    @classmethod
    def set_main_pset(cls, main_pset_name: str) -> None:
        cls.get_properties().main_pset = main_pset_name

    @classmethod
    def get_main_pset(cls) -> str:
        return cls.get_properties().main_pset

    @classmethod
    def set_main_attribute(cls, main_attribute_name: str) -> None:
        cls.get_properties().main_attribute = main_attribute_name

    @classmethod
    def get_main_attribute(cls) -> str:
        return cls.get_properties().main_attribute

    @classmethod
    def is_aborted(cls) -> bool:
        return cls.get_properties().import_is_aborted

    @classmethod
    def reset_abort(cls) -> None:
        cls.get_properties().import_is_aborted = False

    @classmethod
    def create_import_runner(cls, ifc_import_path: str) -> QRunnable:
        status_label = cls.get_ifc_import_widget().widget.label_status
        runner = tool.IfcImporter.create_runner(status_label, ifc_import_path)
        cls.get_properties().ifc_import_runners.append(runner)
        return runner

    @classmethod
    def connect_ifc_import_runner(cls, runner) -> None:
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def destroy_import_runner(cls, runner) -> None:
        cls.get_properties().ifc_import_runners.remove(runner)

    @classmethod
    def create_attribute_import_runner(cls, ifc_file: ifcopenshell.file) -> AttributeImportRunner:
        return AttributeImportRunner(ifc_file)

    @classmethod
    def connect_attribute_import_runner(cls, runner: AttributeImportRunner) -> None:
        trigger.connect_attribute_import_runner(runner)

    @classmethod
    def set_current_runner(cls, runner) -> AttributeImportRunner:
        cls.get_properties().runner = runner

    @classmethod
    def get_attribute_import_threadpool(cls):
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def attribute_import_is_running(cls):
        return cls.get_attribute_import_threadpool().activeThreadCount() > 0

    @classmethod
    def last_import_finished(cls):
        trigger.last_import_finished()
