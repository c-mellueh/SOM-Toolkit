from __future__ import annotations
import logging

from PySide6.QtCore import (
    QAbstractTableModel,
    QCoreApplication,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTableView
import SOMcreator

class PropertyView(QTableView):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

class PropertyModel(QAbstractTableModel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)