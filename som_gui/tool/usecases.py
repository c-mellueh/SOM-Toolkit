from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, QObject
from som_gui.module.usecases import ui

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
        return window

    @classmethod
    def add_models_to_window(cls,window:ui.Widget,project:SOMcreator.SOMProject):
        project_model = ui.ProjectModel(project)
        window.ui.project_tableView.setModel(project_model)
