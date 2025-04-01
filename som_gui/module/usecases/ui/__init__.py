from PySide6.QtWidgets import QWidget
import som_gui
from .ui_project import ProjectView,ProjectModel
from .ui_class import ClassView
from .ui_property import PropertyView

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..qt import ui_Widget

        self.ui = ui_Widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(som_gui.get_icon())