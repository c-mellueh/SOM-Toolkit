from __future__ import annotations  # make own class referencable

import logging
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QBrush,QStandardItem,QStandardItemModel
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QDialog
from SOMcreator import classes, value_constants
from ifcopenshell.util.element import get_pset
from ...widgets import ifc_widget

from ... import settings
from ...icons import get_icon, get_settings_icon
from ...ifc_modification.modelcheck import get_identifier
from ...settings import EXISTING_ATTRIBUTE_IMPORT, RANGE_ATTRIBUTE_IMPORT, REGEX_ATTRIBUTE_IMPORT, \
    COLOR_ATTTRIBUTE_IMPORT
from ...widgets import property_widget

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow
    from som_gui.windows.attribute_import import gui
from ...qt_designs import ui_attribute_import_window, ui_attribute_import_settings_window


class ObjectModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
class ObjectItem(QStandardItem):
    def __init__(self):
        super().__init__()



class IfcImportRunner(ifc_widget.IfcRunner):
    def __init__(self, ifc_paths: list[str], project: classes.Project, main_pset: str, main_attribute: str,
                 function_name: str):
        self.data_dict = dict()
        self.count_dict = dict()

        super(IfcImportRunner, self).__init__(ifc_paths, project, main_pset, main_attribute,
                                              function_name)


def init(window: gui.AttributeImport):
    def connect():
        window.widget.button_ifc.clicked.connect(lambda: ifc_button_clicked(window))  # IFC Auswahl
        window.widget.combo_box_name.currentIndexChanged.connect(lambda: object_index_changed(window))
        window.widget.combo_box_group.currentIndexChanged.connect(lambda: type_index_changed(window))
        window.widget.check_box_values.clicked.connect(lambda: main_checkbox_clicked(window))
        window.widget.button_run.clicked.connect(lambda: button_run_clicked(window))
        window.widget.button_accept.clicked.connect(lambda:button_accept_clicked(window))
        window.widget.button_settings.clicked.connect(lambda: settings_clicked(window))
        window.widget.button_abort.clicked.connect(lambda: abort_clicked(window))
        window.widget.table_widget_property_set.clicked.connect(pset_table_clicked)
        window.widget.table_widget_attribute.clicked.connect(attribute_table_clicked)
        window.widget.table_widget_attribute.doubleClicked.connect(attribute_table_double_clicked)
        window.widget.table_widget_value.clicked.connect(value_table_clicked)

    connect()
    ifc_widget.set_main_attribute(window.project, window.widget.line_edit_ident_pset,
                                  window.widget.line_edit_ident_attribute)
    ifc_widget.auto_set_ifc_path(window.widget.line_edit_ifc)


def ifc_button_clicked(window: gui.AttributeImport) -> None:
    path = ifc_widget.ifc_file_dialog(window, window.widget.line_edit_ifc)
    if path is None:
        return


def button_run_clicked(window: gui.AttributeImport) -> None:
    path = window.widget.line_edit_ifc.text()
    paths = path.split(settings.PATH_SEPERATOR)
    main_property_set_name = window.widget.line_edit_ident_pset.text()
    main_attribute_name = window.widget.line_edit_ident_attribute.text()
    import_ifc(window,paths, main_property_set_name, main_attribute_name)


def import_ifc(window:gui.AttributeImport,paths: list[str], main_property_set_name: str, main_attribute_name: str) -> None:
    runner = IfcImportRunner(paths,window.project,main_property_set_name,main_attribute_name,"ImportIFC")
    connect_runner_signals(window,runner)
    window.thread_pool.start(runner)
def connect_runner_signals(window:gui.AttributeImport,runner:IfcImportRunner):
    runner.signaller.started.connect(lambda: runner_started(window))
    runner.signaller.finished.connect(lambda text : runner_finished(window,text))
    runner.signaller.progress.connect(window.widget.progress_bar.setValue)
    runner.signaller.status.connect(lambda text: update_status(window,text))
def runner_started(window:gui.AttributeImport):
    logging.info(f"Runner Started")
    hide_progress_bar(window,False)
    window.widget.button_run.hide()
    window.widget.button_accept.show()
    window.widget.button_accept.setEnabled(False)

def update_status(window:gui.AttributeImport,status):
    logging.info(f"Runner Status: {status}")
    window.widget.label_status.setText(status)

def runner_finished(window:gui.AttributeImport,text):
    logging.info(f"Runner finished: {text}")
    hide_progress_bar(window,True)
    hide_tables(window,False)
    window.widget.button_accept.setEnabled(True)

def object_index_changed(window: gui.AttributeImport):
    pass


def type_index_changed(window: gui.AttributeImport):
    pass


def pset_table_clicked():
    pass


def attribute_table_clicked():
    pass


def attribute_table_double_clicked():
    pass


def value_table_clicked():
    pass


def main_checkbox_clicked():
    pass


def settings_clicked():
    pass


def abort_clicked():
    pass

def button_accept_clicked(window:gui.AttributeImport):
    pass


def hide_progress_bar(window: gui.AttributeImport, value: bool) -> None:
    items = [window.widget.label_status, window.widget.progress_bar]
    window.hide_items(items, value)


def hide_tables(window: gui.AttributeImport, value: bool) -> None:
    items = [window.widget.splitter_tables, window.widget.combo_box_group, window.widget.combo_box_name,
             window.widget.label_object_count, window.widget.label_status]
    window.hide_items(items, value)



