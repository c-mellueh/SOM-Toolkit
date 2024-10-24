from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING

from PySide6.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem

import SOMcreator
import SOMcreator.util.project
import som_gui
import som_gui.core.tool
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.project.prop import ProjectProperties
from som_gui.module.project.ui import MergeDialog

if TYPE_CHECKING:
    from som_gui.module.project import ui
    from PySide6.QtGui import QAction


class Project(som_gui.core.tool.Project):

    @classmethod
    def get_properties(cls) -> ProjectProperties:
        return som_gui.ProjectProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def add_plugin_save_function(cls, func: Callable):
        """
        add Function that gets called before Project is saved to JSON
        """
        cls.get_properties().plugin_save_functions.append(func)

    @classmethod
    def get_plugin_functions(cls):
        return cls.get_properties().plugin_save_functions

    @classmethod
    def get_filter_matrix(cls):
        return cls.get().get_filter_matrix()

    @classmethod
    def get_use_cases(cls):
        return cls.get().get_usecases()

    @classmethod
    def get_phases(cls):
        return cls.get().get_phases()

    @classmethod
    def create_project(cls):
        logging.info("Create new Project")
        proj = SOMcreator.Project()
        prop: ProjectProperties = cls.get_properties()
        prop.active_project = proj
        som_gui.on_new_project()

    @classmethod
    def load_project(cls, path: str):
        proj = SOMcreator.Project.open(path)
        proj.path = path
        return proj

    @classmethod
    def set_active_project(cls, proj: SOMcreator.Project):
        prop = cls.get_properties()
        prop.active_project = proj

    @classmethod
    def get(cls) -> SOMcreator.Project:
        return cls.get_properties().active_project

    @classmethod
    def get_root_objects(cls, filter_objects=True, proj: SOMcreator.Project = None) -> list[SOMcreator.Object]:
        if proj is None:
            proj: SOMcreator.Project = cls.get_properties().active_project
        if proj is None:
            return []
        return list(proj.get_root_objects(filter=filter_objects))

    @classmethod
    def create_combobox(cls, filter_1):
        box = QComboBox()
        box.addItems([f.name for f in filter_1])
        for index, f in enumerate(filter_1):
            box.setItemData(index, f, CLASS_REFERENCE)
        return box

    @classmethod
    def fill_mapping_table(cls, table: QTableWidget,
                           filter_1: list[SOMcreator.UseCase | SOMcreator.Phase],
                           filter_2: list[SOMcreator.UseCase | SOMcreator.Phase]):

        table.setRowCount(len(filter_2))
        for row, f in enumerate(filter_2):
            item = QTableWidgetItem(f.name)
            item.setData(CLASS_REFERENCE, f)
            table.setItem(row, 0, item)
            table.setCellWidget(row, 1, cls.create_combobox(filter_1))

    @classmethod
    def get_mapping_from_table(cls, table: QTableWidget):
        """
        returns dict with imported filter as Key and existing filter as value
        """
        mapping_dict = dict()
        for row in range(table.rowCount()):
            f2 = table.item(row, 0).data(CLASS_REFERENCE)
            box: QComboBox = table.cellWidget(row, 1)
            f1 = box.itemData(box.currentIndex(), CLASS_REFERENCE)
            mapping_dict[f2] = f1
        return mapping_dict

    @classmethod
    def create_mapping_window(cls, title, filter_1: list[SOMcreator.UseCase | SOMcreator.Phase],
                              filter_2: list[SOMcreator.UseCase | SOMcreator.Phase]):
        dialog = MergeDialog()

        dialog.setWindowTitle(title)
        cls.fill_mapping_table(dialog.widget.tableWidget, filter_1, filter_2)
        if not dialog.exec():
            return None
        else:
            return cls.get_mapping_from_table(dialog.widget.tableWidget)

    @classmethod
    def get_phase_mapping(cls, title, p1: SOMcreator.Project, p2: SOMcreator.Project):
        return cls.create_mapping_window(title, p1.get_phases(), p2.get_phases())

    @classmethod
    def get_use_case_mapping(cls, title, p1: SOMcreator.Project, p2: SOMcreator.Project):
        return cls.create_mapping_window(title, p1.get_usecases(), p2.get_usecases())

    @classmethod
    def merge_projects(cls, title, project_1: SOMcreator.Project, project_2: SOMcreator.Project):
        phase_mapping = cls.get_phase_mapping(title, project_1, project_2)
        if phase_mapping is None:
            return
        use_case_mapping = cls.get_use_case_mapping(title, project_1, project_2)
        if use_case_mapping is None:
            return
        SOMcreator.util.project.merge_projects(project_1, project_2, phase_mapping, use_case_mapping)

    @classmethod
    def set_settings_general_widget(cls, widget: ui.SettingsGeneral):
        cls.get_properties().settings_general_widget = widget

    @classmethod
    def get_settings_general_widget(cls) -> ui.SettingsGeneral:
        return cls.get_properties().settings_general_widget

    @classmethod
    def set_settings_path_widget(cls, widget: ui.SettingsPath):
        cls.get_properties().settings_path_widget = widget

    @classmethod
    def get_settings_path_widget(cls, ) -> ui.SettingsPath:
        return cls.get_properties().settings_path_widget
