from som_gui.plugins.aggregation_window.core import aggregation as core
from som_gui import tool
from som_gui.plugins.aggregation_window import tool as aw_tool


def connect():
    core.init_main_window(tool.Object, aw_tool.Aggregation, tool.MainWindow)
    tool.MainWindow.add_action("Desite/Bauwerksstruktur exportieren",
                               lambda: core.export_building_structure(tool.Exports, aw_tool.Aggregation,
                                                                      tool.MainWindow, tool.Project))


def on_new_project():
    pass


def refresh_object_info_line_edit() -> None:
    core.refresh_object_info_line_edit(tool.Object, aw_tool.Aggregation)
