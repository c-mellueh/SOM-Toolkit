from som_gui.aggregation_window.core import window as core
from som_gui.aggregation_window import tool as aw_tool
from som_gui import tool


def connect() -> None:
    tool.MainWindow.add_action("Bauwerksstruktur",
                               lambda: core.create_window(aw_tool.Window, aw_tool.View, tool.Util, tool.Search,
                                                          tool.Popups))
    core.init_main_window(tool.Object, aw_tool.Window, tool.MainWindow)

def on_new_project() -> None:
    pass


def update_combo_box() -> None:
    core.update_combo_box(aw_tool.Window, aw_tool.View)


def combo_box_changed() -> None:
    core.combobox_changed(aw_tool.Window, aw_tool.View)


def window_paint_event() -> None:
    core.paint_event(aw_tool.Window)


def refresh_object_info_line_edit() -> None:
    core.refresh_object_info_line_edit(tool.Object, aw_tool.Window)
