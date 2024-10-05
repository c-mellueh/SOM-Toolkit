from __future__ import annotations

from typing import TYPE_CHECKING, Callable
import logging
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QInputDialog, QLineEdit

import SOMcreator
import som_gui.core.tool
import som_gui
from som_gui import tool

if TYPE_CHECKING:
    from som_gui.module.filter_window.prop import FilterWindowProperties
from som_gui.module.filter_window import ui, trigger


class FilterWindow(som_gui.core.tool.FilterWindow):
    @classmethod
    def get_properties(cls) -> FilterWindowProperties:
        return som_gui.FilterWindowProperties

    @classmethod
    def get_project_table(cls) -> ui.ProjectView:
        return cls.get().ui.project_table

    @classmethod
    def get_object_tree(cls) -> ui.ObjectTreeView:
        return cls.get().ui.object_tree

    @classmethod
    def get_pset_tree(cls):
        return cls.get().ui.pset_tree

    @classmethod
    def create_widget(cls) -> ui.FilterWidget:
        cls.get_properties().widget = ui.FilterWidget()
        return cls.get_properties().widget

    @classmethod
    def connect_pset_tree(cls, project: SOMcreator.Project):
        pset_tree = cls.get_pset_tree()
        pset_tree.setModel(ui.PsetModel(project))

    @classmethod
    def connect_object_tree(cls, project: SOMcreator.Project):
        object_tree = cls.get_object_tree()
        object_tree.setModel(ui.ObjectModel(project))
        object_tree.setSelectionMode(object_tree.SelectionMode.SingleSelection)
        object_tree.setSelectionBehavior(object_tree.SelectionBehavior.SelectRows)
        object_tree.selectionModel().selectionChanged.connect(trigger.object_tree_clicked)

    @classmethod
    def connect_project_table(cls, project: SOMcreator.Project):
        project_table = cls.get_project_table()
        model = ui.ProjectModel(project)
        project_table.setModel(model)
        horizontal_header = project_table.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(trigger.pt_horizontal_context_requested)

        vertical_header = project_table.verticalHeader()
        vertical_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(trigger.pt_vertical_context_requested)


    @classmethod
    def get(cls) -> ui.FilterWidget | None:
        return cls.get_properties().widget

    @classmethod
    def add_usecase(cls, project: SOMcreator.Project):
        new_name = tool.Util.get_new_name("Neuer Anwendungsfall", [uc.name for uc in project.get_usecases()])
        usecase = SOMcreator.UseCase(new_name, new_name, new_name)
        model = cls.get_project_table().model()
        model.beginInsertColumns(QModelIndex(), model.columnCount(), model.columnCount())
        model.project.add_use_case(usecase)
        model.endInsertColumns()

    @classmethod
    def remove_usecase(cls, usecase: SOMcreator.UseCase, project: SOMcreator.Project):
        model = cls.get_project_table().model()
        usecase_index = project.get_use_case_index(usecase)
        model.beginRemoveColumns(QModelIndex(), usecase_index, usecase_index)
        project.remove_use_case(usecase)
        model.endRemoveColumns()

    @classmethod
    def add_phase(cls, project: SOMcreator.Project):
        new_name = tool.Util.get_new_name("Neue Phase", [uc.name for uc in project.get_usecases()])
        phase = SOMcreator.Phase(new_name, new_name, new_name)
        model = cls.get_project_table().model()
        model.beginInsertRows(QModelIndex(), model.rowCount(), model.rowCount())
        model.project.add_project_phase(phase)
        model.endInsertRows()

    @classmethod
    def remove_phase(cls, phase: SOMcreator.Phase, project: SOMcreator.Project):
        model = cls.get_project_table().model()
        phase_index = project.get_phase_index(phase)
        model.beginRemoveRows(QModelIndex(), phase_index, phase_index)
        project.remove_phase(phase)
        model.endRemoveRows()

    @classmethod
    def rename_filter(cls, filter: SOMcreator.UseCase | SOMcreator.Phase):
        new_name, ok = QInputDialog.getText(cls.get(), "Edit Header", "Enter new header title:", QLineEdit.Normal,
                                            filter.name)
        if ok:
            filter.name = new_name

    @classmethod
    def create_context_menu(cls, menu_list: list[tuple[str, Callable]], pos):
        menu = QMenu()
        actions = list()
        for [action_name, action_func] in menu_list:
            action = QAction(action_name)
            actions.append(action)
            action.triggered.connect(action_func)
        menu.addActions(actions)
        menu.exec(pos)

    @classmethod
    def set_active_object(cls, obj: SOMcreator.Object):
        cls.get_properties().active_object = obj

    @classmethod
    def get_active_object(cls) -> SOMcreator.Object:
        return cls.get_properties().active_object

    @classmethod
    def set_object_label(cls, value: str):
        cls.get().ui.label.setText(value)
