from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QItemSelection, QModelIndex, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QCheckBox, QFormLayout, QLabel

import SOMcreator

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_ import ui as property_ui
    from som_gui.module.filter_window import ui


def create_main_menu_actions(
    filter_window: Type[tool.FilterWindow], main_window: Type[tool.MainWindow]
):
    from som_gui.module.filter_window import trigger

    action = main_window.add_action("menuEdit", "FilterWindow", trigger.open_window)
    filter_window.set_action("open_window", action)


def retranslate_ui(filter_window: Type[tool.FilterWindow], util: Type[tool.Util]):
    action = filter_window.get_action("open_window")
    action.setText(QCoreApplication.translate("FilterWindow", "Project Filter"))

    if filter_window.get():
        title = QCoreApplication.translate("FilterWindow", "Project Filter")
        filter_window.get().ui.retranslateUi(filter_window.get())
        filter_window.get().setWindowTitle(util.get_window_title(title))


def open_window(
    filter_window: Type[tool.FilterWindow],
    project: Type[tool.Project],
    util: Type[tool.Util],
    search: Type[tool.Search],
):

    if filter_window.get():
        filter_window.get().show()
        filter_window.get().activateWindow()
        return

    widget = filter_window.create_widget(project.get())
    util.add_shortcut(
        "Ctrl+F", widget, lambda: search_class(filter_window, search, project)
    )
    filter_window.connect_project_table(project.get())
    filter_window.connect_class_tree(project.get())
    retranslate_ui(filter_window, util)
    widget.show()


