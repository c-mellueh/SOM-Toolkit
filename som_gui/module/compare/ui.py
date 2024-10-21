from PySide6.QtWidgets import QDialog, QTreeWidget, QPushButton
from . import trigger
from .qt import ui_ImportWidget, ui_Widget
from som_gui.icons import get_icon, get_switch_icon, get_download_icon
from PySide6.QtGui import QPalette
from PySide6.QtCore import QModelIndex
from som_gui import tool

def color_button(button: QPushButton) -> None:
    button.setAutoFillBackground(True)
    pal = button.palette()
    pal.setColor(QPalette.ColorRole.Button, pal.accent().color())
    button.setPalette(pal)


class CompareDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = ui_Widget.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr(f"Projekte Vergleichen | {tool.Util.get_status_text()}"))
        self.widget.tabWidget.setTabText(0, self.tr("Attribute"))
        button = self.widget.button_download
        button.setIcon(get_download_icon())
        color_button(button)
        button.setText("")


class ProjectSelectDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = ui_ImportWidget.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr(f"Projekte Vergleichen | {tool.Util.get_status_text()}"))
        button = self.widget.button_switch
        button.setText("")
        button.setIcon(get_switch_icon())
        color_button(button)





class EntityTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drawBranches(self, painter, rect, index: QModelIndex):
        results = trigger.draw_branches(self, painter, rect, index)
        super().drawBranches(*results)
