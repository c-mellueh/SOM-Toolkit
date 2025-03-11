from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton, QTreeView

from som_gui import tool
from som_gui.core import modelcheck_window as core

if TYPE_CHECKING:
    from .ui import ModelcheckWindow, ClassTree, PsetTree
    from PySide6.QtCore import QRunnable, QItemSelectionModel, QPoint

    from PySide6.QtGui import QStandardItem
    from som_gui.tool.modelcheck import ModelcheckRunner
    from som_gui.tool.ifc_importer import IfcImportRunner


def connect():
    core.create_main_menu_actions(tool.ModelcheckWindow, tool.MainWindow)


def open_window():
    core.open_window(tool.ModelcheckWindow, tool.Util, tool.Project)


def paint_object_tree(tree):
    core.paint_class_tree(tree, tool.ModelcheckWindow, tool.Project)


def paint_pset_tree(tree):
    core.paint_pset_tree(tool.ModelcheckWindow)


def button_box_clicked(button: QPushButton):
    bb = tool.ModelcheckWindow.get_window().ui.buttonBox
    if button == bb.button(bb.StandardButton.Apply):
        logging.debug(f"Run Clicked")
        core.run_modelcheck(
            tool.ModelcheckWindow,
            tool.Modelcheck,
            tool.ModelcheckResults,
            tool.IfcImporter,
            tool.Project,
            tool.Util,
        )
    if button == bb.button(bb.StandardButton.Cancel):
        logging.debug("Cancel Clicked")
        core.close_window(tool.ModelcheckWindow)

    if button == bb.button(bb.StandardButton.Abort):
        core.abort_clicked(tool.ModelcheckWindow, tool.Modelcheck, tool.IfcImporter)


def connect_object_check_tree(widget: ClassTree):
    core.connect_class_tree(widget, tool.ModelcheckWindow)


def object_checkstate_changed(item: QStandardItem):
    core.class_check_changed(item, tool.ModelcheckWindow)


def object_selection_changed(selection_model: QItemSelectionModel):
    core.class_selection_changed(selection_model, tool.ModelcheckWindow)


def object_tree_context_menu_requested(pos: QPoint, tree_widget: ClassTree):
    core.class_tree_context_menu_requested(pos, tree_widget, tool.ModelcheckWindow)


def connect_pset_check_tree(widget: QTreeView):
    core.connect_pset_tree(widget, tool.ModelcheckWindow)


def pset_checkstate_changed(item: QStandardItem):
    core.class_check_changed(item, tool.ModelcheckWindow)


def pset_context_menu_requested(pos, widget: PsetTree):
    core.class_tree_context_menu_requested(pos, widget, tool.ModelcheckWindow)


def connect_modelcheck_runner(runner: ModelcheckRunner):
    runner.signaller.finished.connect(
        lambda: core.modelcheck_finished(
            runner,
            tool.ModelcheckWindow,
            tool.Modelcheck,
            tool.ModelcheckResults,
            tool.IfcImporter,
        )
    )
    runner.signaller.status.connect(
        lambda s: tool.Util.set_status(runner.progress_bar, s)
    )
    runner.signaller.progress.connect(
        lambda p: tool.Util.set_progress(runner.progress_bar, p)
    )


def connect_ifc_import_runner(runner: IfcImportRunner):
    runner.signaller.started.connect(
        lambda: core.ifc_import_started(runner, tool.ModelcheckWindow, tool.IfcImporter)
    )
    runner.signaller.finished.connect(
        lambda: core.ifc_import_finished(
            runner, tool.ModelcheckWindow, tool.Modelcheck, tool.IfcImporter
        )
    )
    runner.signaller.status.connect(
        lambda s: tool.Util.set_status(runner.progress_bar, s)
    )
    runner.signaller.progress.connect(
        lambda p: tool.Util.set_progress(runner.progress_bar, p)
    )


def on_new_project():
    pass


def retranslate_ui():
    core.retranslate_ui(tool.ModelcheckWindow, tool.Util)
