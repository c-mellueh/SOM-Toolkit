from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import tool
from som_gui.core import modelcheck_window as core
import logging
from PySide6.QtWidgets import QTreeView, QPushButton, QDialogButtonBox


if TYPE_CHECKING:
    from .ui import ModelcheckWindow
    from PySide6.QtCore import QRunnable

    from PySide6.QtGui import QStandardItemModel
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from som_gui.tool.modelcheck import ModelcheckRunner

def connect():
    tool.MainWindow.add_action("Modelle/Modellprüfung",
                               lambda: core.open_window(tool.ModelcheckWindow, tool.Util, tool.Project))


def paint_object_tree():
    core.paint_object_tree(tool.ModelcheckWindow, tool.Project)


def paint_pset_tree():
    core.paint_pset_tree(tool.ModelcheckWindow)


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


def connect_object_check_tree(widget: QTreeView):
    model: QStandardItemModel = widget.model()
    model.itemChanged.connect(lambda item: core.object_check_changed(item, tool.ModelcheckWindow))
    widget.selectionModel().selectionChanged.connect(
        lambda item: core.object_selection_changed(widget.selectionModel(), tool.ModelcheckWindow))
    widget.customContextMenuRequested.connect(
        lambda pos: core.object_tree_conect_menu_requested(pos, widget, tool.ModelcheckWindow))


def connect_pset_check_tree(widget: QTreeView):
    model: QStandardItemModel = widget.model()
    model.itemChanged.connect(lambda item: core.object_check_changed(item, tool.ModelcheckWindow))
    widget.customContextMenuRequested.connect(
        lambda pos: core.object_tree_conect_menu_requested(pos, widget, tool.ModelcheckWindow))

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
