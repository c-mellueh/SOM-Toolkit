from __future__ import annotations

import logging
import os
import tempfile
from datetime import datetime
from time import time, sleep
from typing import TYPE_CHECKING

import ifcopenshell
import openpyxl
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem, QWidget
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.worksheet.table import Table, TableStyleInfo

from ..icons import get_icon
from ..modelcheck import modelcheck, sql
from ..qt_designs import ui_modelcheck
from ..settings import get_ifc_path, get_issue_path, set_ifc_path, set_issue_path

if TYPE_CHECKING:
    from ..main_window import MainWindow

FILE_SPLIT = "; "
HEADER = ["Datum", "GUID", "Beschreibung", "Typ", "Name", "PropertySet", "Attribut", "Datei",
          "Bauteilklassifikation"]


class ModelcheckWindow(QWidget):
    def __init__(self, main_window: MainWindow):
        super(ModelcheckWindow, self).__init__()
        self.main_window = main_window
        self.widget = ui_modelcheck.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Modelcheck")
        self.widget.button_ifc.clicked.connect(self.ifc_file_dialog)
        self.widget.button_export.clicked.connect(self.export_file_dialog)
        pset, attribute = self.get_main_attribute()
        self.widget.line_edit_ident_pset.setText(pset)
        self.widget.line_edit_ident_attribute.setText(attribute)
        self.data_base_path = None
        self.widget.label_ifc_missing.hide()
        self.widget.label_export_missing.hide()
        self.widget.label_export_missing.setStyleSheet("QLabel { color : red; }")
        self.widget.label_ifc_missing.setStyleSheet("QLabel { color : red; }")
        self.widget.line_edit_ifc.textEdited.connect(self.widget.label_ifc_missing.hide)
        self.widget.line_edit_export.textEdited.connect(self.widget.label_export_missing.hide)
        self.widget.line_edit_ident_pset.textEdited.connect(self.fill_table)
        self.widget.line_edit_ident_attribute.textEdited.connect(self.fill_table)
        self.widget.progress_bar.hide()
        self.widget.label_status.hide()
        self.fill_table()

        if get_ifc_path():
            self.widget.line_edit_ifc.setText(get_ifc_path())
        if get_issue_path():
            self.widget.line_edit_export.setText(get_issue_path())

        self.active_threads = 0
        self.thread_pool = QThreadPool()
        self.widget.buttonBox.accepted.connect(self.accept)
        self.widget.buttonBox.rejected.connect(self.hide)
        self.show()
        self.start_time = None
        self.end_time = None
        self.threads = set()

    def fill_table(self):
        issues = self.get_issue_description()
        self.widget.table_widget.setRowCount(0)
        self.widget.table_widget.setRowCount(len(issues))
        for index, (key, description) in enumerate(sorted(issues.items())):
            self.widget.table_widget.setItem(index, 0, QTableWidgetItem(f"Fehler {key}"))
            self.widget.table_widget.setItem(index, 1, QTableWidgetItem(description))

    def accept(self) -> None:
        allow = True
        if not self.get_ifc_path():
            if self.widget.line_edit_ifc.text():
                self.widget.label_ifc_missing.setText("Path doesn't exist!")
            else:
                self.widget.label_ifc_missing.setText("IFC File Path is missing!")
            self.widget.label_ifc_missing.show()
            allow = False
        export_path = self.widget.line_edit_export.text()
        if not export_path:
            self.widget.label_export_missing.setText("Export Path is missing!")
            self.widget.label_export_missing.show()
            allow = False

        elif not os.path.exists(os.path.dirname(export_path)):
            self.widget.label_export_missing.setText("Path doesn't exist!")
            self.widget.label_export_missing.show()
            allow = False

        if allow:
            self.start_modelcheck()

    def ifc_file_dialog(self):
        file_text = "IFC Files (*.ifc *.IFC);;"
        path = QFileDialog.getOpenFileNames(self, "IFC-Files", get_ifc_path(), file_text)[0]
        if not path:
            return
        set_ifc_path(path)
        self.widget.line_edit_ifc.setText(FILE_SPLIT.join(path))

    def export_file_dialog(self):
        file_text = "Excel File (*.xlsx);;"
        path = QFileDialog.getSaveFileName(self, "Issue-Excel", get_issue_path(), file_text)[0]
        if not path:
            return
        set_issue_path(path)
        self.widget.line_edit_export.setText(path)

    def get_ifc_path(self) -> list[str]:
        paths = self.widget.line_edit_ifc.text().split(FILE_SPLIT)
        result = list()
        for path in paths:
            if not os.path.exists(path):
                logging.error(f"IFC-File does not exist: '{path}'")
            else:
                result.append(path)
        return result

    def get_main_attribute(self) -> (str, str):
        proj = self.main_window.project
        ident_attributes = dict()
        ident_psets = dict()
        for obj in proj.objects:
            ident_pset = obj.ident_attrib.property_set.name
            ident_attribute = obj.ident_attrib.name
            if not ident_pset in ident_psets:
                ident_psets[ident_pset] = 0
            if not ident_attribute in ident_attributes:
                ident_attributes[ident_attribute] = 0
            ident_psets[ident_pset] += 1
            ident_attributes[ident_attribute] += 1

        ident_attribute = (sorted(ident_attributes.items(), key=lambda x: x[1]))
        ident_pset = (sorted(ident_psets.items(), key=lambda x: x[1]))
        if ident_attribute and ident_pset:
            return ident_pset[0][0], ident_attribute[0][0]
        else:
            return "", ""

    def get_issue_description(self):
        main_pset = self.widget.line_edit_ident_pset.text()
        main_attrib = self.widget.line_edit_ident_attribute.text()

        return {1: f"Propertyset '{main_pset}' fehlt",
                2: f"{main_pset}:{main_attrib} fehlt",
                3: "Bauteilklassifikation nicht in SOM vorhanden",
                4: "GUID ist in mehreren Dateien identisch",
                5: "PropertySet Fehlt",
                6: "Attribut Fehlt",
                7: "Attribut hat falschen Wert",
                8: "Gruppe hat falsches Subelement",
                9: "Zwischenebene besitzt verschiedene Klassen als Subelement",
                10: "Gruppe besitzt keine Subelemente",
                11: "Element hat keine Gruppenzuweisen",
                12: "Zu Viele Subelemente"}

    def on_started(self, path):
        logging.info(f"Start {path}")
        self.active_threads += 1

    def on_finished(self, path):
        self.active_threads -= 1
        logging.info(f"Finish {path}")
        logging.info(f"active Threads: {self.active_threads}")
        if self.active_threads == 0:
            self.end_modelcheck()

    def start_modelcheck(self):
        self.start_time = time()
        self.widget.buttonBox.setEnabled(False)
        proj = self.main_window.project
        ifc = self.get_ifc_path()
        pset = self.widget.line_edit_ident_pset.text()
        attribute = self.widget.line_edit_ident_attribute.text()
        self.data_base_path = tempfile.NamedTemporaryFile().name
        export_path = self.widget.line_edit_export.text()
        self.runner = MainRunnable(modelcheck.check_file, ifc, proj, pset, attribute, self.data_base_path, export_path)
        self.runner.signaller.started.connect(self.on_started)
        self.runner.signaller.finished.connect(self.on_finished)
        self.runner.signaller.progress.connect(self.update_progress_bar)
        self.runner.signaller.status.connect(self.update_status)

        self.widget.label_status.show()
        self.widget.progress_bar.show()
        self.widget.progress_bar.reset()
        self.thread_pool = QThreadPool()
        self.thread_pool.start(self.runner)

    def end_modelcheck(self):
        logging.info("Modelcheck Done")
        self.widget.label_status.setText("Create")
        self.widget.buttonBox.setEnabled(True)
        self.end_time = time()
        print(f"Elapsed Time: {self.end_time - self.start_time}")

    def update_progress_bar(self, value):
        self.widget.progress_bar.setValue(value)

    def update_status(self, value):
        self.widget.label_status.setText(value)