def filter_changed_externally(filter_window: Type[tool.FilterWindow]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = filter_window.get_project_table().model()
    logging.debug(
        f"Filter Changed Externally. rowCount: {model.last_row_count} -> {model.rowCount()} columnCount:{model.last_col_count} -> {model.columnCount()}"
    )

    # Remove Rows (Phases)
    if model.last_row_count > model.rowCount():
        model.beginRemoveRows(QModelIndex(), model.rowCount(), model.last_row_count - 1)
        model.endRemoveRows()

    # Insert Rows (Phases)
    if model.last_row_count < model.rowCount():
        model.beginInsertRows(QModelIndex(), model.last_row_count + 1, model.rowCount())
        model.endInsertRows()

    # Remove Colums (UseCases)
    if model.last_col_count > model.columnCount():
        model.beginRemoveColumns(
            QModelIndex(), model.columnCount(), model.last_col_count - 1
        )
        model.endRemoveColumns()

    # Insert Colums (UseCases)
    if model.last_col_count < model.columnCount():
        model.beginInsertColumns(
            QModelIndex(), model.last_col_count + 1, model.columnCount()
        )
        model.endInsertColumns()


def search_class(
    filter_window: Type[tool.FilterWindow],
    search: Type[tool.Search],
    project: Type[tool.Project],
):
    som_class = search.search_class(list(project.get().get_classes(filter=True)))
    if som_class is None:
        return
    class_tree = filter_window.get_class_trees()
    parent_list = list()
    parent = som_class.parent
    while parent is not None:
        parent_list.append(parent)
        parent = parent.parent

    # needs to happen top down. DataModel creates children only if parent is already created
    # You can't combine the parent search with expanding the Tree it needs to happen in two steps

    for item in reversed(parent_list):
        index: QModelIndex = item.index
        class_tree.expand(index)

    index: QModelIndex = som_class.index
    flags = (
        class_tree.selectionModel().SelectionFlag.ClearAndSelect
        | class_tree.selectionModel().SelectionFlag.Rows
    )
    class_tree.selectionModel().select(index, flags)
    class_tree.scrollTo(
        index.sibling(index.row(), 0), class_tree.ScrollHint.EnsureVisible
    )


def pt_context_menu(
    local_pos,
    orientation: Qt.Orientation,
    filter_window: Type[tool.FilterWindow],
    project: Type[tool.Project],
):
    proj = project.get()

    menu_list = list()
    table = filter_window.get_project_table()
    if orientation == Qt.Orientation.Horizontal:  # use_case
        index = table.horizontalHeader().logicalIndexAt(local_pos)
        usecase = proj.get_usecase_by_index(index)

        del_uc = QCoreApplication.translate("FilterWindow", "Delete UseCase")
        rename_uc = QCoreApplication.translate("FilterWindow", "Rename UseCase")
        add_uc = QCoreApplication.translate("FilterWindow", "Add UseCase")

        if len(proj.get_usecases()) > 1:
            menu_list.append(
                (del_uc, lambda: filter_window.remove_usecase(usecase, proj))
            )
        menu_list.append((rename_uc, lambda: filter_window.rename_filter(usecase)))
        menu_list.append((add_uc, lambda: filter_window.add_usecase(proj)))
        pos = table.horizontalHeader().viewport().mapToGlobal(local_pos)

    elif orientation == Qt.Orientation.Vertical:
        index = table.verticalHeader().logicalIndexAt(local_pos)
        phase = proj.get_phase_by_index(index)
        del_ph = QCoreApplication.translate("FilterWindow", "Delete Phase")
        rename_ph = QCoreApplication.translate("FilterWindow", "Rename Phase")
        add_ph = QCoreApplication.translate("FilterWindow", "Add Phase")

        if len(proj.get_phases()) > 1:
            menu_list.append((del_ph, lambda: filter_window.remove_phase(phase, proj)))
        menu_list.append((rename_ph, lambda: filter_window.rename_filter(phase)))
        menu_list.append((add_ph, lambda: filter_window.add_phase(proj)))
        pos = table.verticalHeader().viewport().mapToGlobal(local_pos)

    filter_window.create_context_menu(menu_list, pos)


def update_class_tree(filter_window: Type[tool.FilterWindow]): 
    model = filter_window.get_class_model()
    logging.debug(f"Update Class Tree")
    for tree in filter_window.get_class_trees():
        tree.model().update()
        tree.repaint()

        for i in range(model.columnCount()):
            if tree.mode != 0:
                tree.setColumnHidden(i,i <len(tree.model().column_titles))
            else:
                hide = i >=len(tree.model().column_titles)
                if hide and not tree.isColumnHidden(i):
                    tree.setColumnHidden(i,hide)

def class_tree_selection_changed(
    selected: QItemSelection, filter_window: Type[tool.FilterWindow]
):
    indexes = selected.indexes()
    if len(indexes) == 0:
        return
    index = indexes[0]
    som_class: SOMcreator.SOMClass = index.internalPointer()
    filter_window.set_active_class(som_class)
    filter_window.set_class_label(som_class.name)
    update_pset_tree(filter_window)


def update_pset_tree(filter_window: Type[tool.FilterWindow]):
    model = filter_window.get_pset_model()
    for tree in filter_window.get_pset_trees():
        tree.model().update()
        for i in range(model.columnCount()):
            if tree.mode != 0:
                tree.setColumnHidden(i,i <len(tree.model().column_titles))
            else:
                tree.setColumnHidden(i,i >=len(tree.model().column_titles))

def tree_mouse_move_event(index: QModelIndex, filter_window: Type[tool.FilterWindow]):
    if not filter_window.is_tree_clicked():
        filter_window.tree_activate_click_drag(index)
        return
    filter_window.tree_move_click_drag(index)


def tree_mouse_release_event(
    index: QModelIndex, filter_window: Type[tool.FilterWindow]
):
    if index is None:
        return
    filter_window.tree_release_click_drag()


### Compare Widget


def add_compare_widget(
    filter_compare: Type[tool.FilterCompare],
    property_compare: Type[tool.PropertyCompare],
    compare_window: Type[tool.CompareWindow],
):
    name_getter = lambda: QCoreApplication.translate("FilterWindow", "Project Filter")
    compare_window.add_tab(
        name_getter,
        filter_compare.create_widget,
        lambda p0, p1: create_compare_widget(p0, p1, filter_compare, property_compare),
        filter_compare,
        lambda file: export_filter_differences(file, filter_compare, property_compare),
    )


def create_compare_widget(
    project0: SOMcreator.SOMProject,
    project1: SOMcreator.SOMProject,
    filter_compare: Type[tool.FilterCompare],
    property_compare: Type[tool.PropertyCompare],
):
    """
    Sets up the Filter Compare Widget to function properly
    """
    # Define Projects
    property_compare.set_projects(
        project0, project1
    )  # defines which projects will be compared
    filter_compare.set_projects(project0, project1)

    # Create widget
    widget = filter_compare.create_widget()

    # get UI-elements
    class_tree_widget = property_compare.get_class_tree(widget)
    pset_tree = property_compare.get_pset_tree(widget)
    value_table = property_compare.get_value_table(widget)

    # Add Wordwrap to Header

    # fill ClassTree with classes
    property_compare.create_class_lists()
    property_compare.fill_class_tree(class_tree_widget, add_missing=False)

    # define and set header labels & add wordwrap
    filter_compare.make_header_wordwrap(class_tree_widget)
    filter_compare.make_header_wordwrap(pset_tree)
    header_labels = [
        property_compare.get_header_name_from_project(project0),
        property_compare.get_header_name_from_project(project1),
    ]
    property_compare.set_header_labels(
        [class_tree_widget, pset_tree], [value_table], header_labels
    )

    filter_compare.create_tree_selection_trigger(widget)

    # Search for matchups
    filter_compare.find_matching_phases(project0, project1)
    filter_compare.find_matching_usecases(project0, project1)

    filter_compare.append_collumns(class_tree_widget, pset_tree)
    for child_index in range(class_tree_widget.invisibleRootItem().childCount()):
        child = class_tree_widget.invisibleRootItem().child(child_index)
        filter_compare.fill_tree_with_checkstates(child)
        filter_compare.style_class_tree(child)
    for col in range(2, class_tree_widget.columnCount()):
        class_tree_widget.setColumnWidth(col, 58)

    widget.ui.table_widget_values.hide()


def filter_tab_class_tree_selection_changed(
    widget: property_ui.PropertyWidget,
    property_compare: Type[tool.PropertyCompare],
    filter_compare: Type[tool.FilterCompare],
):
    som_class = property_compare.get_selected_entity(
        property_compare.get_class_tree(widget)
    )
    tree_widget = property_compare.get_pset_tree(widget)
    pset_list = property_compare.get_pset_list(som_class)

    property_compare.fill_pset_tree(tree_widget, pset_list, add_missing=False)
    property_compare.add_properties_to_pset_tree(tree_widget, False)
    for child_index in range(tree_widget.invisibleRootItem().childCount()):
        child = tree_widget.invisibleRootItem().child(child_index)
        filter_compare.fill_tree_with_checkstates(child)

    for col in range(2, tree_widget.columnCount()):
        tree_widget.setColumnWidth(col, 58)


def export_filter_differences(
    file,
    filter_compare: Type[tool.FilterCompare],
    property_compare: Type[tool.PropertyCompare],
):
    name = QCoreApplication.translate("FilterWindow", "CLASS FILTER")
    file.write(f"\n{name:46s}\n\n")
    filter_compare.export_class_filter_differences(file, property_compare)
    file.write("\n")


# Settings WIdget
def settings_widget_created(
    widget: ui.SettingsWidget,
    filter_window: Type[tool.FilterWindow],
    project: Type[tool.Project],
):
    filter_window.set_settings_widget(widget)

    proj = project.get()
    phase_layout = QFormLayout()
    widget.ui.widget_phase.setLayout(phase_layout)
    usecase_layout = QFormLayout()
    widget.ui.widget_usecase.setLayout(usecase_layout)

    for phase in proj.get_phases():
        cb = QCheckBox()
        phase_index = proj.get_phase_index(phase)
        cb.setChecked(bool(phase_index in proj.active_phases))
        phase_layout.addRow(QLabel(phase.name), cb)

    for usecase in proj.get_usecases():
        cb = QCheckBox()
        usecase_index = proj.get_usecase_index(usecase)
        cb.setChecked(bool(usecase_index in proj.active_usecases))
        usecase_layout.addRow(QLabel(usecase.name), cb)


def settings_accepted(
    filter_window: Type[tool.FilterWindow],
    project: Type[tool.Project],
    popups: Type[tool.Popups],
):
    proj = project.get()
    widget = filter_window.get_settings_widget()
    phase_layout: QFormLayout = widget.ui.widget_phase.layout()
    usecase_layout: QFormLayout = widget.ui.widget_usecase.layout()

    active_phases = list()
    for row in range(phase_layout.rowCount()):
        cb: QCheckBox = phase_layout.itemAt(
            row, QFormLayout.ItemRole.FieldRole
        ).widget()
        if cb.isChecked():
            active_phases.append(row)

    active_usecases = list()
    for row in range(usecase_layout.rowCount()):
        cb: QCheckBox = usecase_layout.itemAt(
            row, QFormLayout.ItemRole.FieldRole
        ).widget()
        if cb.isChecked():
            active_usecases.append(row)
    proj.active_phases = active_phases
    proj.active_usecases = active_usecases
    logging.info(
        f"Set Active Usecases {[proj.get_usecase_by_index(i).name for i in proj.active_usecases]}"
    )
    logging.info(
        f"Set Active Phases {[proj.get_phase_by_index(i).name for i in proj.active_phases]}"
    )


def settings_combobox_changed(
    filter_window: Type[tool.FilterWindow],
    project: Type[tool.Project],
    util: Type[tool.Util],
):
    widget = filter_window.get_settings_widget()
    combobox_usecase = widget.ui.cb_usecase
    combobox_phase = widget.ui.cb_phase
    usecase_name = combobox_usecase.currentText()
    phase_name = combobox_phase.currentText()
    if not all([usecase_name, phase_name]):
        return
    proj = project.get()
    usecase = proj.get_usecase_by_name(usecase_name)
    phase = proj.get_phase_by_name(phase_name)

    # add warning icons to combobox
    for uc_name, index in util.get_text_from_combobox(combobox_usecase).items():
        uc = proj.get_usecase_by_name(uc_name)
        if not proj.get_filter_state(phase, uc):
            warn_icon = widget.style().standardIcon(
                widget.style().StandardPixmap.SP_MessageBoxWarning
            )
            combobox_usecase.setItemIcon(index.row(), warn_icon)
        else:
            combobox_usecase.setItemIcon(index.row(), QIcon())

    for ph_name, index in util.get_text_from_combobox(combobox_phase).items():
        ph = proj.get_phase_by_name(ph_name)
        if not proj.get_filter_state(ph, usecase):
            warn_icon = widget.style().standardIcon(
                widget.style().StandardPixmap.SP_MessageBoxWarning
            )
            combobox_phase.setItemIcon(index.row(), warn_icon)
        else:
            combobox_phase.setItemIcon(index.row(), QIcon())
