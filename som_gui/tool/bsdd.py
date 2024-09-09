from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.bsdd.prop import BsddProperties
import som_gui.core.tool
import som_gui
from som_gui.module.bsdd import ui
from PySide6.QtWidgets import QWidget, QToolBox

class Bsdd(som_gui.core.tool.Bsdd):

    @classmethod
    def get_properties(cls) -> BsddProperties:
        return som_gui.BsddProperties

    @classmethod
    def get_window(cls) -> ui.Widget:
        return cls.get_properties().widget

    @classmethod
    def create_window(cls):
        widget = ui.Widget()
        cls.get_properties().widget = widget
        cls.clear_toolbox()
        cls.set_tabs(["Dictionary", "Classes", "Properties"])
        return widget

    @classmethod
    def get_toolbox(cls) -> QToolBox:
        return cls.get_window().ui.toolBox

    @classmethod
    def clear_toolbox(cls):
        tb = cls.get_toolbox()
        for index in reversed(range(tb.count())):
            widget = tb.widget(index)
            tb.removeItem(index)
            widget.deleteLater()

    @classmethod
    def set_tabs(cls, name_list: list[str]):
        for name in name_list:
            cls.get_properties().tab_names.append(name)
            widget = QWidget()
            cls.get_properties().tab_widgets.append(widget)
            cls.get_toolbox().addItem(widget, name)
        cls.get_properties().tab_widgets = [QWidget() for _ in name_list]
