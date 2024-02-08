from __future__ import annotations
from typing import Type, TYPE_CHECKING

import SOMcreator
from PySide6 import QtGui
from PySide6.QtCore import QModelIndex
import som_gui
from som_gui.core import attribute as attribute_core
from SOMcreator.constants.value_constants import RANGE

if TYPE_CHECKING:
    from som_gui.tool import PropertySet, Object, Attribute, Settings, MainWindow, Popups
    from som_gui.module.property_set_window.ui import PropertySetWindow
