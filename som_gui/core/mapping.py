from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication

import SOMcreator
from SOMcreator.exporter import revit

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QTreeWidgetItem


def create_main_menu_actions(mapping: Type[tool.Mapping], main_window: Type[tool.MainWindow]):
    from som_gui.module.mapping import trigger
    open_window_action = main_window.add_action("menuExport", "Mapping", trigger.open_window)
    mapping.set_action("open_window", open_window_action)


def retranslate_ui(mapping: Type[tool.Mapping], util: Type[tool.Util]):
    open_window_action = mapping.get_action("open_window")
    open_window_action.setText(QCoreApplication.translate("Mapping", "Revit-Mapping"))
    window = mapping.get_window()
    if window:
        window.ui.retranslateUi(window)
        title = util.get_window_title(QCoreApplication.translate("Mapping", "Revit-Mapping"))
        window.setWindowTitle(title)


def open_window(mapping: Type[tool.Mapping]):
    if window := mapping.get_window() is None:
        window = mapping.create_window()
    from som_gui.module.mapping import trigger
    trigger.retranslate_ui()
    mapping.connect_window_triggers(window)
    window.show()


def export_revit_ifc_mapping(mapping: Type[tool.Mapping], project: Type[tool.Project], popups: Type[tool.Popups]):
    path = popups.get_save_path("txt Files (*.txt);;", mapping.get_window())
    if not path:
        return

    export_dict = mapping.create_export_dict(list(project.get().get_root_objects(filter=False)))
    revit.export_ifc_template(path, export_dict)


def export_revit_shared_parameters(mapping: Type[tool.Mapping], project: Type[tool.Project], popups: Type[tool.Popups]):
    path = popups.get_save_path("txt Files (*.txt);;", mapping.get_window())
    if not path:
        return
    export_dict = mapping.create_export_dict(project.get_root_objects())
    revit.export_shared_parameters(path, export_dict)


def update_object_tree(mapping: Type[tool.Mapping], project: Type[tool.Project]):
    logging.debug(f"Update ObjectTree")
    root_objects = project.get_root_objects(filter_objects=False)
    mapping.fill_object_tree(root_objects)


def update_pset_tree(mapping: Type[tool.Mapping]):
    logging.debug("Update Pset Tree")
    selected_object = mapping.get_selected_object()

    if selected_object is None:
        property_sets = set()
    else:
        property_sets = set(selected_object.get_property_sets(filter=True))

    enable_state = True if mapping.get_checkstate(selected_object) and property_sets else False
    tree = mapping.get_pset_tree()
    if enable_state != tree.isEnabled():
        tree.setEnabled(enable_state)

    mapping.update_tree(property_sets, tree.invisibleRootItem(), tree)


def tree_item_changed(item: QTreeWidgetItem, mapping: Type[tool.Mapping], util: Type[tool.Util]):
    logging.debug(f"Tree Item Changed {item}")
    entity = mapping.get_entity_from_item(item)
    cs = util.checkstate_to_bool(item.checkState(0))
    mapping.set_checkstate(entity, cs)
    if isinstance(entity, SOMcreator.Object):
        update_pset_tree(mapping)
        mapping.disable_all_child_entities(item, not cs)
    if isinstance(entity, SOMcreator.PropertySet):
        mapping.disable_all_child_entities(item, not cs)
