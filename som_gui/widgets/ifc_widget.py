from __future__ import annotations

import logging
import os
from time import time, sleep
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from PySide6.QtWidgets import QFileDialog, QWidget, QLineEdit, QLabel
from SOMcreator import classes

import som_gui.tool
from som_gui import settings
from som_gui.icons import get_icon
from som_gui.qt_designs import ui_ifc_widget

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow

ABORT = "ABORT"


class IfcWidget(QWidget):
    def __init__(self, main_window: MainWindow):
        super(IfcWidget, self).__init__()
        self.main_window = main_window
        self.widget = ui_ifc_widget.Ui_Form()
        self.widget.setupUi(self)
        self.widget.button_ifc.clicked.connect(lambda: ifc_file_dialog(self, self.widget.line_edit_ifc))
        self.widget.button_export.clicked.connect(self.export_file_dialog)

        self.active_threads = 0
        self.thread_pool = QThreadPool()
        self.widget.button_run.clicked.connect(self.accept)
        self.widget.button_close.clicked.connect(self.close_button_clicked)
        self.start_time = None
        self.end_time = None
        self.task_is_running = False
        self.format_window()
        self.set_min_size()
        self.show()

    def format_window(self):
        self.setWindowIcon(get_icon())
        from som_gui import tool
        set_main_attribute(tool.Project.get(), self.widget.line_edit_ident_pset,
                           self.widget.line_edit_ident_attribute)
        self.widget.label_ifc_missing.hide()
        self.widget.label_export_missing.hide()
        self.widget.label_export_missing.setStyleSheet("QLabel { color : red; }")
        self.widget.label_ifc_missing.setStyleSheet("QLabel { color : red; }")
        self.widget.line_edit_ifc.textEdited.connect(self.widget.label_ifc_missing.hide)
        self.widget.line_edit_export.textEdited.connect(self.widget.label_export_missing.hide)
        self.widget.progress_bar.hide()
        self.widget.label_status.hide()
        auto_set_ifc_path(self.widget.line_edit_ifc)
        if settings.get_issue_path():
            self.widget.line_edit_export.setText(settings.get_issue_path())

    def set_min_size(self):
        def set_line_edit_size(le: QLineEdit):
            text = le.text()
            fm = le.fontMetrics()
            width = fm.boundingRect(text).width()
            le.setMinimumSize(max(width, le.width()), le.height())

        set_line_edit_size(self.widget.line_edit_ident_pset)
        set_line_edit_size(self.widget.line_edit_ident_attribute)

    def connect_runner(self, runner: IfcRunner):
        runner.signaller.started.connect(self.on_started)
        runner.signaller.finished.connect(self.on_finished)
        runner.signaller.progress.connect(self.update_progress_bar)
        runner.signaller.status.connect(self.update_status)
        self.widget.button_close.clicked.connect(runner.abort)

    def close_button_clicked(self):
        if not self.task_is_running:
            self.hide()

    def accept(self) -> None:
        checks = set()
        checks.add(check_for_ifc(self.widget.line_edit_ifc, self.widget.label_ifc_missing))
        checks.add(check_for_export_path(self.widget.line_edit_export.text(), self.widget.label_export_missing))
        if all(checks):
            self.start_task()

    def export_file_dialog(self):
        file_text = "Excel File (*.xlsx);;"
        path = QFileDialog.getSaveFileName(self, "Issue-Excel", settings.get_issue_path(), file_text)[0]
        if not path:
            return
        settings.set_issue_path(path)
        self.widget.line_edit_export.setText(path)

    def on_started(self, path):
        logging.info(f"Start {path}")
        self.active_threads += 1

    def on_finished(self, path):
        self.active_threads -= 1
        logging.info(f"Finish {path}")
        logging.info(f"active Threads: {self.active_threads}")
        if self.active_threads == 0:
            self.end_task()

    def start_task(self) -> tuple:
        self.task_is_running = True
        self.start_time = time()
        self.widget.button_run.setEnabled(False)
        self.widget.button_close.setText(ABORT)
        proj = som_gui.tool.Project.get()
        ifc = get_ifc_path(self.widget.line_edit_ifc)
        pset = self.widget.line_edit_ident_pset.text()
        attribute = self.widget.line_edit_ident_attribute.text()
        export_path = self.widget.line_edit_export.text()
        self.widget.label_status.show()
        self.widget.progress_bar.show()
        self.widget.progress_bar.reset()
        self.thread_pool.clear()
        return proj, ifc, pset, attribute, export_path

    def end_task(self):
        logging.info("Task Done")
        self.end_time = time()
        logging.info(f"{self.end_time - self.start_time}")

        self.widget.button_run.setEnabled(True)
        self.widget.button_close.setText("Close")
        self.task_is_running = False

    def update_progress_bar(self, value):
        self.widget.progress_bar.setValue(value)

    def update_status(self, value):
        self.widget.label_status.setText(value)


