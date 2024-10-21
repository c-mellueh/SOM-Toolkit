from som_gui.plugins.aggregation_window.core import window as core
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui import tool


def connect() -> None:
    tool.MainWindow.add_action("Bauwerksstruktur",
                               lambda: core.create_window(aw_tool.Window, aw_tool.View, tool.Util, tool.Search,
                                                          tool.Popups))
def on_new_project() -> None:
    pass


def update_combo_box() -> None:
    core.update_combo_box(aw_tool.Window, aw_tool.View)


def combo_box_changed() -> None:
    core.combobox_changed(aw_tool.Window, aw_tool.View)


def window_paint_event() -> None:
    core.paint_event(aw_tool.Window)


def request_scene_rename():
    core.request_scene_rename(aw_tool.Window, aw_tool.View, tool.Popups, )


def retranslate_ui():
    pass
