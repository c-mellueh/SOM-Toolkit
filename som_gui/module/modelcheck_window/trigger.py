from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import tool
from som_gui.core import modelcheck_window as core
from som_gui.core import modelcheck as mc_core
from som_gui.core import modelcheck_results as mc_results_core
if TYPE_CHECKING:
    from .ui import ModelcheckWindow
    from PySide6.QtWidgets import QTreeView
    from PySide6.QtGui import QStandardItemModel
    from som_gui.module.ifc_importer.ui import IfcImportWidget


def connect():
    tool.MainWindow.add_action("Modelcheck/Interne Modellprüfung",
                               lambda: core.open_window(tool.ModelcheckWindow, tool.IfcImporter))


def paint_object_tree():
    core.paint_object_tree(tool.ModelcheckWindow, tool.Project)


def paint_pset_tree():
    core.paint_pset_tree(tool.ModelcheckWindow)


def connect_ifc_import_widget(widget: IfcImportWidget):
    widget.widget.button_export.clicked.connect(
        lambda: core.export_selection_clicked(widget, tool.ModelcheckWindow, tool.Settings))
    widget.widget.button_run.clicked.connect(
        lambda: core.run_clicked(widget, tool.ModelcheckWindow, tool.Modelcheck, tool.ModelcheckResults,
                                 tool.IfcImporter, tool.Project,
                                 mc_core, mc_results_core))


def connect_object_check_tree(widget: QTreeView):
    model: QStandardItemModel = widget.model()
    model.itemChanged.connect(lambda item: core.object_check_changed(item, tool.ModelcheckWindow))
    widget.selectionModel().selectionChanged.connect(
        lambda item: core.object_selection_changed(widget.selectionModel(), tool.ModelcheckWindow))


def connect_pset_check_tree(widget: QTreeView):
    model: QStandardItemModel = widget.model()
    model.itemChanged.connect(lambda item: core.object_check_changed(item, tool.ModelcheckWindow))


def connect_window(widget: ModelcheckWindow):
    pass


def on_new_project():
    pass