class IfcRunner(QRunnable):

    def __init__(self, ifc_paths: list[str] | str, project: classes.Project, main_pset: str, main_attribute: str,
                 function_name: str):
        self.signaller = Signaller()
        super(IfcRunner, self).__init__()
        self.ifc_paths = ifc_paths
        self.project = project
        self.main_pset = main_pset
        self.main_attribute = main_attribute

        self.is_aborted = False
        self.object_count: int = 0
        self.checked_objects: int = 0
        self.function_name = function_name
        self.base_name: str | None = None

    def increment_progress(self, text="", increment_value=1):
        if self.is_aborted:
            self.set_abort_status()
            return
        self.checked_objects += increment_value
        progress = int(self.checked_objects / self.object_count * 100)
        self.signaller.progress.emit(progress)
        self.signaller.status.emit(f"{text} [{self.checked_objects}/{self.object_count}]")

    def get_check_file_list(self) -> set[str]:
        check_list = set()
        if not isinstance(self.ifc_paths, list):
            if not isinstance(self.ifc_paths, str):
                return check_list
            if not os.path.isfile(self.ifc_paths):
                return check_list
            check_list.add(self.ifc_paths)

        else:
            for path in self.ifc_paths:
                if os.path.isdir(path):
                    for file in os.listdir(path):
                        file_path = os.path.join(path, file)
                        check_list.add(file_path)
                else:
                    check_list.add(path)

        return set(file for file in check_list if file.lower().endswith(".ifc"))

    def set_abort_status(self):
        self.signaller.status.emit(f"{self.function_name} abgebrochen")
        self.signaller.progress.emit(0)

    def abort(self):
        self.is_aborted = True
        self.set_abort_status()

    def run(self) -> None:
        """if this functions gets subclassed is_done should be set to False.
        Else the finished signal might be emitted to early"""

        self.signaller.started.emit(self.ifc_paths)
        files = self.get_check_file_list()
        for file in files:
            logging.info(f"run {file}")
            if self.is_aborted:
                continue
            self.run_file_function(file)

        if self.is_aborted:
            self.signaller.finished.emit(ABORT)
            return

        self.signaller.finished.emit(self.ifc_paths)
        self.signaller.status.emit(f"{self.function_name} Abgeschlossen!")

    def run_file_function(self, file_path) -> ifcopenshell.file:
        """imports the Ifc-File"""
        self.base_name = os.path.basename(file_path)
        self.signaller.status.emit(f"Import {self.base_name}")
        self.signaller.progress.emit(0)
        sleep(0.1)

        ifc = ifcopenshell.open(file_path)
        self.signaller.status.emit(f"Import Done!")
        sleep(0.1)
        return ifc


class Signaller(QObject):
    started = Signal(str)
    finished = Signal(str)
    progress = Signal(int)
    status = Signal(str)


def ifc_file_dialog(window: QWidget, line_edit: QLineEdit) -> None | list:
    file_text = "IFC Files (*.ifc *.IFC);;"
    ifc_paths = settings.get_ifc_path()
    if isinstance(ifc_paths, list):
        ifc_paths = ifc_paths[0]
    path = QFileDialog.getOpenFileNames(window, "IFC-Files", ifc_paths, file_text)[0]
    if not path:
        return
    settings.set_ifc_path(path)
    line_edit.setText(settings.PATH_SEPERATOR.join(path))
    return path


def get_ifc_path(line_edit_ifc: QLineEdit) -> list[str]:
    paths = line_edit_ifc.text().split(settings.PATH_SEPERATOR)
    result = list()
    for path in paths:
        if not os.path.exists(path):
            logging.error(f"IFC-File does not exist: '{path}'")
        else:
            result.append(path)
    return result


def get_main_attribute(proj: classes.Project) -> (str, str):
    ident_attributes = dict()
    ident_psets = dict()
    for obj in proj.objects:
        if obj.ident_attrib is None:
            continue
        ident_pset = obj.ident_attrib.property_set.name
        ident_attribute = obj.ident_attrib.name
        if ident_pset not in ident_psets:
            ident_psets[ident_pset] = 0
        if ident_attribute not in ident_attributes:
            ident_attributes[ident_attribute] = 0
        ident_psets[ident_pset] += 1
        ident_attributes[ident_attribute] += 1

    ident_attribute = (sorted(ident_attributes.items(), key=lambda x: x[1]))
    ident_pset = (sorted(ident_psets.items(), key=lambda x: x[1]))
    if ident_attribute and ident_pset:
        return ident_pset[0][0], ident_attribute[0][0]
    else:
        return "", ""


def set_main_attribute(proj: classes.Project, line_edit_pset: QLineEdit, line_edit_attribute: QLineEdit) -> None:
    pset, attribute = proj.get_main_attribute()
    line_edit_pset.setText(pset)
    line_edit_attribute.setText(attribute)


def auto_set_ifc_path(line_edit_ifc: QLineEdit):
    ifc_path = settings.get_ifc_path()
    if ifc_path:
        if isinstance(ifc_path, list):
            ifc_path = settings.PATH_SEPERATOR.join(ifc_path)
        line_edit_ifc.setText(ifc_path)


def check_for_ifc(line_edit_ifc: QLineEdit, label_ifc_missing: QLabel):
    if not get_ifc_path(line_edit_ifc):
        if line_edit_ifc.text():
            label_ifc_missing.setText("Path doesn't exist!")
        else:
            label_ifc_missing.setText("IFC File Path is missing!")
        label_ifc_missing.show()
        return False
    return True


def check_for_export_path(export_path: str, label_export_missing: QLabel):
    allow = True
    if not export_path:
        label_export_missing.setText("Export Path is missing!")
        label_export_missing.show()
        allow = False

    elif not os.path.exists(os.path.dirname(export_path)):
        label_export_missing.setText("Path doesn't exist!")
        label_export_missing.show()
        allow = False
    return allow
