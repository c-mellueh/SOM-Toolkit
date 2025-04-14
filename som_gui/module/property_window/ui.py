from PySide6.QtWidgets import QWidget
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
        trigger.window_created(self)
