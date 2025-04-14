from PySide6.QtWidgets import QWidget,QWidget, QComboBox, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

from som_gui.resources.icons import get_icon
from .qt.ui_Window import Ui_PropertyWindow
import SOMcreator
from . import trigger

class PropertyWindow(QWidget):
    def __init__(self,som_property:SOMcreator.SOMProperty, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowIcon(get_icon())
        self.ui = Ui_PropertyWindow()
        self.ui.setupUi(self)
        self.som_property = som_property
        self.initial_fill = True
        trigger.window_created(self)

    def enterEvent(self, event):
        trigger.update_window(self)
        return super().enterEvent(event)