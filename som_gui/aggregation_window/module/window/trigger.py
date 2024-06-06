from som_gui.aggregation_window.core import window as core
from som_gui.aggregation_window import tool as aw_tool
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Test",
                               lambda: core.create_window(aw_tool.Window, aw_tool.View, tool.Util))


def update_combo_box():
    core.update_combo_box(aw_tool.Window, aw_tool.View)


def combo_box_changed():
    core.combobox_changed(aw_tool.Window, aw_tool.View)


def on_new_project():
    pass
