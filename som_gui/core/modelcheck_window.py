from __future__ import annotations

import logging
import os
import time
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialogButtonBox

import SOMcreator
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.tool.modelcheck import ModelcheckRunner

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtGui import QStandardItem, QStandardItemModel
    from PySide6.QtCore import QItemSelectionModel, QModelIndex
    from som_gui.tool.ifc_importer import IfcImportRunner
    from som_gui.module.modelcheck_window import ui


def create_main_menu_actions(
    modelcheck_window: Type[tool.ModelcheckWindow], main_window: Type[tool.MainWindow]
):
    from som_gui.module.modelcheck_window import trigger

    open_window_action = main_window.add_action(
        "menuModels", "modelcheck", trigger.open_window
    )
    modelcheck_window.set_action("open_window", open_window_action)


def open_window(
    modelcheck_window: Type[tool.ModelcheckWindow],
    util: Type[tool.Util],
    project: Type[tool.Project],
):
    proj = project.get()
    window = modelcheck_window.create_window()
    main_pset_name, main_attribute_name = proj.get_main_property()
    util.fill_main_attribute(
        window.ui.main_attribute_widget, main_pset_name, main_attribute_name
    )

    util.fill_file_selector(
        window.ui.widget_import,
        "IfcPath",
        "IFC Files (*.ifc *.IFC);;",
        "modelcheck_files",
    )
    util.fill_file_selector(
        window.ui.widget_export,
        "ExportPfad",
        "Excel File (*.xlsx);;",
        "modelcheck_export",
        request_save=True,
    )
    modelcheck_window.connect_buttons()
    modelcheck_window.clear_progress_bars()
    modelcheck_window.set_progress_bar_layout_visible(False)
    modelcheck_window.reset_butons()
    retranslate_ui(modelcheck_window, util)
    window.show()


def retranslate_ui(
    modelcheck_window: Type[tool.ModelcheckWindow], util: Type[tool.Util]
):
    action = modelcheck_window.get_action("open_window")
    modelcheck_title = QCoreApplication.translate("Modelcheck", "Modelcheck")
    action.setText(modelcheck_title)
    window = modelcheck_window.get_window()

    if not window:
        return
    window.ui.retranslateUi(window)
    window.ui.widget_export.name = QCoreApplication.translate(
        "Modelcheck", "Export Path"
    )
    window.ui.widget_import.name = QCoreApplication.translate("Modelcheck", "IFC Path")
    title = util.get_window_title(modelcheck_title)
    window.setWindowTitle(title)

    object_model: QStandardItemModel = modelcheck_window.get_object_tree().model()
    headers = [
        QCoreApplication.translate("Modelcheck", "Object"),
        QCoreApplication.translate("Modelcheck", "Identifier"),
    ]
    object_model.setHorizontalHeaderLabels(headers)

    pset_model: QStandardItemModel = modelcheck_window.get_pset_tree().model()
    headers = [QCoreApplication.translate("Modelcheck", "PropertySet,Attribute")]
    pset_model.setHorizontalHeaderLabels(headers)


def close_window(modelcheck_window: Type[tool.ModelcheckWindow]):
    modelcheck_window.close_window()


def abort_clicked(
    modelcheck_window: Type[tool.ModelcheckWindow],
    modelcheck: Type[tool.Modelcheck],
    ifc_importer: Type[tool.IfcImporter],
):

    import_pool = ifc_importer.get_threadpool()
    check_pool = modelcheck_window.get_modelcheck_threadpool()
    logging.debug(
        f"Cancel clicked. Active threads: {import_pool.activeThreadCount()}|{check_pool.activeThreadCount()}"
    )

    if ifc_importer.import_is_running():
        for runner in modelcheck_window.get_properties().ifc_import_runners:
            runner.is_aborted = True
    if modelcheck_window.modelcheck_is_running() or ifc_importer.import_is_running():
        modelcheck_window.set_progress_bar_layout_visible(False)
        modelcheck_window.clear_progress_bars()
        modelcheck.abort()
        modelcheck_window.reset_butons()


