from som_gui import tool
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.core import window as core


def activate() -> None:
    core.activate(aw_tool.Window, tool.MainWindow)


def deactivate() -> None:
    core.remove_main_menu_actions(aw_tool.Window, tool.MainWindow)


def open_window():
    core.create_window(aw_tool.Window, aw_tool.View)


def on_new_project() -> None:
    core.reset(aw_tool.Window)


def update_combo_box() -> None:
    core.update_combo_box(aw_tool.Window, aw_tool.View)


def combo_box_changed() -> None:
    core.combobox_changed(aw_tool.Window, aw_tool.View)


def window_paint_event() -> None:
    core.paint_event(aw_tool.Window)


def request_scene_rename():
    core.request_scene_rename(
        aw_tool.Window,
        aw_tool.View,
        tool.Popups,
    )


def retranslate_ui():
    core.retranslate_ui(aw_tool.Window, tool.Util)


def create_new_scene():
    core.create_new_scene(aw_tool.Window, aw_tool.View)


def rename_view():
    core.request_scene_rename(aw_tool.Window, aw_tool.View, tool.Popups)


def delete_active_scene():
    core.delete_active_scene(aw_tool.Window, aw_tool.View)


def filter_scenes():
    core.filter_scenes(
        aw_tool.Window, aw_tool.View, tool.Search, tool.Popups, tool.Project
    )


def reset_filters():
    core.remove_filter(aw_tool.Window)


def find_aggregation():
    core.search_aggregation(aw_tool.View, tool.Search, tool.Popups, tool.Project)


def copy_selected_nodes():
    core.copy_selected_nodes(aw_tool.View)


def paste_nodes():
    core.paste_nodes(aw_tool.View)
