from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui import tool


def open_project_filter_window(project_filter_tool: Type[tool.ProjectFilter], project_tool: Type[tool.Project]):
    dialog = project_filter_tool.create_dialog()
    project_filter_tool.fill_filter_properties()
    project_filter_tool.create_header()
    dialog.exec()
    close_dialog(project_filter_tool)


def context_menu(local_pos, orientation: int, project_filter: Type[tool.ProjectFilter]):
    menu_list = list()
    table = project_filter.get_table()
    if orientation == 0:  # use_case
        index = table.horizontalHeader().logicalIndexAt(local_pos)
        item = project_filter.get_header_item(index, Qt.Orientation.Horizontal)

        if len(project_filter.get_use_case_list()) > 1:
            menu_list.append(["Anwendungsfall löschen", project_filter.delete_filter])
        menu_list.append(["Anwendungsfall umbenennen", project_filter.rename_filter])
        menu_list.append(["Anwendungsfall hinzufügen", project_filter.add_use_case])
        pos = table.horizontalHeader().viewport().mapToGlobal(local_pos)

    else:  # project_phase
        index = table.verticalHeader().logicalIndexAt(local_pos)
        item = project_filter.get_header_item(index, Qt.Orientation.Vertical)
        if len(project_filter.get_phase_list()) > 1:
            menu_list.append(["Leistungsphase löschen", project_filter.delete_filter])
        menu_list.append(["Leistungsphase umbenennen", project_filter.rename_filter])
        menu_list.append(["Leistungsphase hinzufügen", project_filter.add_phase])
        pos = table.verticalHeader().viewport().mapToGlobal(local_pos)

    project_filter.set_selected_header(item)
    project_filter.create_context_menu(index, menu_list, pos)

    pass


def update_project_filter(project_filter_tool: Type[tool.ProjectFilter]):
    pass


def refresh_table(project_filter: Type[tool.ProjectFilter], project: Type[tool.Project]):
    use_case_list = project_filter.get_use_case_list()
    phase_list = project_filter.get_phase_list()
    table = project_filter.get_table()
    project_filter.create_header()

    for column_index, use_case in enumerate(use_case_list):
        item = project_filter.get_header_item(column_index, Qt.Orientation.Horizontal)
        if column_index == table.model().columnCount():
            table.model().insertColumn(column_index)
        if item != use_case:
            project_filter.set_column(column_index, use_case)

    for row_index, phase in enumerate(phase_list):
        item = project_filter.get_header_item(row_index, Qt.Orientation.Vertical)
        if item != phase:
            project_filter.set_row(row_index, phase)


def close_dialog(project_filter_tool: Type[tool.ProjectFilter]):
    project_filter_tool.delete_dialog()
