from PySide6.QtWidgets import QTableWidget, QWidget, QLineEdit
from PySide6.QtCore import Qt
from PySide6 import QtGui
from som_gui.module import property_set
from .window import Ui_layout_main
from som_gui.icons import get_icon

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
        self.widget.verticalLayout_2.setSpacing(2)
        self.widget.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.widget.verticalLayout_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWindowIcon(get_icon())

    def closeEvent(self, event):
        super().closeEvent(event)
        property_set.trigger.close_pset_window(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_pset_window(self)


class LineInput(QLineEdit):
    def __init__(self) -> None:
        super(LineInput, self).__init__()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if property_set.trigger.key_press_event(event, self.window()):
            super().keyPressEvent(event)
