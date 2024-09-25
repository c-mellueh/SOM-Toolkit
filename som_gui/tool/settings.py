from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import logging
from PySide6.QtWidgets import QHBoxLayout, QTabWidget, QWidget, QToolBox
import som_gui.core.tool
import som_gui
from som_gui.module.settings import ui
if TYPE_CHECKING:
    from som_gui.module.settings.prop import SettingsProperties


class Settings(som_gui.core.tool.Settings):
    @classmethod
    def get_properties(cls) -> SettingsProperties:
        return som_gui.SettingsProperties

    @classmethod
    def add_page_to_toolbox(cls, widget, page_name: str, tab_name: str, start_function: Callable,
                            accept_function: Callable):
        if tab_name not in cls.get_tab_dict():
            cls.get_properties().tab_dict[tab_name] = dict()
        if page_name not in cls.get_properties().tab_dict[tab_name]:
            cls.get_properties().tab_dict[tab_name][page_name] = list()
        cls.get_properties().tab_dict[tab_name][page_name].append(widget)

        cls.get_properties().open_functions.append(start_function)
        cls.get_properties().accept_functions.append(accept_function)

    @classmethod
    def get_widget(cls) -> ui.Widget:
        return cls.get_properties().widget

    @classmethod
    def set_widget(cls, widget: ui.Widget):
        cls.get_properties().widget = widget

    @classmethod
    def create_widget(cls) -> ui.Widget:
        widget = ui.Widget()
        for name, toolbox_dict in cls.get_tab_dict():
            tool_box = cls.create_tab(cls.get_tab_widget(), name)
            for page_name, widgets in toolbox_dict.items():
                page = QWidget()
                page.setLayout(QHBoxLayout())
                tool_box.addItem(page, page_name)
                for widget in widgets:
                    page.layout().addWidget(widget)
        return widget

    @classmethod
    def get_tab_widget(cls) -> QTabWidget:
        return cls.get_widget().tab_widget

    @classmethod
    def get_tab_dict(cls) -> dict[str, dict[str, QWidget]]:
        return cls.get_properties().tab_dict

    @classmethod
    def create_tab(cls, tab_widget: QTabWidget, tab_name: str) -> QToolBox:
        tb = QToolBox()
        tab_widget.addTab(tb, tab_name)
        return tb

    @classmethod
    def get_tab_names(cls) -> list[str]:
        return sorted(cls.get_properties().tab_dict.keys())
