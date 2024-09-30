from PySide6.QtWidgets import QTableWidget, QDialog
from som_gui.icons import get_icon
import som_gui.module.project_filter as project_filter
from PySide6.QtCore import Qt
from som_gui import tool


class ProjectFilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = project_filter.window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(f"Projekt Filter | {tool.Util.get_status_text()}")

    def closeEvent(self, event):
        project_filter.trigger.close_event()
        super().closeEvent(event)


class ProjectFilterTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.verticalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            project_filter.trigger.uc_context_menu_requested)
        self.verticalHeader().customContextMenuRequested.connect(
            project_filter.trigger.pp_context_menu_requested)

        self.itemClicked.connect(project_filter.trigger.item_changed)
    def paintEvent(self, e):
        super().paintEvent(e)
        project_filter.trigger.refresh_table()
