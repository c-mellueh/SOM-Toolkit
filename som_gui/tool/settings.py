from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Type
import logging
from PySide6.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QToolBox, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
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
    def add_page_to_toolbox(cls, widget, page_name: str, tab_name: str, accept_function: Callable):
        if tab_name not in cls.get_tab_dict():
            cls.get_properties().tab_dict[tab_name] = dict()

        if page_name not in cls.get_properties().tab_dict[tab_name]:
            cls.get_properties().tab_dict[tab_name][page_name] = list()
        cls.get_properties().tab_dict[tab_name][page_name].append(widget)

        cls.get_properties().accept_functions.append(accept_function)

    @classmethod
    def get_widget(cls) -> ui.Dialog:
        return cls.get_properties().widget

    @classmethod
    def set_widget(cls, widget: ui.Dialog):
        cls.get_properties().widget = widget

    @classmethod
    def create_dialog(cls) -> ui.Dialog:
        settings_dialog = ui.Dialog()
        cls.set_widget(settings_dialog)
        for name, toolbox_dict in cls.get_tab_dict().items():
            tool_box = cls.create_tab(cls.get_tab_widget(), name)
            page_dict = dict()
            for page_name, widgets in toolbox_dict.items():
                page = QWidget()
                page_dict[page_name] = page
                page.setLayout(QVBoxLayout())
                tool_box.addItem(page, page_name)
                for widget in widgets:
                    page.layout().addWidget(widget())
            cls.get_properties().tab_widget_dict[name] = (tool_box, page_dict)

        return settings_dialog

    @classmethod
    def get_tab_widget(cls) -> QTabWidget:
        return cls.get_widget().tab_widget

    @classmethod
    def get_tab_dict(cls) -> dict[str, dict[str, list[Type[QWidget]]]]:
        return cls.get_properties().tab_dict

    @classmethod
    def create_tab(cls, tab_widget: QTabWidget, tab_name: str) -> QToolBox:
        tb = QToolBox()
        tab_widget.addTab(tb, tab_name)
        return tb

    @classmethod
    def get_tab_names(cls) -> list[str]:
        return sorted(cls.get_properties().tab_dict.keys())

    @classmethod
    def get_accept_functions(cls) -> list[Callable]:
        return cls.get_properties().accept_functions

    @classmethod
    def set_icon(cls, tab_name: str, page_name: str, icon: QIcon):
        if not tab_name in cls.get_properties().tab_widget_dict:
            return
        toolbox = cls.get_properties().tab_widget_dict[tab_name][0]
        if not page_name in cls.get_properties().tab_widget_dict[tab_name][1]:
            return
        page = cls.get_properties().tab_widget_dict[tab_name][1][page_name]
        toolbox.setItemIcon(toolbox.indexOf(page), icon)
