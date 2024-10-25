from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QTreeView

from som_gui import tool
from som_gui.core import modelcheck_window as core

if TYPE_CHECKING:
    from .ui import ModelcheckWindow, ObjectTree, PsetTree
    from PySide6.QtCore import QRunnable, QItemSelectionModel, QPoint

    from PySide6.QtGui import QStandardItem
    from som_gui.tool.modelcheck import ModelcheckRunner


def connect():
    core.create_main_menu_actions(tool.ModelcheckWindow, tool.MainWindow)


def open_window():
    core.open_window(tool.ModelcheckWindow, tool.Util, tool.Project)


def paint_object_tree(tree):
    core.paint_object_tree(tree, tool.ModelcheckWindow, tool.Project)


def paint_pset_tree(tree):
    core.paint_pset_tree(tree, tool.ModelcheckWindow)


def button_box_clicked(button: QPushButton):
    logging.debug(f"button_box_clicked: {button}")
    bb = tool.ModelcheckWindow.get_window().ui.buttonBox
    if button == bb.button(bb.StandardButton.Apply):
        core.run_clicked(tool.ModelcheckWindow, tool.Modelcheck, tool.ModelcheckResults,
                         tool.IfcImporter, tool.Project, tool.Util)
    if button == bb.button(bb.StandardButton.Cancel):
        core.cancel_clicked(tool.ModelcheckWindow)

    if button == bb.button(bb.StandardButton.Abort):
        core.abort_clicked(tool.ModelcheckWindow, tool.Modelcheck, tool.IfcImporter)


def connect_object_check_tree(widget: ObjectTree):
    core.connect_object_tree(widget, tool.ModelcheckWindow)


def object_checkstate_changed(item: QStandardItem):
    core.object_check_changed(item, tool.ModelcheckWindow)


def object_selection_changed(selection_model: QItemSelectionModel):
    core.object_selection_changed(selection_model, tool.ModelcheckWindow)


def object_tree_context_menu_requested(pos: QPoint, tree_widget: ObjectTree):
    core.object_tree_context_menu_requested(pos, tree_widget, tool.ModelcheckWindow)


def connect_pset_check_tree(widget: QTreeView):
    core.connect_pset_tree(widget, tool.ModelcheckWindow)


def pset_checkstate_changed(item: QStandardItem):
    core.object_check_changed(item, tool.ModelcheckWindow)


def pset_context_menu_requested(pos, widget: PsetTree):
    core.object_tree_context_menu_requested(pos, widget, tool.ModelcheckWindow)


def connect_modelcheck_runner(runner: ModelcheckRunner):
    runner.signaller.finished.connect(
        lambda: core.modelcheck_finished(tool.ModelcheckWindow, tool.Modelcheck, tool.ModelcheckResults))
    runner.signaller.status.connect(tool.ModelcheckWindow.set_status)
    runner.signaller.progress.connect(tool.ModelcheckWindow.set_progress)


def connect_ifc_import_runner(runner: QRunnable):
    runner.signaller.started.connect(lambda: core.ifc_import_started(runner, tool.ModelcheckWindow))
    runner.signaller.finished.connect(lambda: core.ifc_import_finished(runner, tool.ModelcheckWindow, tool.Modelcheck))


def on_new_project():
    pass


def retranslate_ui():
    core.retranslate_ui(tool.ModelcheckWindow, tool.Util)
