from __future__ import annotations

from typing import TYPE_CHECKING, TextIO, Type

from PySide6.QtCore import QCoreApplication

import SOMcreator

if TYPE_CHECKING:
    from som_gui import tool


def connect_signals(
    predefined_property_set: Type[tool.PredefinedPropertySet],
    property_tool: Type[tool.Property],
    property_table: Type[tool.PropertyTable],
    property_window:Type[tool.PropertyWindow],
):
    predefined_property_set.connect_signals()
    predefined_property_set.signaller.new_property_requested.connect(
        property_tool.signaller.empty_property_requested.emit
    )
    refresh_property_table_func = lambda: property_table.refresh_table(
        predefined_property_set.get_property_table()
    )

    property_tool.signaller.property_created.connect(refresh_property_table_func)
    property_window.signaller.datatype_changed.connect(refresh_property_table_func)
    property_window.signaller.valuetype_changed.connect(refresh_property_table_func)
    property_window.signaller.values_changed.connect(refresh_property_table_func)
    property_window.signaller.name_changed.connect(refresh_property_table_func)
    property_window.signaller.unit_changed.connect(refresh_property_table_func)


def create_main_menu_actions(
    predefined_pset: Type[tool.PredefinedPropertySet],
    main_window: Type[tool.MainWindow],
):
    from som_gui.module.predefined_property_set import trigger

    open_window_action = main_window.add_action(
        None, "PredefinedPset", trigger.open_window
    )
    predefined_pset.set_action("open_window", open_window_action)


def retranslate_ui(
    predefined_pset: Type[tool.PredefinedPropertySet],
    util: Type[tool.Util],
    property_table: Type[tool.PropertyTable],
):
    open_window_action = predefined_pset.get_action("open_window")
    open_window_action.setText(
        QCoreApplication.translate("PredefinedPset", "Predefined Pset")
    )
    if not predefined_pset.get_window():
        return
    window = predefined_pset.get_window()
    window.ui.retranslateUi(window)
    title = util.get_window_title(
        QCoreApplication.translate("PredefinedPset", "Predefined Pset")
    )
    window.setWindowTitle(title)
    property_table.signaller.translation_requested.emit(
        predefined_pset.get_property_table()
    )


def open_window(
    predefined_pset: Type[tool.PredefinedPropertySet],
    util: Type[tool.Util],
    property_table: Type[tool.PropertyTable],
    property_window: Type[tool.PropertyWindow],
):
    if not predefined_pset.get_window():
        dialog = predefined_pset.create_window()
        predefined_pset.connect_window(dialog)
    window = predefined_pset.get_window()
    window.show()
    retranslate_ui(predefined_pset, util, property_table)
    window.activateWindow()


def close_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    predefined_pset.close_window()


def create_pset_context_menu(
    pos,
    predefined_pset: Type[tool.PredefinedPropertySet],
    property_set: Type[tool.PropertySet],
):
    delete = QCoreApplication.translate("PredefinedPset", "Delete")
    rename = QCoreApplication.translate("PredefinedPset", "Rename")
    add = QCoreApplication.translate("PredefinedPset", "Add")

    functions = [
        [delete, predefined_pset.delete_selected_property_set],
        [rename, predefined_pset.rename_selected_property_set],
        [add, predefined_pset.create_property_set],
    ]
    list_widget = predefined_pset.get_pset_list_widget()
    property_set.create_context_menu(list_widget.mapToGlobal(pos), functions)


def pset_selection_changed(
    property_set: SOMcreator.SOMPropertySet,
    predefined_pset: Type[tool.PredefinedPropertySet],
    property_table: Type[tool.PropertyTable],
):
    table_view = predefined_pset.get_property_table()
    predefined_pset.set_active_property_set(property_set)
    repaint_class_list(predefined_pset)
    property_table.set_property_set_of_table(table_view, property_set)
    from som_gui.core import property_table as property_table_core

    property_table_core.update_table(table_view, property_table)
    property_table.signaller.translation_requested.emit(table_view)


def class_context_menu(
    pos,
    predefined_pset: Type[tool.PredefinedPropertySet],
    property_set: Type[tool.PropertySet],
):
    delete = QCoreApplication.translate("PredefinedPset", "Delete")
    remove_link = QCoreApplication.translate("PredefinedPset", "Remove Link")
    functions = [
        [delete, predefined_pset.delete_selected_classes],
        [remove_link, predefined_pset.remove_selected_links],
    ]
    table_widget = predefined_pset.get_class_table_widget()
    property_set.create_context_menu(table_widget.mapToGlobal(pos), functions)


def activate_linked_property_set(
    linked_property_set: SOMcreator.SOMPropertySet,
    predefined_pset: Type[tool.PredefinedPropertySet],
    property_set: Type[tool.PropertySet],
    class_tree: Type[tool.ClassTree],
    main_window: Type[tool.MainWindow],
):
    som_class = linked_property_set.som_class
    if not som_class:
        return
    predefined_pset.close_window()
    tree = main_window.get_class_tree()
    class_tree.expand_to_class(tree, som_class)
    property_set.select_property_set(linked_property_set)


