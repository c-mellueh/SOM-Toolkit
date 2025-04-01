from __future__ import annotations
import logging

from PySide6.QtCore import (
    QAbstractItemModel,
    QCoreApplication,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTreeView
import SOMcreator

class ClassView(QTreeView):
    update_requested = Signal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTreeView.SelectionMode.SingleSelection)

    

class ClassModel(QAbstractItemModel):
    def __init__(self,project:SOMcreator.SOMProject,*args,**kwargs):
        self.project = project
        super().__init__(*args,**kwargs)
    
    def update_data(self):
        pass