from __future__ import annotations
import som_gui.core.tool
from som_gui.module.modelcheck import ui, trigger
from typing import TYPE_CHECKING
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QLayout, QWidget

if TYPE_CHECKING:
    from som_gui.module.modelcheck.prop import ModelcheckProperties


class Modelcheck(som_gui.core.tool.Modelcheck):

    @classmethod
    def get_properties(cls) -> ModelcheckProperties:
        return som_gui.ModelcheckProperties

    @classmethod
    def create_checkbox_widget(cls):
        prop = cls.get_properties()
        prop.checkbox_widget = ui.ObjectCheckWidget()
        return prop.checkbox_widget

    @classmethod
    def create_window(cls):
        prop = cls.get_properties()
        prop.active_window = ui.ModelcheckWindow()
        return prop.active_window

    @classmethod
    def connect_window(cls, window: ui.ModelcheckWindow):
        trigger.connect_window(window)

    @classmethod
    def add_splitter(cls, layout: QLayout, orientation: Qt.Orientation, widget_1: QWidget, widget_2: QWidget):
        splitter = QSplitter(orientation)
        layout.addWidget(splitter)
        splitter.addWidget(widget_1)
        splitter.addWidget(widget_2)
