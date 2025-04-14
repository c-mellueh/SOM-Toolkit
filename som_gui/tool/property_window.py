
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

from PySide6.QtCore import Slot,Signal,QObject
import SOMcreator
from som_gui.module.property_window import trigger

if TYPE_CHECKING:
    from som_gui.module.property_window.prop import PropertyWindowProperties

class Signaller(QObject):
    pass

class PropertyWindow(som_gui.core.tool.PropertyWindow):
    signaller = Signaller()
    
    @classmethod
    def get_properties(cls) -> PropertyWindowProperties:
        return som_gui.PropertyWindowProperties

    @classmethod
    def property_info_requested(cls,som_property:SOMcreator.SOMProperty):
        trigger.property_info_requested(som_property)
