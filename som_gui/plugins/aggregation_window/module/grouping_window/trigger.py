import ifcopenshell
from PySide6.QtWidgets import QPushButton

from som_gui import tool
from ... import tool as aw_tool
from ...core import grouping_window as core


def connect():
    core.create_main_menu_actions(aw_tool.GroupingWindow, tool.MainWindow)


def open_window():
    core.open_window(aw_tool.GroupingWindow, tool.Util)


def connect_ifc_import_runner(runner):
    runner.signaller.started.connect(lambda: core.ifc_import_started(runner, aw_tool.GroupingWindow))
    runner.signaller.finished.connect(lambda: core.ifc_import_finished(runner, aw_tool.GroupingWindow))


def button_clicked(button: QPushButton):
    bb = aw_tool.GroupingWindow.get().ui.buttonBox
    if button == bb.button(bb.StandardButton.Apply):
        core.run_clicked(aw_tool.GroupingWindow, tool.IfcImporter, tool.Util)
    if button == bb.button(bb.StandardButton.Cancel):
        core.cancel_clicked(aw_tool.GroupingWindow)
    if button == bb.button(bb.StandardButton.Abort):
        core.abort_clicked(aw_tool.GroupingWindow, tool.IfcImporter)


def start_grouping(ifc_file: ifcopenshell.file):
    core.create_groups_in_file(ifc_file, aw_tool.GroupingWindow, tool.Project)


def connect_grouping_runner(runner):
    runner.signaller.finished.connect(
        lambda: core.grouping_finished(aw_tool.GroupingWindow, tool.Popups))
    runner.signaller.status.connect(aw_tool.GroupingWindow.set_status)
    runner.signaller.progress.connect(aw_tool.GroupingWindow.set_progress)


def on_new_project():
    pass


def retranslate_ui():
    core.retranslate_ui(aw_tool.GroupingWindow, tool.Util)
