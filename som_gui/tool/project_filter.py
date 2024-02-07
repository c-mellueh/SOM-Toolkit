from __future__ import annotations

import SOMcreator.classes

import som_gui.core.tool
from som_gui.module import project_filter
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui import tool
from typing import TYPE_CHECKING, Callable
from PySide6.QtWidgets import QTableWidgetItem, QMenu
from PySide6.QtGui import QStandardItemModel, QAction
from PySide6.QtCore import Qt, QAbstractItemModel
from SOMcreator.classes import UseCase, Phase

if TYPE_CHECKING:
    from som_gui.module.project_filter.prop import ProjectFilterProperties


class ProjectFilter(som_gui.core.tool.ProjectFilter):

    @classmethod
    def set_selected_header(cls, item):
        props = cls.get_properties()
        props.selected_header = item

    @classmethod
    def create_context_menu(cls, value: UseCase | Phase, menu_list: list[[str, Callable]], pos):
        menu = QMenu()
        actions = list()
        for [action_name, action_func] in menu_list:
            action = QAction(action_name)
            actions.append(action)
            action.triggered.connect(action_func)
        menu.addActions(actions)
        menu.exec(pos)

    @classmethod
    def delete_filter(cls):
        props = cls.get_properties()
        filter_item = props.selected_header
        print(filter_item)
        if isinstance(filter_item, UseCase):
            props.use_cases.remove(filter_item)
            props.delete_use_cases.append(filter_item)
        else:
            props.phases.remove(filter_item)
            props.delete_phases.append(filter_item)

    @classmethod
    def rename_filter(cls):
        props = cls.get_properties()
        filter_item = props.selected_header
        if isinstance(filter_item, UseCase):
            props.use_cases.remove(filter_item)
            props.delete_use_cases.append(filter_item)
        else:
            props.phases.remove(filter_item)
            props.delete_phases.append(filter_item)

    @classmethod
    def add_use_case(cls):
        props = cls.get_properties()
        new_name = tool.Project.get_new_name("Neuer Anwendungsfall", [uc.name for uc in cls.get_use_case_list()])
        new_use_case = UseCase(new_name, new_name, "")
        props.use_cases.append(new_use_case)
        props.add_use_cases.append(new_use_case)
        for uc_list in props.filter_matrix:
            uc_list.append(True)

    @classmethod
    def add_phase(cls):
        props = cls.get_properties()
        new_name = tool.Project.get_new_name("Neue Leistungsphase", [pp.name for pp in cls.get_phase_list()])
        new_phase = Phase(new_name, new_name, "")
        props.phases.append(new_phase)
        props.add_phases.append(new_phase)
        props.filter_matrix.append([True for _ in props.use_cases])

    @classmethod
    def delete_dialog(cls):
        cls.get_properties().project_filter_dialog = None

    @classmethod
    def get_use_case_list(cls):
        return cls.get_properties().use_cases

    @classmethod
    def get_phase_list(cls):
        return cls.get_properties().phases

    @classmethod
    def fill_filter_properties(cls):
        prop = cls.get_properties()
        prop.phases = tool.Project.get_phases()
        prop.use_cases = tool.Project.get_use_cases()
        prop.filter_matrix = list()
        for phase in prop.phases:
            phase_list = list()
            for use_case in prop.use_cases:
                phase_list.append(tool.Project.get().get_filter_state(phase, use_case))
            prop.filter_matrix.append(phase_list)

    @classmethod
    def get_properties(cls) -> ProjectFilterProperties:
        return som_gui.ProjectFilterProperties

    @classmethod
    def create_dialog(cls):
        dialog = cls.get_properties().project_filter_dialog
        if not dialog:
            dialog = project_filter.ui.ProjectFilterDialog()
        cls.get_properties().project_filter_dialog = dialog
        return dialog

    @classmethod
    def get_table(cls):
        prop = cls.get_properties()
        dialog = prop.project_filter_dialog
        return dialog.widget.tableWidget

    @classmethod
    def create_header(cls):
        use_cases = cls.get_use_case_list()
        project_phases = cls.get_phase_list()
        table = cls.get_table()
        table.setColumnCount(len(use_cases))
        table.setRowCount(len(project_phases))
        table.setHorizontalHeaderLabels([uc.name for uc in use_cases])
        table.setVerticalHeaderLabels([pp.name for pp in project_phases])

    @classmethod
    def get_header_item(cls, section: int, orientation: Qt.Orientation) -> None | UseCase | Phase:
        table = cls.get_table()
        return table.model().headerData(section, orientation, CLASS_REFERENCE)

    @classmethod
    def set_column(cls, column: int, use_case: UseCase):
        table = cls.get_table()
        table.model().setHeaderData(column, Qt.Orientation.Horizontal, use_case, CLASS_REFERENCE)
        table.model().setHeaderData(column, Qt.Orientation.Horizontal, use_case.name, Qt.ItemDataRole.DisplayRole)
        for row in range(table.rowCount()):
            cls.update_item(row, column)

    @classmethod
    def set_row(cls, row: int, phase: Phase):
        table = cls.get_table()
        table.model().setHeaderData(row, Qt.Orientation.Vertical, phase, CLASS_REFERENCE)
        table.model().setHeaderData(row, Qt.Orientation.Vertical, phase.name, Qt.ItemDataRole.DisplayRole)
        for column in range(table.columnCount()):
            cls.update_item(row, column)

    @classmethod
    def update_item(cls, row, column):
        table = cls.get_table()
        phase = table.model().headerData(row, Qt.Orientation.Vertical, CLASS_REFERENCE)
        use_case = table.model().headerData(column, Qt.Orientation.Horizontal, CLASS_REFERENCE)
        if phase is None or use_case is None:
            item = QTableWidgetItem()
            table.setItem(row, column, item)
            cs = Qt.CheckState.PartiallyChecked
        else:
            state = cls.get_filter_state(phase, use_case)
            cs = Qt.CheckState.Checked if state else Qt.CheckState.Unchecked
        item = table.item(row, column)
        if item is None:
            item = QTableWidgetItem()
            table.setItem(row, column, item)
        item.setCheckState(cs)

    @classmethod
    def get_filter_state(cls, phase: Phase, use_case: UseCase):
        prop = cls.get_properties()

        phase_index = prop.phases.index(phase)
        use_case_index = prop.use_cases.index(use_case)
        return prop.filter_matrix[phase_index][use_case_index]
