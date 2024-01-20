from PySide6.QtWidgets import QTableWidget
from som_gui.module import attribute


class AttributeTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute.trigger.table_paint_event(self)
