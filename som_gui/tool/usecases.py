from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import (
    Signal,
    QObject,
    QModelIndex,
    QItemSelectionModel,
    QSortFilterProxyModel,
    QItemSelection
)
from PySide6.QtWidgets import QLabel
from som_gui.module.usecases import ui
from som_gui.module.usecases import trigger
import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.usecases.prop import UsecasesProperties


class Signaller(QObject):
    open_window = Signal()
    retranslate_ui = Signal()
    class_selection_changed = Signal()

class Usecases(som_gui.core.tool.Usecases):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> UsecasesProperties:
        return som_gui.UsecasesProperties

    @classmethod
    def set_action(cls, name, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name) -> QAction:
        return cls.get_properties().actions[name]

    @classmethod
    def connect_signals(cls):
        from som_gui.module.usecases import trigger

        cls.signaller.open_window.connect(trigger.open_window)
        cls.signaller.retranslate_ui.connect(trigger.retranslate_ui)

    @classmethod
    def get_window(cls) -> ui.Widget | None:
        return cls.get_properties().window

    @classmethod
    def create_window(cls):
        window = ui.Widget()
        cls.get_properties().window = window
        return window

    @classmethod
    def add_models_to_window(cls, project: SOMcreator.SOMProject):
        project_model = ui.ProjectModel(project)
        project_view = cls.get_project_view()
        project_view.setModel(project_model)
        project_view.update_requested.connect(project_model.update_data)

        class_model = ui.ClassModel(project)
        filter_model = ui.ClassFilterModel(class_model.fixed_column_count)
        filter_model.setSourceModel(class_model)
        class_view_1, class_view_2 = cls.get_class_views()
        class_view_1.setModel(filter_model)
        class_view_2.setModel(class_model)
        class_view_2.hideColumn(0)
        class_view_2.hideColumn(1)
        class_view_2.update_requested.connect(class_model.update_data)

    @classmethod
    def connect_models(cls):
        project_model = cls.get_project_model()
        class_model = cls.get_class_model()
        project_model.checkstate_changed.connect(
            lambda: class_model.resize_required.emit(QModelIndex())
        )
        class_model.resize_required.connect(trigger.resize_class_model)
        class_model.resize_required.emit(QModelIndex())

    @classmethod
    def update_class_selection(cls,selected:QItemSelection,deselected):
        indexes = selected.indexes()
        if not indexes:
            cls.get_properties().active_class = None
            cls.signaller.class_selection_changed.emit()
        else:
            cls.get_properties().active_class = indexes[0].internalPointer()

            cls.signaller.class_selection_changed.emit()

    @classmethod
    def connect_class_views(cls):

        proxy_class_view, class_view = cls.get_class_views()
        proxyModel: QSortFilterProxyModel = proxy_class_view.model()
        proxy_selection_model = proxy_class_view.selectionModel()
        selection_model = class_view.selectionModel()

        # Selection

        flags = (
            QItemSelectionModel.SelectionFlag.Rows
            | QItemSelectionModel.SelectionFlag.ClearAndSelect
        )

        def syncSelectionFromProxyToSource(selected, deselected):
            for index in selected.indexes():
                selection_model.select(proxyModel.mapToSource(index), flags)
                return

        def syncSelectionFromSourceToProxy(selected, deselected):
            for index in selected.indexes():
                proxy_selection_model.select(proxyModel.mapFromSource(index), flags)
                return

        proxy_selection_model.selectionChanged.connect(syncSelectionFromProxyToSource)
        selection_model.selectionChanged.connect(syncSelectionFromSourceToProxy)
        selection_model.selectionChanged.connect(cls.update_class_selection)
        cls.signaller.class_selection_changed.connect(trigger.class_selection_changed)
        # expand
        class_view.expanded.connect(
            lambda index: proxy_class_view.expand(proxyModel.mapFromSource(index))
        )
        proxy_class_view.expanded.connect(
            lambda index: class_view.expand(proxyModel.mapToSource(index))
        )
        # collapsed
        class_view.collapsed.connect(
            lambda index: proxy_class_view.collapse(proxyModel.mapFromSource(index))
        )
        proxy_class_view.collapsed.connect(
            lambda index: class_view.collapse(proxyModel.mapToSource(index))
        )
        # Scrollbar
        class_view.verticalScrollBar().valueChanged.connect(
            proxy_class_view.verticalScrollBar().setValue
        )
        proxy_class_view.verticalScrollBar().valueChanged.connect(
            class_view.verticalScrollBar().setValue
        )

    @classmethod
    def get_project_view(cls) -> ui.ProjectView:
        window = cls.get_window()
        if window is None:
            return None
        return window.ui.project_tableView

    @classmethod
    def get_project_model(cls) -> ui.ProjectModel:
        pv = cls.get_project_view()
        if pv is None:
            return None
        return pv.model()

    @classmethod
    def get_class_views(cls) -> tuple[ui.ClassView, ui.ClassView]:
        window = cls.get_window()
        if window is None:
            return None, None
        return window.ui.class_treeView_fixed, window.ui.class_treeView_extendable

    @classmethod
    def get_class_model(cls) -> ui.ClassModel | None:
        view1, view2 = cls.get_class_views()
        if view2.model() is None:
            return view1.model().sourceModel()
        return view2.model()

    @classmethod
    def get_property_views(cls) -> tuple[ui.PropertyView, ui.PropertyView]:
        window = cls.get_window()
        if window is None:
            return None, None
        return (
            window.ui.property_table_view_fixed,
            window.ui.property_table_view_extendable,
        )

    @classmethod
    def get_property_model(cls) -> ui.PropertyModel | None:
        view1, view2 = cls.get_property_views()
        if view2 is None:
            return None
        return view2.model()
    
    @classmethod
    def get_property_label(cls) -> QLabel:
        window = cls.get_window()
        if window is None:
            return None
        return window.ui.property_label

    @classmethod
    def get_active_class(cls) -> SOMcreator.SOMClass|None:
        return cls.get_properties().active_class    