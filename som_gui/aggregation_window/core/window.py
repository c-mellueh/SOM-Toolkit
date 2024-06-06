from __future__ import annotations
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import Window, View, Node
    from som_gui import tool


def create_window(window: Type[Window], view: Type[View], util: Type[tool.Util]):
    if window.get_aggregation_window() is not None:
        aggregation_window = window.get_aggregation_window()
        aggregation_window.show()
        return

    aggregation_window = window.create_window()
    combo_box = window.create_combo_box()
    aggregation_view = view.create_view()
    window.add_widget_to_layout(combo_box)
    window.add_widget_to_layout(aggregation_view)
    menu_list = window.get_menu_list()
    menu_list.append(["Ansicht/Ansichtig hinzufügen", lambda: view.create_scene("Undefined")])
    menu_list.append(["Ansicht/Aktuelle Ansicht löschen", lambda: view.delete_scene(view.get_active_scene())])
    menu_list.append(["Ansicht/Ansicht Filtern", lambda: view.filter_scenes()])
    menu_list.append(["Ansicht/Filter Zurücksetzen", lambda: view.reset_filter()])
    menu_list.append(["Aggregation/Aggregation finden", lambda: view.search_node()])
    menu_bar = window.get_menu_bar()
    menu_dict = window.get_menu_dict()
    menu_dict["menu"] = menu_bar
    for action, function in menu_list:
        util.add_action(menu_bar, menu_dict, action, function)
    util.create_actions(menu_dict, None)
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


def combobox_changed(window: Type[Window], view: Type[View]):
    text = window.get_combo_box_text()
    scene = view.get_scene_by_name(text)
    if scene is None:
        scene = view.create_scene("Undefined")
    view.activate_scene(scene)
