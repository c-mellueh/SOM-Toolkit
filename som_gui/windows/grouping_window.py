from __future__ import annotations

import logging
import os
import tempfile
from datetime import datetime
from time import sleep
from typing import TYPE_CHECKING

import SOMcreator
import ifcopenshell
import openpyxl
from PySide6.QtCore import QObject, Signal, QRunnable,QSize
from PySide6.QtWidgets import  QLineEdit
from SOMcreator import classes
from SOMcreator import constants as som_constants
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.worksheet.table import Table, TableStyleInfo

from ..ifc_modification import modelcheck, sql, issues
from .ifc_mod_window import IfcWindow,IfcRunner

if TYPE_CHECKING:
    from ..main_window import MainWindow

FILE_SPLIT = "; "
HEADER = ["Datum", "GUID", "Beschreibung", "Typ", "Name", "PropertySet", "Attribut", "Datei",
          "Bauteilklassifikation"]


class GroupingWindow(IfcWindow):
    def __init__(self, main_window: MainWindow):
        super(GroupingWindow, self).__init__(main_window)
        self.setWindowTitle("Gruppen erzeugen")
        self.create_group_line_input()
        self.set_fixed_sizes()
        self.adjustSize()

    def set_fixed_sizes(self):
        def set_line_edit_size(le:QLineEdit):
            text = le.text()
            fm = le.fontMetrics()
            width = fm.boundingRect(text).width()
            le.setMinimumSize(max(width,le.width()),le.height())

        set_line_edit_size(self.widget.line_edit_ident_pset)
        set_line_edit_size(self.widget.line_edit_ident_attribute)

    def create_group_line_input(self):
        self.line_edit_group_pset = QLineEdit()
        self.widget.layout_attribute.addWidget(self.line_edit_group_pset, 1, 0, 1, 1)
        self.line_edit_group_attrib = QLineEdit()
        self.widget.layout_attribute.addWidget(self.line_edit_group_attrib, 1, 1, 1, 1)
        self.line_edit_group_pset.setPlaceholderText("Gruppen PropertySet")
        self.line_edit_group_attrib.setPlaceholderText("Gruppen Attribut")
        self.line_edit_group_attrib.setText(self.main_window.project.aggregation_attribute)
        self.line_edit_group_pset.setText(self.main_window.project.aggregation_pset)

    def start_task(self) -> tuple:
        proj, ifc, pset, attribute, export_path = super(GroupingWindow, self).start_task()
        group_pset = self.line_edit_group_pset.text()
        group_attribute = self.line_edit_group_attrib.text()
        self.runner = Grouping(ifc, proj, pset, attribute,export_path,group_pset,group_attribute)
        self.connect_runner(self.runner)
        self.thread_pool.start(self.runner)

        return proj,ifc,pset,attribute,export_path

class Grouping(IfcRunner):
    def __init__(self, ifc_paths: str, project: classes.Project, main_pset: str, main_attribute: str, issue_path: str,group_pset:str,group_attrib:str):
        super(Grouping, self).__init__(ifc_paths, project, main_pset, main_attribute, issue_path,"Modelcheck")
        self.group_pset = group_pset
        self.group_attribute = group_attrib

    def run(self) -> None:
        super(Grouping, self).run()

    def run_file_function(self, file_path) -> ifcopenshell.file:
        ifc_file_path = super(Grouping, self).run_file_function(file_path)