def run_modelcheck(
    modelcheck_window: Type[tool.ModelcheckWindow],
    modelcheck: Type[tool.Modelcheck],
    modelcheck_results: Type[tool.ModelcheckResults],
    ifc_importer: Type[tool.IfcImporter],
    project: Type[tool.Project],
    util: Type[tool.Util],
):
    ifc_paths, export_path, main_pset, main_attribute = modelcheck_window.read_inputs()
    inputs_are_valid = ifc_importer.check_inputs(ifc_paths, main_pset, main_attribute)
    export_path_is_valid = modelcheck_window.check_export_path(export_path)

    if not inputs_are_valid or not export_path_is_valid:
        return

    modelcheck_window.set_progress_bar_layout_visible(True)
    modelcheck_window.show_buttons(QDialogButtonBox.StandardButton.Abort)
    modelcheck.reset_abort()
    modelcheck.set_main_pset_name(main_pset)
    modelcheck.set_main_attribute_name(main_attribute)
    modelcheck_results.set_export_path(export_path)

    pool = ifc_importer.get_threadpool()
    pool.setMaxThreadCount(3)
    modelcheck.init_sql_database(util.create_tempfile(".db"))
    modelcheck.reset_guids()
    modelcheck.build_ident_dict(set(project.get().get_classes(filter=True)))

    for path in ifc_paths:
        progress_bar = util.create_progressbar()
        modelcheck_window.add_progress_bar(progress_bar)
        runner = modelcheck_window.create_import_runner(progress_bar, path)
        modelcheck_window.connect_ifc_import_runner(runner)

        status = QCoreApplication.translate("Modelcheck", "Import '{}'").format(
            os.path.basename(path)
        )
        modelcheck_window.set_status(runner, status)
        modelcheck_window.set_progress(runner, 0)
        pool.start(runner)


def ifc_import_started(
    runner: IfcImportRunner,
    modelcheck_window: Type[tool.ModelcheckWindow],
    ifc_importer: Type[tool.IfcImporter],
):
    logging.debug(f"IFC Runner '{runner.path}' started.")
    modelcheck_window.set_progressbar_visible(runner, True)

    status = QCoreApplication.translate("Modelcheck", "Import '{}'").format(
        os.path.basename(runner.path)
    )
    ifc_importer.set_status(runner, status)
    ifc_importer.set_progress(runner, 0)


def ifc_import_finished(
    runner: IfcImportRunner,
    modelcheck_window: Type[tool.ModelcheckWindow],
    modelcheck: Type[tool.Modelcheck],
    ifc_importer: Type[tool.IfcImporter],
):
    """
    creates and runs Modelcheck Runnable
    """
    logging.debug(f"IFC Runner '{runner.path}' finished.")
    modelcheck_window.destroy_import_runner(runner)
    ifc_importer.set_status(
        runner,
        QCoreApplication.translate("Modelcheck", "Import of '{}' Done!").format(
            runner.path
        ),
    )
    modelcheck.set_ifc_name(os.path.basename(runner.path))

    logging.debug(f"Create Modelcheck Runner '{runner.path}'")
    modelcheck_runner = modelcheck.create_modelcheck_runner(runner)
    modelcheck_window.connect_modelcheck_runner(modelcheck_runner)

    logging.debug(
        f"Start Threadpool for Modelcheck Runner '{modelcheck_runner.file.wrapped_data}'"
    )
    modelcheck_window.get_modelcheck_threadpool().start(modelcheck_runner)


