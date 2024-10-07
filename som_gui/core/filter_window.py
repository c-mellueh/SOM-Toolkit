from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type
import SOMcreator
from PySide6.QtCore import Qt, QItemSelection, QModelIndex

if TYPE_CHECKING:
    from som_gui import tool


def open_window(filter_window: Type[tool.FilterWindow], project: Type[tool.Project], util: Type[tool.Util],
                search: Type[tool.Search]):
    widget = filter_window.create_widget()
    util.add_shortcut("Ctrl+F", widget, lambda: search_object(filter_window, search))

    filter_window.connect_project_table(project.get())
    filter_window.connect_object_tree(project.get())
    filter_window.connect_pset_tree(project.get())
    widget.show()


def search_object(filter_window: Type[tool.FilterWindow], search: Type[tool.Search]):
    obj = search.search_object()
    if obj is None:
        return
    object_tree = filter_window.get_object_tree()
    parent_list = list()
    parent = obj.parent
    while parent is not None:
        parent_list.append(parent)
        parent = parent.parent

    for item in reversed(parent_list):
        index: QModelIndex = item.index
        object_tree.expand(index)
    index: QModelIndex = obj.index
    flags = object_tree.selectionModel().SelectionFlag.ClearAndSelect | object_tree.selectionModel().SelectionFlag.Rows
    object_tree.selectionModel().select(index, flags)
    object_tree.scrollTo(index.sibling(index.row(), 0))


def pt_context_menu(local_pos, orientation: Qt.Orientation, filter_window: Type[tool.FilterWindow],
                    project: Type[tool.Project]):
    proj = project.get()

    menu_list = list()
    table = filter_window.get_project_table()
    if orientation == Qt.Orientation.Horizontal:  # use_case
        index = table.horizontalHeader().logicalIndexAt(local_pos)
        usecase = proj.get_usecase_by_index(index)
        if len(proj.get_usecases()) > 1:
            menu_list.append(("Anwendungsfall löschen", lambda: filter_window.remove_usecase(usecase, proj)))
        menu_list.append(("Anwendungsfall umbenennen", lambda: filter_window.rename_filter(usecase)))
        menu_list.append(("Anwendungsfall hinzufügen", lambda: filter_window.add_usecase(proj)))
        pos = table.horizontalHeader().viewport().mapToGlobal(local_pos)

    else:
        index = table.verticalHeader().logicalIndexAt(local_pos)
        phase = proj.get_phase_by_index(index)
        if len(proj.get_phases()) > 1:
            menu_list.append(("Leistungsphase löschen", lambda: filter_window.remove_phase(phase, proj)))
        menu_list.append(("Leistungsphase umbenennen", lambda: filter_window.rename_filter(phase)))
        menu_list.append(("Leistungsphase hinzufügen", lambda: filter_window.add_phase(proj)))
        pos = table.horizontalHeader().viewport().mapToGlobal(local_pos)

    filter_window.create_context_menu(menu_list, pos)


def update_object_tree(filter_window: Type[tool.FilterWindow]):
    filter_window.get_object_tree().model().update()


def object_tree_selection_changed(selected: QItemSelection, filter_window: Type[tool.FilterWindow]):
    indexes = selected.indexes()
    if len(indexes) == 0:
        return
    index = indexes[0]
    obj: SOMcreator.Object = index.internalPointer()
    filter_window.set_active_object(obj)
    filter_window.set_object_label(obj.name)
    update_pset_tree(filter_window)


def update_pset_tree(filter_window: Type[tool.FilterWindow]):
    filter_window.get_pset_tree().model().update()


def tree_mouse_move_event(index: QModelIndex, filter_window: Type[tool.FilterWindow]):
    if not filter_window.is_tree_clicked():
        filter_window.tree_activate_click_drag(index)
        return
    filter_window.tree_move_click_drag(index)


def tree_mouse_release_event(index: QModelIndex, filter_window: Type[tool.FilterWindow]):
    if index is None:
        return
    filter_window.tree_release_click_drag()
