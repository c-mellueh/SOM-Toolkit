from PySide6.QtWidgets import QTableWidget
from som_gui.module import attribute_table


class AttributeTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        attribute_table.trigger.connect_table(self)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_table.trigger.table_paint_event(self)
