from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, QObject, QModelIndex,QItemSelectionModel,QSortFilterProxyModel
from som_gui.module.usecases import ui
from som_gui.module.usecases import trigger

if TYPE_CHECKING:
    from som_gui.module.usecases.prop import UsecasesProperties
    import SOMcreator


class Signaller(QObject):
    open_window = Signal()
    retranslate_ui = Signal()


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
    def connect_views(cls):
        proxy_class_view,class_view = cls.get_class_views()
        proxyModel:QSortFilterProxyModel = proxy_class_view.model()
        proxy_selection_model = proxy_class_view.selectionModel()
        selection_model = class_view.selectionModel()
        class_view.setSelectionBehavior(class_view.SelectionBehavior.SelectRows)
        proxy_class_view.setSelectionBehavior(class_view.SelectionBehavior.SelectRows)
        class_view.setSelectionMode(class_view.SelectionMode.SingleSelection)
        proxy_class_view.setSelectionMode(class_view.SelectionMode.SingleSelection)

        def syncSelectionFromProxyToSource(sel_mod ,selected, deselected):
            for index in selected.indexes():
                sourceIndex = proxyModel.mapToSource(index)
                print(f"{index} -> From Proxy {sourceIndex}")
                sel_mod.select(sourceIndex, QItemSelectionModel.SelectionFlag.Select)
                return

        def syncSelectionFromSourceToProxy(selected, deselected):
            for index in selected.indexes():
                proxyIndex = proxyModel.mapFromSource(index)
                print(f"{index}From Source {proxyIndex}")
                proxy_selection_model.select(proxyIndex, QItemSelectionModel.SelectionFlag.Select)
                return

        def test(sm,selection,deselected):
            print(selection)
        proxy_selection_model.selectionChanged.connect(lambda s,d,sm = selection_model:syncSelectionFromProxyToSource(sm,s,d))
        selection_model.selectionChanged.connect(lambda s,d,sm = selection_model:test(sm,s,d))

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
