from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt
from PySide6 import QtGui
from som_gui.module import property_set_window
from .qt.ui_Window import Ui_PropertySetWindow
from som_gui.ressources.icons import get_icon


class PropertySetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PropertySetWindow()
        self.ui.setupUi(self)
        self.ui.verticalLayout_2.setSpacing(2)
        self.ui.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.ui.verticalLayout_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWindowIcon(get_icon())

    def closeEvent(self, event):
        super().closeEvent(event)
        property_set_window.trigger.close_window(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set_window.trigger.repaint_window(self)


class LineInput(QLineEdit):
    def __init__(self) -> None:
        super(LineInput, self).__init__()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if property_set_window.trigger.key_press_event(event, self.window()):
            super().keyPressEvent(event)
