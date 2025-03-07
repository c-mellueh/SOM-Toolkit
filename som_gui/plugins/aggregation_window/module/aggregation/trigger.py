from som_gui import tool
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.core import aggregation as core


def connect():
    core.init_main_window(tool.Class,tool.ClassInfo, aw_tool.Aggregation, tool.MainWindow)
    tool.Project.add_plugin_save_function(
        lambda: core.save_aggregations(aw_tool.View, tool.Project)
    )
    core.create_main_menu_actions(aw_tool.Aggregation, tool.MainWindow)


def export_building_structure():
    core.export_building_structure(
        aw_tool.Aggregation, tool.MainWindow, tool.Project, tool.Popups
    )


def on_new_project():
    pass


def refresh_object_info_line_edit() -> None:
    core.refresh_object_info_line_edit(tool.Class,tool.ClassInfo, aw_tool.Aggregation)


def retranslate_ui():
    core.retranslate_ui(aw_tool.Aggregation)

def on_deactivation():
    core.deactivate(tool.Class,aw_tool.Aggregation,tool.MainWindow)