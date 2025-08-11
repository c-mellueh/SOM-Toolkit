from __future__ import annotations
from PySide6.QtWidgets import QCompleter
import SOMcreator


class PropertySetProperties:
    active_pset: SOMcreator.SOMPropertySet = None
    is_renaming_property_set = False
    completer: QCompleter = None
