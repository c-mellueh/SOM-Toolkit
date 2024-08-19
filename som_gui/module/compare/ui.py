from PySide6.QtWidgets import QDialog, QHeaderView, QTreeWidget, QPushButton
from . import window, import_window, trigger
from som_gui.icons import get_icon, get_switch_icon, get_download_icon
from PySide6.QtGui import QPalette
from PySide6.QtCore import QModelIndex, Qt, QRect, QSize


def color_button(button: QPushButton) -> None:
    button.setAutoFillBackground(True)
    pal = button.palette()
    pal.setColor(QPalette.ColorRole.Button, pal.accent().color())
    button.setPalette(pal)


class CompareDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr("Projekte Vergleichen"))
        self.widget.tabWidget.setTabText(0, self.tr("Attribute"))
        button = self.widget.button_download
        button.setIcon(get_download_icon())
        color_button(button)
        button.setText("")


class ProjectSelectDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = import_window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr("Projekte Vergleichen"))
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
