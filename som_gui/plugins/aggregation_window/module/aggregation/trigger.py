from som_gui import tool
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.core import aggregation as core


def activate():
    core.activate(
        tool.ClassTree,
        tool.ClassInfo,
        aw_tool.Aggregation,
        tool.Project,
        tool.MainWindow,
    )
    core.create_main_menu_actions(aw_tool.Aggregation, tool.MainWindow)


def deactivate():
    core.deactivate(
        tool.ClassTree,
        tool.ClassInfo,
        aw_tool.Aggregation,
        tool.Project,
        tool.MainWindow,
    )
    core.remove_main_menu_actions(aw_tool.Aggregation, tool.MainWindow)


def export_building_structure():
    core.export_building_structure(
        aw_tool.Aggregation, tool.MainWindow, tool.Project, tool.Popups
    )


def on_new_project():
    pass


def refresh_class_info_line_edit() -> None:
    core.refresh_class_info_line_edit(
        tool.MainWindow, tool.ClassInfo, aw_tool.Aggregation
    )


def retranslate_ui():
    core.retranslate_ui(aw_tool.Aggregation)


def save_aggregations():
    core.save_aggregations(aw_tool.View, tool.Project)
