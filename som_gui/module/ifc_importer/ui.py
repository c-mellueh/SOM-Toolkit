import os

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import QRunnable, Signal, QObject
from .widget import Ui_Form
import ifcopenshell


class IfcImportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Ui_Form()
        self.widget.setupUi(self)


from time import sleep
import random


class IfcImportRunner(QRunnable):
    def __init__(self, path: os.PathLike | str, status_label: QLabel):
        super(IfcImportRunner, self).__init__()
        self.path = path
        self.ifc: ifcopenshell.file | None = None
        self.signaller = Signaller()
        self.status_label = status_label

    def run(self):
        self.signaller.started.emit()
        self.ifc = ifcopenshell.open(self.path, should_stream=True)
        self.signaller.finished.emit()


class Signaller(QObject):
    started = Signal()
    finished = Signal()
