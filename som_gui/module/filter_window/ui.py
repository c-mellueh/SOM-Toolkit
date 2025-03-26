from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING


from PySide6.QtCore import (
    QAbstractItemModel,
    QAbstractTableModel,
    QCoreApplication,
    QSortFilterProxyModel,
    QModelIndex,
    Qt,
    Signal,
    QSize,
    QRect,
    QPoint,
)
    
from PySide6.QtGui import QMouseEvent, QColor, QPainter, QPalette, QBrush,QPaintEvent
from PySide6.QtWidgets import (
    QTableView,
    QTreeView,
    QWidget,
    QHeaderView,
    QStyleOptionHeader,
    QStyle,
)
import SOMcreator
import som_gui
from som_gui import tool
from . import trigger

from .ui_table import ProjectModel,ProjectView
from .ui_tree import ClassModel,ClassTreeView,PsetTreeView,PsetModel


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        from .qt import ui_Settings

        self.ui = ui_Settings.Ui_FilterWindow()
        self.ui.setupUi(self)
        trigger.settings_widget_created(self)


class FilterWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .qt import ui_Widget

        self.ui = ui_Widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(som_gui.get_icon())
