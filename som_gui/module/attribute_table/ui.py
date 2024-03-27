from PySide6.QtWidgets import QTableWidget
from som_gui.module import attribute_table
from PySide6.QtGui import QDropEvent, QDragMoveEvent
import pickle
class AttributeTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        attribute_table.trigger.connect_table(self)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_table.trigger.table_paint_event(self)

    def mimeData(self, items):
        mime_data = super().mimeData(items)
        return attribute_table.trigger.create_mime_data(list(items), mime_data)

    def dropEvent(self, event: QDropEvent):
        attribute_table.trigger.drop_event(event, self)
        super().dropEvent(event)
