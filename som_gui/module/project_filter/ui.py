from PySide6.QtWidgets import QTableWidget, QDialog
from som_gui.icons import get_icon
import som_gui.module.project_filter
from PySide6.QtCore import Qt

class ProjectFilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = som_gui.module.project_filter.window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())

    def closeEvent(self, event):
        som_gui.module.project_filter.trigger.close_event()
        super().closeEvent(event)


class ProjectFilterTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.verticalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            som_gui.module.project_filter.trigger.uc_context_menu_requested)
        self.verticalHeader().customContextMenuRequested.connect(
            som_gui.module.project_filter.trigger.pp_context_menu_requested)

        self.itemClicked.connect(som_gui.module.project_filter.trigger.item_changed)
    def paintEvent(self, e):
        super().paintEvent(e)
        som_gui.module.project_filter.trigger.refresh_table()
