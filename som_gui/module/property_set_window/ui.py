from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QWidget

from som_gui.module import property_set_window
from som_gui.resources.icons import get_icon
from .qt.ui_Window import Ui_PropertySetWindow
from .qt.ui_SplitterSettings import Ui_SplitterSettings
from ..attribute.qt.ui_UnitSettings import Ui_UnitSettings
from som_gui.module import property_set_window

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

class SplitterSettings(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui = Ui_SplitterSettings()
        self.ui.setupUi(self)
        property_set_window.trigger.splitter_settings_created(self)

