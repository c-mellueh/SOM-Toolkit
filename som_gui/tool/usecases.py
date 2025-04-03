from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, QObject,QModelIndex
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
    def get_window(cls) -> ui.Widget|None:
        return cls.get_properties().window

    @classmethod
    def create_window(cls):
        window = ui.Widget()
        cls.get_properties().window = window
        cls.get_class_views()[0].hide()
        return window

    @classmethod
    def add_models_to_window(cls,project:SOMcreator.SOMProject):
        project_model = ui.ProjectModel(project)
        project_view = cls.get_project_view()
        project_view.setModel(project_model)
        project_view.update_requested.connect(project_model.update_data)

        class_model = ui.ClassModel(project)
        class_view_1,class_view_2 = cls.get_class_views()
        class_view_2.setModel(class_model)
        class_view_2.update_requested.connect(class_model.update_data)
        
    @classmethod
    def connect_models(cls):
        project_model = cls.get_project_model()
        class_model = cls.get_class_model()
        project_model.checkstate_changed.connect(lambda:class_model.resize_required.emit(QModelIndex()))
        class_model.resize_required.connect(trigger.resize_class_model)
        class_model.resize_required.emit(QModelIndex())
        
    @classmethod
    def get_project_view(cls) -> ui.ProjectView:
        window = cls.get_window()
        if window is None:
            return None
        return window.ui.project_tableView

    @classmethod
    def get_project_model(cls) ->ui.ProjectModel:
        pv = cls.get_project_view()
        if pv is None:
            return None
        return pv.model()
    

    
    @classmethod
    def get_class_views(cls) -> tuple[ui.ClassView,ui.ClassView]:
        window = cls.get_window()
        if window is None:
            return None,None
        return window.ui.class_treeView_fixed,window.ui.class_treeView_extendable

    @classmethod
    def get_class_model(cls) -> ui.ClassModel|None:
        view1,view2 = cls.get_class_views()
        if view2 is None:
            return None
        return view2.model()

    @classmethod
    def get_property_views(cls) -> tuple[ui.PropertyView,ui.PropertyView]:
        window = cls.get_window()
        if window is None:
            return None,None
        return window.ui.property_table_view_fixed,window.ui.property_table_view_extendable

    @classmethod
    def get_property_model(cls) -> ui.PropertyModel|None:
        view1,view2 = cls.get_property_views()
        if view2 is None:
            return None
        return view2.model()