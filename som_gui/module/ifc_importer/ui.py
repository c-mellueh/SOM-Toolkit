import os

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import QRunnable, Signal, QObject
from . import qt
import ifcopenshell


class IfcImportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = qt.Ui_Form()
        self.widget.setupUi(self)


from time import sleep
import random



