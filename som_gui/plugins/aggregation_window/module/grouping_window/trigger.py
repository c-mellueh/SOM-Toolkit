from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton

from som_gui import tool

from ... import tool as aw_tool
from ...core import grouping_window as core

if TYPE_CHECKING:
    from ...tool.grouping_window import GroupingRunner
    from som_gui.tool.ifc_importer import IfcImportRunner


def activate():
    core.create_main_menu_actions(aw_tool.GroupingWindow, tool.MainWindow)


def deactivate():
    core.remove_main_menu_actions(aw_tool.GroupingWindow, tool.MainWindow)


def open_window():
    core.open_window(aw_tool.GroupingWindow, tool.Util)


def connect_ifc_import_runner(runner: IfcImportRunner):
    runner.signaller.started.connect(lambda: core.ifc_import_started(runner))
    runner.signaller.finished.connect(
        lambda: core.ifc_import_finished(runner, aw_tool.GroupingWindow)
    )
    runner.signaller.status.connect(
        lambda s: aw_tool.GroupingWindow.set_status(runner.progress_bar, s)
    )
    runner.signaller.progress.connect(
        lambda p: aw_tool.GroupingWindow.set_progress(runner.progress_bar, p)
    )


def button_clicked(button: QPushButton):
    bb = aw_tool.GroupingWindow.get().ui.buttonBox
    if button == bb.button(bb.StandardButton.Apply):
        core.run_clicked(aw_tool.GroupingWindow, tool.IfcImporter, tool.Util)
    if button == bb.button(bb.StandardButton.Cancel):
        core.close_window(aw_tool.GroupingWindow)
    if button == bb.button(bb.StandardButton.Abort):
        core.abort_clicked(aw_tool.GroupingWindow, tool.IfcImporter)


def start_grouping(runner: GroupingRunner):
    core.create_groups_in_file(runner, aw_tool.GroupingWindow, tool.Project)


def connect_grouping_runner(runner: GroupingRunner):
    runner.signaller.finished.connect(
        lambda: core.grouping_finished(
            runner, aw_tool.GroupingWindow, tool.IfcImporter, tool.Popups
        )
    )
    runner.signaller.status.connect(
        lambda s: aw_tool.GroupingWindow.set_status(runner.progress_bar, s)
    )
    runner.signaller.progress.connect(
        lambda p: aw_tool.GroupingWindow.set_progress(runner.progress_bar, p)
    )


def on_new_project():
    pass


def retranslate_ui():
    core.retranslate_ui(aw_tool.GroupingWindow, tool.Util)
