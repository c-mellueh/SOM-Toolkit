from PySide6.QtWidgets import QTableWidget, QDialog
from som_gui.icons import get_icon
import som_gui.module.project_filter


class ProjectFilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = som_gui.module.project_filter.window.Ui_Dialog()
        self.widget.setupUi(self)


class ProjectFilterTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowIcon(get_icon())