class MainRunnable(QRunnable):
    def __init__(self, target, path, project, property_set, attribute, db_path, export_path):
        super(MainRunnable, self).__init__()
        self.target = target
        self.path = path
        self.project = project
        self.property_set = property_set
        self.attribute = attribute
        self.db_path = db_path
        self.signaller = Signaller()
        self.export_path = export_path

    def get_check_file_list(self, ifc_paths: str) -> list[str]:
        check_list = list()
        if not isinstance(ifc_paths, list):
            if not isinstance(ifc_paths, str):
                return check_list
            if not os.path.isfile(ifc_paths):
                return check_list
            check_list.append(ifc_paths)

        else:
            for path in ifc_paths:
                if os.path.isdir(path):
                    for file in os.listdir(path):
                        file_path = os.path.join(path, file)
                        check_list.append(file_path)
                else:
                    check_list.append(path)
        return check_list

    def run(self) -> None:
        self.signaller.started.emit(self.path)
        sql.guids = dict()
        sql.create_tables(self.db_path)

        files = self.get_check_file_list(self.path)
        for file in files:
            self.check_file(file)
        self.signaller.finished.emit(self.path)
        self.signaller.status.emit("Modelcheck Done!")
        self.create_issues(self.db_path, self.export_path)

    def check_file(self, file):
        file_name, extension = os.path.splitext(file)
        base_name = os.path.basename(file)
        self.signaller.status.emit(f"Import {base_name}")
        self.signaller.progress.emit(0)
        sleep(0.1)
        if extension.lower() != ".ifc":
            return
        ifc = ifcopenshell.open(file)
        self.signaller.status.emit(f"Import Done!")
        sleep(0.1)
        self.check_all_elements(ifc, base_name)

    def check_all_elements(self, ifc: ifcopenshell.file, file_name: str):
        db_name = self.db_path
        project_name = self.project.name
        modelcheck.remove_existing_issues(db_name, project_name, datetime.today(), file_name)
        root_groups = [group for group in ifc.by_type("IfcGroup") if not modelcheck.get_parent_group(group)]
        ident_dict = {obj.ident_value: obj for obj in self.project.objects}
        group_dict = dict()
        group_parent_dict = dict()
        for element in root_groups:
            group_dict[element] = dict()
            modelcheck.build_group_structure(element, group_dict[element], self.property_set, self.attribute,
                                             group_parent_dict)

        element: ifcopenshell.entity_instance
        object_count = len(list(ifc.by_type("IfcObject")))

        last_prog = 0
        self.signaller.status.emit(f"Check '{file_name}'")
        for index, element in enumerate(ifc.by_type("IfcObject"), start=1):

            progress = int(index / object_count * 100)
            self.signaller.progress.emit(progress)
            self.signaller.status.emit(f"Check '{file_name}' [{index}/{object_count}]")
            if element.is_a("IfcElement"):
                modelcheck.check_element(element, self.property_set, self.attribute, db_name, file_name, ident_dict,
                                         modelcheck.ELEMENT, project_name)
            elif element.is_a("IfcGroup"):
                if element in group_dict:
                    modelcheck.check_group_structure(element, group_dict, 0, self.property_set, self.attribute, db_name,
                                                     file_name, project_name, ident_dict,
                                                     group_parent_dict)

    def create_issues(self, db_name, path):
        def get_max_width():
            col_widths = [0 for _ in range(worksheet.max_column)]
            for row_index, row in enumerate(worksheet, start=1):
                for col_index, cell in enumerate(row):
                    length = len(str(cell.value))
                    if length > col_widths[col_index]:
                        col_widths[col_index] = length
            return col_widths

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.mkdir(directory)

        issues = sql.query_issues(db_name)

        self.signaller.status.emit(f"{len(issues)} Fehler gefunden!")

        if len(issues) == 0:
            self.signaller.status.emit("Modelle fehlerfrei!")
            return

        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        for col_index, value in enumerate(HEADER, start=1):
            worksheet.cell(1, col_index, value)

        last_cell = worksheet.cell(1, 8)

        for row_index, column in enumerate(issues, start=2):
            for column_index, value in enumerate(column, start=1):
                last_cell = worksheet.cell(row_index, column_index, value)  # remove Whitespace

        table_zone = f"A1:{last_cell.coordinate}"
        tab = Table(displayName="Issues", ref=table_zone)
        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
                               showRowStripes=True, showColumnStripes=True)
        tab.tableStyleInfo = style
        worksheet.add_table(tab)

        max_widths = get_max_width()

        # autoFit Column
        dim_holder = DimensionHolder(worksheet=worksheet)
        for col in range(worksheet.min_column, worksheet.max_column + 1):
            dim_holder[get_column_letter(col)] = ColumnDimension(worksheet, min=col, max=col,
                                                                 width=max_widths[col - 1] * 1.1)
        worksheet.column_dimensions = dim_holder

        self.save_workbook(workbook, path)

    def save_workbook(self, workbook, path):
        try:
            workbook.save(path)
        except PermissionError:
            print("-" * 60)
            print(f"folgende Datei ist noch geöffnet: {path} \n Datei schließen und beliebige Taste Drücken")
            input("Achtung! Datei wird danach überschrieben!")
            self.save_workbook(workbook, path)


class Signaller(QObject):
    started = Signal(str)
    finished = Signal(str)
    progress = Signal(int)
    status = Signal(str)
