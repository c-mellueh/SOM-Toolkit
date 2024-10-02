from som_gui import tool
from ... import tool as aw_tool
from ...core import grouping_window as core
from PySide6.QtWidgets import QPushButton
import ifcopenshell


def connect():
    tool.MainWindow.add_action("Modelle/Gruppen Generieren",
                               lambda: core.open_window(aw_tool.GroupingWindow, tool.IfcImporter))


def connect_ifc_import_runner(runner):
    runner.signaller.started.connect(lambda: core.ifc_import_started(runner, aw_tool.GroupingWindow, tool.IfcImporter))
    runner.signaller.finished.connect(lambda: core.ifc_import_finished(runner, aw_tool.GroupingWindow))


def connect_buttons(run_button: QPushButton, abort_button: QPushButton):
    run_button.clicked.connect(lambda: core.run_clicked(aw_tool.GroupingWindow, tool.IfcImporter))
    abort_button.clicked.connect(lambda: core.cancel_clicked(aw_tool.GroupingWindow, tool.IfcImporter))


def start_grouping(ifc_file: ifcopenshell.file):
    core.create_groups_in_file(ifc_file, aw_tool.GroupingWindow, tool.Project)


def connect_grouping_runner(runner):
    runner.signaller.finished.connect(
        lambda: core.grouping_finished(aw_tool.GroupingWindow, tool.IfcImporter, tool.Popups))
    runner.signaller.status.connect(aw_tool.GroupingWindow.set_status)
    runner.signaller.progress.connect(aw_tool.GroupingWindow.set_progress)


def on_new_project():
    pass
