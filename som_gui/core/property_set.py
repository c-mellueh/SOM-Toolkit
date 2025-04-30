from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from som_gui.core import property_table as property_table_core

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QModelIndex, Qt, QCoreApplication


def add_property_set_button_pressed(
    main_window_tool: Type[tool.MainWindow],
    property_set_tool: Type[tool.PropertySet],
    popup_tool: Type[tool.Popups],
    predefined_psets: Type[tool.PredefinedPropertySet],
    ifc_schema: Type[tool.IfcSchema],
    util: Type[tool.Util],
    popups: Type[tool.Popups],
):
    logging.debug(f"Add PropertySet button clicked")
    title = QCoreApplication.translate("PropertySet", "Add PropertySet")
    name = QCoreApplication.translate("PropertySet", "PropertySet name?")
    pset_existist_error = QCoreApplication.translate(
        f"PropertySet", "PropertySet '{}' exists allready"
    )
    som_class = main_window_tool.get_active_class()
    newest_version = ifc_schema.get_newest_version(ifc_schema.get_active_versions())
    pset_names = property_set_tool.get_pset_name_suggestion(
        som_class,
        predefined_psets.get_property_sets(),
        [newest_version],
    )

    completer = util.create_completer(pset_names)

    new_name = popup_tool._request_text_input(
        title, name, prefill="", parent=main_window_tool.get(), completer=completer
    )
    if not new_name:
        return

    if property_set_tool.is_pset_existing(new_name, som_class):
        popup_tool.create_warning_popup(pset_existist_error.format(new_name))
        return

    # Handle Inheritance
    parent_pset = None
    if predefined_psets.name_is_in_predefined_psets(new_name):
        connect_result = popups.request_property_set_merge(new_name, 1)
        if connect_result:
            parent_pset = predefined_psets.get_pset_by_name(new_name)

    elif property_set_tool.is_name_in_parent_classes(new_name, som_class):
        connect_result = popups.request_property_set_merge(new_name, 2)
        if connect_result:
            parent_pset = property_set_tool.get_parent_by_name(new_name, som_class)

    elif property_set_tool.is_name_in_ifc_psets(new_name, som_class, newest_version):
        connect_result = popups.request_property_set_merge(new_name, 3)
        if connect_result:
            new_pset = property_set_tool.create_ifc_pset(new_name, newest_version)
            som_class.add_property_set(new_pset)
            repaint_pset_table(property_set_tool, main_window_tool)
            return
    property_set_tool.create_property_set(new_name, som_class, parent_pset)

    repaint_pset_table(property_set_tool, main_window_tool)


def pset_clicked(item: QTableWidgetItem, property_set: Type[tool.PropertySet]):
    pset = property_set.get_pset_from_item(item)
    if not item.column() == 2:
        return
    cs = True if item.checkState() == Qt.CheckState.Checked else False
    pset.set_optional(cs)


def pset_selection_changed(
    property_set_tool: Type[tool.PropertySet],
    property_table: Type[tool.PropertyTable],
    main_window: Type[tool.MainWindow],
):

    property_set = property_set_tool.get_selecte_property_set_from_table()
    property_set_tool.set_active_property_set(property_set)
    property_table.set_property_set_of_table(
        main_window.get_property_table(), property_set
    )
    property_table_core.update_table(main_window.get_property_table(), property_table)
    text = "" if not property_set else property_set.name

    main_window.get_pset_name_label().setText(text)


def pset_table_context_menu(
    pos, property_set_tool: Type[tool.PropertySet], class_tool: Type[tool.Class]
):

    table = property_set_tool.get_table()
    if not table.itemAt(pos):
        return
    pset = property_set_tool.get_pset_from_item(table.itemAt(pos))
    if pset.is_child:

        actions = [
            [
                QCoreApplication.translate(f"PropertySet", "Delete"),
                property_set_tool.delete_table_pset,
            ],
        ]
    else:

        actions = [
            [
                QCoreApplication.translate(f"PropertySet", "Rename"),
                property_set_tool.rename_table_pset,
            ],
            [
                QCoreApplication.translate(f"PropertySet", "Delete"),
                property_set_tool.delete_table_pset,
            ],
        ]

    def inherit_to_child():
        pset = property_set_tool.get_active_property_set()
        som_class = pset.som_class
        if not som_class:
            return
        class_tool.inherit_property_set_to_all_children(som_class, pset)

    actions.append(
        [
            QCoreApplication.translate(f"PropertySet", "Inherit to child classes"),
            inherit_to_child,
        ]
    )

    property_set_tool.create_context_menu(table.mapToGlobal(pos), actions)


def pset_table_edit_started(property_set: Type[tool.PropertySet]):
    pset = property_set.get_selecte_property_set_from_table()
    table = property_set.get_table()
    for row in range(table.rowCount()):
        if property_set.get_property_set_from_row(row, table) == pset:
            property_set.set_pset_name_by_row(pset, row, table)

    props = property_set.get_properties()
    props.is_renaming_property_set = True


def pset_table_edit_stopped(property_set_tool: Type[tool.PropertySet]):
    props = property_set_tool.get_properties()
    props.is_renaming_property_set = False


def rename_pset_by_editor(
    new_name: str, index: QModelIndex, property_set_tool: Type[tool.PropertySet]
):
    pset = property_set_tool.get_pset_from_index(index)
    pset.name = new_name


def repaint_pset_table(
    property_set_tool: Type[tool.PropertySet], main_window: Type[tool.MainWindow]
):
    logging.debug(f"Repaint PropertySet Table")

    if main_window.get_active_class() is None:
        property_set_tool.set_enabled(False)
        return

    property_set_tool.set_enabled(True)

    # if pset_table is in rename mode this blocks overwrites
    if property_set_tool.pset_table_is_editing():
        return

    new_property_sets = property_set_tool.get_property_sets(
        main_window.get_active_class()
    )
    table = property_set_tool.get_table()

    existing_property_sets = property_set_tool.get_existing_psets_in_table(table)
    delete_property_sets = existing_property_sets.difference(new_property_sets)
    add_property_sets = new_property_sets.difference(existing_property_sets)
    property_set_tool.remove_property_sets_from_table(delete_property_sets, table)
    property_set_tool.add_property_sets_to_table(add_property_sets, table)
    property_set_tool.update_property_set_table(table)
