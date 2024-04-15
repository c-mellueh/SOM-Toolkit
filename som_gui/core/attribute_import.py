from __future__ import annotations
from typing import Type, TYPE_CHECKING
import os
import logging
import ifcopenshell

if TYPE_CHECKING:
    from som_gui import tool
import time


def open_window(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    if attribute_import.is_window_allready_build():
        attribute_import.get_attribute_widget().show()
        return

    window = attribute_import.create_window()
    attribute_import_widget = attribute_import.create_import_widget()
    ifc_import_widget = ifc_importer.create_importer()
    window.layout().addWidget(ifc_import_widget)
    window.layout().addWidget(attribute_import_widget)
    attribute_import_widget.hide()

    attribute_import.set_ifc_importer_widget(ifc_import_widget)
    attribute_import.connect_buttons(attribute_import.get_buttons())
    window.show()


def run_clicked(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    ifc_import_widget = attribute_import.get_ifc_import_widget()
    ifc_paths, main_pset_name, main_attribute_name = ifc_importer.read_inputs(ifc_import_widget)

    if not ifc_importer.check_inputs(ifc_paths, main_pset_name, main_attribute_name):
        return

    attribute_import.reset_abort()

    ifc_importer.set_run_button_enabled(False, ifc_import_widget)
    ifc_importer.set_close_button_text("Abbrechen", ifc_import_widget)
    attribute_import.set_main_pset(main_pset_name)
    attribute_import.set_main_attribute(main_attribute_name)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    ifc_importer.set_progressbar_visible(ifc_import_widget, True)
    ifc_importer.set_progress(ifc_import_widget, 0)
    for path in ifc_paths:
        ifc_importer.set_status(ifc_import_widget, f"Import '{os.path.basename(path)}'")
        runner = attribute_import.create_import_runner(path)
        attribute_import.connect_ifc_import_runner(runner)
        pool.start(runner)


def accept_clicked():
    pass


def abort_clicked():
    pass


def close_clicked():
    pass


def paint_property_set_table():
    pass


def paint_attribute_table():
    pass


def paint_value_table():
    pass


def ifc_import_started(runner, attribute_import: Type[tool.AttributeImport],
                       ifc_importer: Type[tool.IfcImporter]):
    widget = attribute_import.get_ifc_import_widget()
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_status(widget, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(widget, 0)


def ifc_import_finished(runner, attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    """
    creates and runs Modelcheck Runnable
    """

    attribute_import.destroy_import_runner(runner)
    ifc_import_widget = attribute_import.get_ifc_import_widget()
    ifc_importer.set_status(ifc_import_widget, f"Import Abgeschlossen")
    attribute_import_runner = attribute_import.create_attribute_import_runner(runner.ifc)
    attribute_import.connect_attribute_import_runner(attribute_import_runner)
    attribute_import.set_current_runner(attribute_import_runner)
    attribute_import.get_attribute_import_threadpool().start(attribute_import_runner)


def start_attribute_import(file: ifcopenshell.file, attribute_import: Type[tool.AttributeImport]):
    pass




def attribute_import_finished(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    ifc_import_widget = attribute_import.get_ifc_import_widget()

    if attribute_import.is_aborted():
        ifc_importer.set_progressbar_visible(ifc_import_widget, False)
        ifc_importer.set_close_button_text(f"Close", ifc_import_widget)
        ifc_importer.set_run_button_enabled(False, ifc_import_widget)
        return

    time.sleep(0.2)
    if not attribute_import.attribute_import_is_running():
        attribute_import.last_import_finished()
        ifc_importer.set_close_button_text(f"Close", ifc_import_widget)
        ifc_importer.set_run_button_enabled(True, ifc_import_widget)
    else:
        logging.info(f"Prüfung von Datei abgeschlossen, nächste Datei ist dran.")


def last_import_finished(attribute_import: Type[tool.AttributeImport]):
    pass


