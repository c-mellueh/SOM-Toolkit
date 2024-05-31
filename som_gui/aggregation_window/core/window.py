from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import Window, View


def create_window(window: Type[Window], view: Type[View]):
    aggregation_window = window.create_window()
    combo_box = window.create_combo_box()
    aggregation_view = view.create_view()
    window.add_widget_to_layout(combo_box)
    window.add_widget_to_layout(aggregation_view)
    aggregation_window.show()


def update_combo_box(window: Type[Window]):
    combo_box = window.get_combo_box()
    if combo_box is None:
        return
    combo_box.item
