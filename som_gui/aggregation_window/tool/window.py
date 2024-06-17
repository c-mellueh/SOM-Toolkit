from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from PySide6.QtWidgets import QHBoxLayout, QLineEdit
import SOMcreator
import som_gui
import som_gui.aggregation_window.core.tool
from som_gui.module.object import OK
from som_gui.aggregation_window import tool as aw_tool
from som_gui.aggregation_window.module.window import ui as ui_window
from som_gui import tool
from som_gui.windows import grouping_window
if TYPE_CHECKING:
    from som_gui.aggregation_window.module.window.prop import WindowProperties
    from PySide6.QtWidgets import QMenuBar, QStatusBar
    from som_gui.module.util.prop import MenuDict

ABBREV_ISSUE = 2


class Window(som_gui.aggregation_window.core.tool.Window):
    @classmethod
    def open_grouping_window(cls, parent_window):
        if cls.get_properties().grouping_window is None:
            cls.get_properties().grouping_window = grouping_window.GroupingWindow(parent_window)
        else:
            cls.get_properties().grouping_window.show()


    @classmethod
    def set_object_abbreviation(cls, obj: SOMcreator.Object, abbreviation: str):
        obj.abbreviation = abbreviation

    @classmethod
    def test_abbreviation(cls, abbreviation: str, obj: SOMcreator.Object) -> int:
        ignore_text = obj.abbreviation if obj is not None else None
        if tool.Object.oi_get_mode() == 2:
            ignore_text = None
        if abbreviation is not None and not cls.is_abbreviation_allowed(abbreviation, ignore_text):
            text = u"Abkürzung existiert bereits!"
            tool.Popups.create_warning_popup(text)
            return ABBREV_ISSUE
        return OK

    @classmethod
    def oi_set_abbrev_value_color(cls, color: str):
        widget = cls.get_properties().object_info_line_edit
        widget.setStyleSheet(f"color:{color}")

    @classmethod
    def is_abbreviation_allowed(cls, abbreviation, ignore=None):
        abbreviations = cls.get_existing_abbriviations()
        if ignore is not None:
            abbreviations = list(filter(lambda a: a != ignore, abbreviations))
        if abbreviation in abbreviations:
            return False
        else:
            return True

    @classmethod
    def get_existing_abbriviations(cls) -> set[str]:
        proj = tool.Project.get()
        abbreviations = set()
        for obj in proj.get_all_objects():
            if obj.abbreviation:
                abbreviations.add(obj.abbreviation)
        return abbreviations

    @classmethod
    def object_info_line_edit_paint(cls, data_dict, abbrev_filter):
        abbreviation = data_dict["abbreviation"]
        if not cls.is_abbreviation_allowed(abbreviation, abbrev_filter):
            cls.oi_set_abbrev_value_color("red")
        else:
            cls.oi_set_abbrev_value_color("black")


    @classmethod
    def get_properties(cls) -> WindowProperties:
        return som_gui.WindowProperties

    @classmethod
    def create_oi_line_edit(cls):
        cls.get_properties().object_info_line_edit = ui_window.ObjectInfoLineEdit()
        return cls.get_properties().object_info_line_edit

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
    def add_widget_to_layout(cls, widget, *args, **kwargs) -> None:
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
    def get_menu_dict(cls) -> MenuDict:
        return cls.get_properties().menu_dict

    @classmethod
    def get_aggregation_window(cls) -> ui_window.AggregationWindow:
        return cls.get_properties().aggregation_window

    @classmethod
    def get_menu_list(cls) -> list[tuple[str, Callable]]:
        return cls.get_properties().menu_list

    @classmethod
    def set_combo_box(cls, text: str) -> None:
        combo_box = cls.get_combo_box()
        combo_box.setCurrentText(text)

    @classmethod
    def is_filter_activated(cls) -> bool:
        return cls.get_properties().filter_is_activated

    @classmethod
    def activate_filter(cls) -> None:
        cls.get_properties().filter_is_activated = True

    @classmethod
    def remove_filter(cls) -> None:
        cls.get_properties().filter_is_activated = False
        cls.set_filter_object(None)

    @classmethod
    def get_allowed_scenes(cls) -> list:
        if not cls.is_filter_activated():
            return aw_tool.View.get_all_scenes()
        return cls.get_properties().allowed_scenes

    @classmethod
    def set_allowed_scenes(cls, scene_list: list) -> None:
        cls.get_properties().allowed_scenes = scene_list

    @classmethod
    def set_filter_object(cls, obj: SOMcreator.Object | None) -> None:
        cls.get_properties().filter_object = obj

    @classmethod
    def get_status_bar(cls) -> QStatusBar:
        return cls.get_aggregation_window().statusBar()

    @classmethod
    def calculate_statusbar_text(cls) -> str:
        filter_object = cls.get_properties().filter_object
        texts = list()
        if filter_object is not None:
            texts.append(f"Filter by {filter_object.name}")
        return " | ".join(texts)
