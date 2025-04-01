
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal,QObject

if TYPE_CHECKING:
    from som_gui.module.usecases.prop import UsecasesProperties

class Signaller(QObject):
    open_window = Signal()
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

    @classmethod
    def get_window(cls):
        return cls.get_properties.window