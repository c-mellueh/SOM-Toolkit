from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QTableWidget

import SOMcreator
from som_gui.module import property_table

if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow


class PropertyTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        property_table.trigger.connect_table(self)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.ContiguousSelection)
        self.property_set: SOMcreator.SOMPropertySet | None = None

    def paintEvent(self, e):
        super().paintEvent(e)
        property_table.trigger.table_paint_event(self)

    def mimeData(self, items):
        mime_data = super().mimeData(items)
        return property_table.trigger.create_mime_data(list(items), mime_data)

    def dropEvent(self, event: QDropEvent):
        property_table.trigger.drop_event(event, self)
        super().dropEvent(event)

    def window(self) -> MainWindow:
        return super().window()
