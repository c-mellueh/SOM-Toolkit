from __future__ import annotations
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import Window, View


def create_window(window: Type[Window], view: Type[View]):
    aggregation_window = window.create_window()
    combo_box = window.create_combo_box()
    aggregation_view = view.create_view()
    window.add_widget_to_layout(combo_box)
    window.add_widget_to_layout(aggregation_view)
    aggregation_window.show()


def update_combo_box(window: Type[Window], view: Type[View]):
    combo_box = window.get_combo_box()
    if combo_box is None:
        return
    existing_texts = window.get_combo_box_texts()
    wanted_texts = view.get_scene_names()
    new_texts = set(wanted_texts).difference(set(existing_texts))
    if new_texts:
        combo_box.addItems(sorted(new_texts))
        combo_box.model().sort(0, Qt.AscendingOrder)
