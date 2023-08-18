from __future__ import annotations  # make own class referencable

import os.path
from typing import TYPE_CHECKING

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QWheelEvent, QMouseEvent, QTransform, QShortcut, QKeySequence,QPainter,QImage,QMoveEvent
from PySide6.QtWidgets import QGraphicsItem, QWidget, QGraphicsScene, QGraphicsView, QApplication, QMenu, QRubberBand,QFileDialog
from SOMcreator import classes

import logging
import tqdm
from som_gui.qt_designs import ui_GraphWindow
from ..data import constants
from ..icons import get_icon, get_reload_icon, get_search_icon
from . import ifc_mod_window

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow

from ..qt_designs import ui_model_control

class ModelControlWindow(QWidget):

    def __init__(self,main_window:MainWindow):
        def create_connections():
            self.widget.button_ifc.clicked.connect(lambda : ifc_mod_window.ifc_file_dialog(self,self.widget.line_edit_ifc))

        self.main_window = main_window
        super(ModelControlWindow, self).__init__()
        self.widget = ui_model_control.Ui_Form()
        self.widget.setupUi(self)
        self.show()
        self.setWindowTitle("Modellinformationen Einlesen")
        self.setWindowIcon(get_icon())

        self.hide_start_items()
        create_connections()

    def hide_start_items(self):
        self.widget.splitter_lists.hide()
        self.widget.progress_bar.hide()
        self.widget.button_next.hide()
        self.widget.button_last.hide()
        self.widget.label_ifc_missing.hide()

        geometry = self.geometry()
        geometry.setHeight(150)
        self.setGeometry(geometry)
