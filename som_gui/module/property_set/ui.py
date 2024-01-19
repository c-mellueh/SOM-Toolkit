from PySide6.QtWidgets import QTableWidget, QWidget
from som_gui.module import property_set
from .window import Ui_layout_main


class PsetTableWidget(QTableWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_event()


class PropertySetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Ui_layout_main()
        self.widget.setupUi(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_pset_window(self)