def modelcheck_finished(
    modelcheck_runner: ModelcheckRunner,
    modelcheck_window: Type[tool.ModelcheckWindow],
    modelcheck: Type[tool.Modelcheck],
    modelcheck_results: Type[tool.ModelcheckResults],
    ifc_importer: Type[tool.IfcImporter],
):

    if modelcheck.is_aborted():
        logging.debug(f"Modelcheck '{modelcheck_runner.path}' aborted.")
        modelcheck_window.reset_butons()
        return
    else:
        logging.debug(f"Modelcheck '{modelcheck_runner.path}' done.")

    time.sleep(0.2)
    if modelcheck_window.modelcheck_is_running():
        logging.debug(f"Modelchecks are still running")
    if ifc_importer.import_is_running():
        logging.debug(f"Imports are still running")

    if modelcheck_window.modelcheck_is_running() or ifc_importer.import_is_running():
        logging.debug(f"Check next File")

    else:
        logging.debug(f"Finish Modelcheck")
        modelcheck_results.last_modelcheck_finished()
        modelcheck_window.reset_butons()


def paint_object_tree(
    tree: ui.ObjectTree,
    modelcheck_window: Type[tool.ModelcheckWindow],
    project: Type[tool.Project],
):
    logging.debug(f"Repaint Modelcheck Object Tree")
    root_objects = set(project.get_root_objects(True))
    invisible_root_entity = tree.model().invisibleRootItem()
    modelcheck_window.fill_object_tree(
        root_objects, invisible_root_entity, tree.model(), tree
    )
    if modelcheck_window.is_initial_paint:
        modelcheck_window.resize_object_tree(tree)


def object_check_changed(
    item: QStandardItem, modelcheck_window: Type[tool.ModelcheckWindow]
):
    obj = item.data(CLASS_REFERENCE)
    if item.column() != 0:
        return

    modelcheck_window.set_item_check_state(obj, item.checkState())

    paint_pset_tree(modelcheck_window)


def object_selection_changed(
    selection_model: QItemSelectionModel, modelcheck_window: Type[tool.ModelcheckWindow]
):
    logging.debug(f"ObjectSelectionChanged: {selection_model.selectedIndexes()}")
    selected_indexes = selection_model.selectedIndexes()
    if not selected_indexes:
        return
    index: QModelIndex = selected_indexes[0]
    obj: SOMcreator.SOMClass = index.data(CLASS_REFERENCE)
    modelcheck_window.set_selected_object(obj)
    paint_pset_tree(modelcheck_window)
    if obj.ident_value:
        text = f"{obj.name} [{obj.ident_value}]"
    else:
        text = obj.name
    modelcheck_window.set_pset_tree_title(text)
    modelcheck_window.show_pset_tree_title(True)


def paint_pset_tree(modelcheck_window: Type[tool.ModelcheckWindow]):
    logging.debug(f"Repaint Modelcheck Pset Tree")
    obj = modelcheck_window.get_selected_object()
    if obj is None:
        return
    cs = modelcheck_window.get_item_check_state(obj)
    enabled = True if cs == Qt.CheckState.Checked else False
    modelcheck_window.fill_pset_tree(
        set(obj.get_property_sets(filter=True)),
        enabled,
        modelcheck_window.get_pset_tree(),
    )


def object_tree_context_menu_requested(
    pos, widget, modelcheck_window: Type[tool.ModelcheckWindow]
):
    actions = [
        [
            QCoreApplication.translate("Modelcheck", "Extend"),
            lambda: modelcheck_window.expand_selection(widget),
        ],
        [
            QCoreApplication.translate("Modelcheck", "Collapse"),
            lambda: modelcheck_window.collapse_selection(widget),
        ],
        [
            QCoreApplication.translate("Modelcheck", "Activate"),
            lambda: modelcheck_window.check_selection(widget),
        ],
        [
            QCoreApplication.translate("Modelcheck", "Deactivate"),
            lambda: modelcheck_window.uncheck_selection(widget),
        ],
    ]

    modelcheck_window.create_context_menu(pos, actions, widget)


def connect_object_tree(
    tree: ui.ObjectTree, modelcheck_window: Type[tool.ModelcheckWindow]
):
    modelcheck_window.connect_object_tree(tree)


def connect_pset_tree(
    tree: ui.PsetTree, modelcheck_window: Type[tool.ModelcheckWindow]
):
    modelcheck_window.connect_pset_tree(tree)