def name_edit_started(predefined_pset: Type[tool.PredefinedPropertySet]):
    props = predefined_pset.get_properties()
    props.is_renaming_predefined_pset = True


def name_edit_stopped(predefined_pset: Type[tool.PredefinedPropertySet]):
    props = predefined_pset.get_properties()
    props.is_renaming_predefined_pset = False


def pset_data_changed(item, property_set: Type[tool.PropertySet]):
    pset = property_set.get_property_set_from_item(item)
    pset.name = item.text()


#################################################################################
# PAINT EVENTS


def repaint_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    repaint_pset_list(predefined_pset)
    repaint_class_list(predefined_pset)
    pass


def repaint_class_list(predefined_pset: Type[tool.PredefinedPropertySet]):
    property_set = predefined_pset.get_active_property_set()
    table_widget = predefined_pset.get_class_table_widget()

    if property_set is None:
        predefined_pset.clear_class_table()
        return
    predefined_property_sets = set(property_set.get_children(filter=True))
    existing_property_sets = predefined_pset.get_existing_psets_in_table_widget(
        table_widget
    )
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(
        predefined_property_sets.difference(existing_property_sets),
        key=lambda p: p.name,
    )

    predefined_pset.remove_property_sets_from_table_widget(
        delete_property_sets, table_widget
    )
    predefined_pset.add_classes_to_table_widget(
        sorted(
            filter(lambda p: p.som_class is not None, add_property_sets),
            key=lambda p: p.som_class.name,
        ),
        table_widget,
    )

    table_widget.resizeColumnToContents(0)
    predefined_pset.update_class_widget()


def repaint_pset_list(predefined_pset: Type[tool.PredefinedPropertySet]):
    if predefined_pset.is_edit_mode_active():
        return
    predefined_pset.get_pset_list_widget()
    predefined_property_sets = set(predefined_pset.get_property_sets())
    list_widget = predefined_pset.get_pset_list_widget()
    existing_property_sets = predefined_pset.get_existing_psets_in_list_widget(
        list_widget
    )
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(
        predefined_property_sets.difference(existing_property_sets),
        key=lambda p: p.name,
    )
    predefined_pset.remove_property_sets_from_list_widget(
        delete_property_sets, list_widget
    )
    predefined_pset.add_property_sets_to_widget(sorted(add_property_sets), list_widget)
    predefined_pset.update_pset_widget()


def add_compare_widget(
    pset_compare: Type[tool.PredefinedPropertySetCompare],
    property_compare: Type[tool.PropertyCompare],
    compare_window: Type[tool.CompareWindow],
):
    name_getter = lambda: QCoreApplication.translate(
        "PredefinedPset", "Predefined Pset"
    )
    compare_window.add_tab(
        name_getter,
        pset_compare.create_widget,
        lambda p0, p1: create_compare_widget(p0, p1, pset_compare, property_compare),
        pset_compare,
        lambda file: export_compare(file, pset_compare, property_compare),
    )


def create_compare_widget(
    project0: SOMcreator.SOMProject,
    project1: SOMcreator.SOMProject,
    pset_compare: Type[tool.PredefinedPropertySetCompare],
    property_compare: Type[tool.PropertyCompare],
):
    """
    add Predefined-Pset-Tab to CompareWidget
    """
    # Create widget
    widget = pset_compare.create_widget()

    # get UI-elements
    pset_tree = property_compare.get_pset_tree(widget)
    value_table = property_compare.get_value_table(widget)
    info_table = property_compare.get_info_table(widget)

    # define and set header labels
    header_labels = [
        property_compare.get_header_name_from_project(project0),
        property_compare.get_header_name_from_project(project1),
    ]
    property_compare.set_header_labels([pset_tree], [value_table], header_labels)
    property_compare.set_header_labels([], [info_table], ["Name"] + header_labels)

    # Compare PropertySets
    psets0, psets1 = list(project0.get_predefined_psets(filter=False)), list(
        project1.get_predefined_psets(filter=False)
    )
    pset_compare.set_predefined_psets(psets0, psets1)
    pset_list = pset_compare.create_pset_list(psets0, psets1)
    for pset0, pset1 in [x for x in pset_list if not None in x]:
        property_compare.compare_property_sets(pset0, pset1)

    # Fill TreeView with PropertySets
    property_compare.fill_pset_tree(pset_tree, pset_compare.get_pset_lists(), True)
    property_compare.add_properties_to_pset_tree(pset_tree, True)

    # Add Color
    root = pset_tree.invisibleRootItem()
    for child_index in range(root.childCount()):
        property_compare.style_tree_item(root.child(child_index))

    # Create triggers
    pset_compare.create_tree_selection_trigger(widget)


def export_compare(
    file: TextIO,
    pset_compare: Type[tool.PredefinedPropertySetCompare],
    property_compare: Type[tool.PropertyCompare],
):
    name = QCoreApplication.translate("PredefinedPset", "PREDEFINED PROPERTYSETS")
    file.write(f"\n{name}\n\n")
    property_compare.export_pset_differences(file, pset_compare.get_pset_lists(), True)
