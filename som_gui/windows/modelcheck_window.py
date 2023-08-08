from __future__ import annotations

import logging
import os
from time import time
import tempfile
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem, QWidget

from ..icons import get_icon
from ..modelcheck import modelcheck, sql,output
from ..qt_designs import ui_modelcheck
from ..settings import get_ifc_path, get_issue_path, set_ifc_path, set_issue_path

if TYPE_CHECKING:
    from ..main_window import MainWindow

FILE_SPLIT = "; "


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
                print(f"IFC-File does not exist: '{path}'")
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

    def on_started(self,path):
        print(f"Start {path}")
        self.active_threads += 1

    def on_finished(self,path):
        self.active_threads -= 1
        print(f"Finish {path}")
        print(f"active Threads: {self.active_threads}")
        if self.active_threads == 0:
            self.end_modelcheck()

    def start_modelcheck(self):
        def add_runnable(path) -> MainRunnable:
            runnable = MainRunnable(modelcheck.check_file, path, self.main_window.project, property_set, attribute,
                                    self.data_base_path)
            runnable.signaller.started.connect(self.on_started)
            runnable.signaller.finished.connect(self.on_finished)
            self.threads.add(runnable)
            return runnable

        self.start_time = time()
        sql.guids = dict()
        ifc_paths = self.get_ifc_path()
        self.thread_pool = QThreadPool()
        self.threads = set()


        self.data_base_path = tempfile.NamedTemporaryFile().name

        sql.create_tables(self.data_base_path)

        property_set = self.widget.line_edit_ident_pset.text()
        attribute = self.widget.line_edit_ident_attribute.text()

        if not isinstance(ifc_paths, list):
            if not isinstance(ifc_paths, str):
                return
            if not os.path.isfile(ifc_paths):
                return
            add_runnable(ifc_paths)

        else:
            for path in ifc_paths:
                if os.path.isdir(path):
                    for file in os.listdir(path):
                        file_path = os.path.join(path, file)
                        add_runnable(file_path)
                else:
                    add_runnable(path)

        self.widget.buttonBox.setEnabled(False)

        for thread in self.threads:
            self.thread_pool.start(thread)

    def end_modelcheck(self):
        logging.info("Modelcheck Done")
        self.widget.buttonBox.setEnabled(True)
        output.create_issues(self.data_base_path, self.widget.line_edit_export.text())
        self.end_time = time()
        print(f"Elapsed Time: {self.end_time}-{self.start_time}")



class MainRunnable(QRunnable):
    def __init__(self, target, path, project, property_set, attribute, db_path):
        super(MainRunnable, self).__init__()
        self.target = target
        self.path = path
        self.project = project
        self.property_set = property_set
        self.attribute = attribute
        self.db_path = db_path
        self.signaller = Signaller()


    def run(self) -> None:
        self.signaller.started.emit(self.path)

        self.target(self.path, self.project, self.property_set, self.attribute, self.db_path)

        self.signaller.finished.emit(self.path)

class Signaller(QObject):
    started = Signal(str)
    finished = Signal(str)