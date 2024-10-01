from __future__ import annotations


import som_gui.core.tool
from som_gui.module import project_filter
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui import tool
from typing import TYPE_CHECKING, Callable
from PySide6.QtWidgets import QTableWidgetItem, QMenu, QCheckBox
from PySide6.QtGui import QStandardItemModel, QAction
from PySide6.QtCore import Qt, QAbstractItemModel
from SOMcreator import UseCase, Phase

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
        proj = tool.Project.get()
        if isinstance(filter_item, UseCase):
            proj.remove_use_case(filter_item)
        else:
            proj.remove_phase(filter_item)

    @classmethod
    def rename_filter(cls):
        props = cls.get_properties()
        filter_item = props.selected_header
        if isinstance(filter_item, UseCase):
            new_name = tool.Popups.get_new_use_case_name(filter_item.name, props.project_filter_dialog)
        else:
            new_name = tool.Popups.get_phase_name(filter_item.name, props.project_filter_dialog)
        filter_item.name = new_name

    @classmethod
    def add_use_case(cls):
        new_name = tool.Util.get_new_name("Neuer Anwendungsfall", [uc.name for uc in cls.get_use_case_list()])
        new_use_case = UseCase(new_name, new_name, "")
        proj = tool.Project.get()
        proj.add_use_case(new_use_case)
        cls.get_table().resizeColumnsToContents()

    @classmethod
    def add_phase(cls):
        proj = tool.Project.get()
        new_name = tool.Util.get_new_name("Neue Leistungsphase", [pp.name for pp in cls.get_phase_list()])
        new_phase = Phase(new_name, new_name, "")
        proj.add_project_phase(new_phase)
        cls.get_table().resizeRowsToContents()

    @classmethod
    def delete_dialog(cls):
        cls.get_properties().project_filter_dialog = None

    @classmethod
    def get_use_case_list(cls):
        return tool.Project.get().get_usecases()

    @classmethod
    def get_phase_list(cls):
        return tool.Project.get().get_phases()

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
        phase_index = cls.get_phase_list().index(phase)
        use_case_index = cls.get_use_case_list().index(use_case)
        return cls.get_filter_matrix()[phase_index][use_case_index]

    @classmethod
    def get_filter_matrix(cls):
        return tool.Project.get().get_filter_matrix()

    @classmethod
    def set_state(cls, use_case, phase, state):
        proj = tool.Project.get()
        proj.set_filter_state(phase, use_case, state)
