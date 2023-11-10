from __future__ import annotations  # make own class referencable

import logging
import os
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QBrush,QStandardItemModel
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QDialog,QSizePolicy,QHeaderView,QTableView
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

from . import functions
from ...qt_designs import ui_attribute_import_window_v2, ui_attribute_import_settings_window

STANDARD_CHECK_STATE = False
ALL = "Alles"
GROUP = "Gruppe"
ELEMENT = "Element"
TYPE = "Type"
PROPERTYSETS = "PropertySets"

class AttributeImport(QWidget):
    def __init__(self, main_window: MainWindow):
        self.main_window = main_window
        self.project = self.main_window.project
        self.main_window.model_control_window = self
        super(AttributeImport, self).__init__()
        self.widget = ui_attribute_import_window_v2.Ui_Form()
        self.widget.setupUi(self)
        self.show()
        self.setWindowTitle("Modellinformationen Einlesen")
        self.setWindowIcon(get_icon())
        self.thread_pool = QThreadPool()
        self.runner: None = None
        self.widget.button_settings.setIcon(get_settings_icon())
        self.widget.button_accept.hide()

        self.item_model = functions.ObjectModel()

        self.widget.table_widget_property_set.setModel(QStandardItemModel())
        self.widget.table_widget_property_set.model().setHorizontalHeaderLabels(["PropertySet","Anzahl"])
        hor_header = self.widget.table_widget_property_set.horizontalHeader()
        hor_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.widget.table_widget_attribute.setModel(QStandardItemModel())
        self.widget.table_widget_attribute.model().setHorizontalHeaderLabels(["Attribut", "Anzahl","Eindeutig"])
        self.widget.table_widget_value.setModel(QStandardItemModel())
        self.widget.table_widget_value.model().setHorizontalHeaderLabels(["Wert","Anzahl"])

        self.widget.check_box_values.setCheckState(Qt.CheckState.Unchecked)
        self.combi_mode = False
        functions.init(self)
        functions.hide_progress_bar(self,True)
        functions.hide_tables(self,True)

    def hide_items(self,items:set|list,value:bool) -> None:
        func_name = "hide" if value else "show"
        for item in items:
            getattr(item,func_name)()
        self.adjustSize()

    def set_object_count(self,count:int):
        self.widget.label_object_count.setText(f"Anzahl: {count}")

    @staticmethod
    def clear_table(table:QTableView):
        model = table.model()
        for row in reversed(range(model.rowCount())):
            model.removeRow(row)