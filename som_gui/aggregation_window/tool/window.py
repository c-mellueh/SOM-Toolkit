from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator
from PySide6.QtGui import QShortcut, QKeySequence

import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.window import ui as ui_window
import som_gui
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.window.prop import WindowProperties
    from PySide6.QtWidgets import QMenuBar


class Window(som_gui.aggregation_window.core.tool.Window):

    @classmethod
    def get_properties(cls) -> WindowProperties:
        return som_gui.WindowProperties

    @classmethod
    def create_window(cls) -> ui_window.AggregationWindow:
        window = ui_window.AggregationWindow()
        cls.get_properties().aggregation_window = window
        return window

    @classmethod
    def create_combo_box(cls) -> ui_window.ComboBox:
        cls.get_properties().combo_box = ui_window.ComboBox()
        return cls.get_properties().combo_box

    @classmethod
    def add_widget_to_layout(cls, widget, *args, **kwargs):
        window = cls.get_properties().aggregation_window
        if window is None:
            return
        window.central_layout.addWidget(widget, *args, **kwargs)

    @classmethod
    def get_combo_box(cls) -> ui_window.ComboBox:
        return cls.get_properties().combo_box

    @classmethod
    def get_combo_box_texts(cls) -> list[str]:
        cb = cls.get_combo_box()
        return [cb.itemText(i) for i in range(cb.count())]

    @classmethod
    def get_combo_box_text(cls) -> str:
        return cls.get_combo_box().currentText()

    @classmethod
    def get_menu_bar(cls) -> QMenuBar:
        return cls.get_properties().aggregation_window.menuBar()

    @classmethod
    def get_menu_dict(cls):
        return cls.get_properties().menu_dict

    @classmethod
    def get_aggregation_window(cls) -> ui_window.AggregationWindow:
        return cls.get_properties().aggregation_window

    @classmethod
    def get_menu_list(cls):
        return cls.get_properties().menu_list

    @classmethod
    def set_combo_box(cls, text: str):
        combo_box = cls.get_combo_box()
        combo_box.setCurrentText(text)

    @classmethod
    def filter_is_activated(cls):
        return cls.get_properties().filter_is_activated

    @classmethod
    def activate_filter(cls):
        cls.get_properties().filter_is_activated = True

    @classmethod
    def deactivate_filter(cls):
        cls.get_properties().filter_is_activated = False
        cls.set_filter_object(None)

    @classmethod
    def get_allowed_scenes(cls) -> list:
        if not cls.filter_is_activated():
            return aw_tool.View.get_all_scenes()
        return cls.get_properties().allowed_scenes

    @classmethod
    def set_allowed_scenes(cls, scene_list: list):
        cls.get_properties().allowed_scenes = scene_list

    @classmethod
    def set_filter_object(cls, obj: SOMcreator.Object | None):
        cls.get_properties().filter_object = obj

    @classmethod
    def get_status_bar(cls):
        return cls.get_aggregation_window().statusBar()

    @classmethod
    def calculate_statusbar_text(cls):
        filter_object = cls.get_properties().filter_object
        texts = list()
        if filter_object is not None:
            texts.append(f"Filter by {filter_object.name}")
        return " | ".join(texts)
