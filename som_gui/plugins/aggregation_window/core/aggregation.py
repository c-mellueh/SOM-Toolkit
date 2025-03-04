from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QLabel

from som_gui.module.class_.constants import OK

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.plugins.aggregation_window import tool as aw_tool


def create_main_menu_actions(
    aggregation: Type[aw_tool.Aggregation], main_window: Type[tool.MainWindow]
):
    from som_gui.plugins.aggregation_window.module.aggregation import trigger

    open_window_action = main_window.add_action(
        "menuDesite", "Export BS", trigger.export_building_structure
    )
    aggregation.set_action("exportBS", open_window_action)


def retranslate_ui(aggregation: Type[aw_tool.Aggregation]):
    action = aggregation.get_action("exportBS")
    action.setText(
        QCoreApplication.translate("Aggregation", "Export Building Structure")
    )


def init_main_window(
    class_tool: Type[tool.Class],
    class_info_tool: Type[tool.ClassInfo],
    aggregation: Type[aw_tool.Aggregation],
    main_window: Type[tool.MainWindow],
):
    class_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Aggregation", "Abbreviation"),
        -1,
        lambda o: getattr(o, "abbreviation"),
    )

    name = QCoreApplication.translate("Aggregation", "Abbreviation")
    class_info_tool.add_plugin_entry(
        "abbrev_text",
        "horizontal_layout_info",
        QLabel(name),
        -1,
        lambda *a: None,
        lambda *a: None,
        lambda *a: None,
        lambda *a: OK,
        lambda *a: None,
    )
    object_info_line_edit = aggregation.create_ci_line_edit()
    class_info_tool.add_plugin_entry(
        "abbreviation",
        "horizontal_layout_info",
        object_info_line_edit,
        -1,
        lambda o: o.abbreviation if o else "",
        object_info_line_edit.text,
        object_info_line_edit.setText,
        aggregation.test_abbreviation,
        aggregation.set_object_abbreviation,
    )


def export_building_structure(
    aggregation: Type[aw_tool.Aggregation],
    main_window: Type[tool.MainWindow],
    project: Type[tool.Project],
    popups: Type[tool.Popups],
) -> None:
    """Exports dummy Building Structure for Desite"""
    text = QCoreApplication.translate("Aggregation", "Building Structure-XML")
    file_format = f"{text}  (*.bs.xml);;all (*.*)"
    path = popups.get_save_path(file_format, main_window.get())
    if path:
        aggregation.export_building_structure(project.get(), path)


def refresh_object_info_line_edit(
    class_tool: Type[tool.Class],
    class_info: Type[tool.ClassInfo],
    aggregation: Type[aw_tool.Aggregation],
):
    data_dict = class_info.oi_get_values()
    abbrev_filter = (
        class_tool.get_active_class().abbreviation
        if class_info.oi_get_mode() == 1
        else None
    )
    aggregation.object_info_line_edit_paint(data_dict, abbrev_filter)


def save_aggregations(view: Type[aw_tool.View], project: Type[tool.Project]):
    proj = project.get()
    aggregations = sorted(proj.get_aggregations(filter=False), key=lambda x: x.name)
    uuid_dict = view.create_aggregation_scenes_dict(
        {ag: ag.uuid for ag in aggregations}
    )

    project.get().plugin_dict["AggregationScenes"] = uuid_dict
