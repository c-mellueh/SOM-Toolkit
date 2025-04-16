from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QLabel

from som_gui.module.class_tree.constants import OK
import logging

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.plugins.aggregation_window import tool as aw_tool

LABEL_KEY = "abbrev_text"
LINE_EDIT_KEY = "abbreviation"


def remove_main_menu_actions(
    aggregation: Type[aw_tool.Aggregation], main_window: Type[tool.MainWindow]
):
    main_window.remove_action("menuDesite", aggregation.get_action("exportBS"))


def create_main_menu_actions(
    aggregation: Type[aw_tool.Aggregation], main_window: Type[tool.MainWindow]
):
    from som_gui.plugins.aggregation_window.module.aggregation import trigger

    open_window_action = main_window.add_action(
        "menuDesite", "Export BS", trigger.export_building_structure
    )
    aggregation.set_action("exportBS", open_window_action)
    retranslate_ui(aggregation)


def retranslate_ui(aggregation: Type[aw_tool.Aggregation]):
    action = aggregation.get_action("exportBS")
    action.setText(
        QCoreApplication.translate("Aggregation", "Export Building Structure")
    )


def deactivate(
    class_tool: Type[tool.ClassTree],
    class_info_tool: Type[tool.ClassInfo],
    aggregation: Type[aw_tool.Aggregation],
    project: Type[tool.Project],
    main_window: Type[tool.MainWindow],
):
    class_tool.remove_column_from_tree(
        main_window.get_class_tree(),
        QCoreApplication.translate("Aggregation", "Abbreviation"),
    )
    class_info_tool.remove_plugin_entry(LABEL_KEY)
    class_info_tool.remove_plugin_entry(LINE_EDIT_KEY)
    project.remove_plugin_save_function(aggregation.get_save_function_index())


def activate(
    class_tool: Type[tool.ClassTree],
    class_info_tool: Type[tool.ClassInfo],
    aggregation: Type[aw_tool.Aggregation],
    project: Type[tool.Project],
    main_window: Type[tool.MainWindow],
):
    class_tool.add_column_to_tree(
        main_window.get_class_tree(),
        lambda: QCoreApplication.translate("Aggregation", "Abbreviation"),
        -1,
        lambda o: getattr(o, "abbreviation"),
    )

    name = QCoreApplication.translate("Aggregation", "Abbreviation:")
    class_info_tool.add_plugin_entry(
        LABEL_KEY,
        "horizontal_layout_info",
        lambda *a: QLabel(name),
        -1,
        lambda *a: None,
        lambda *a: None,
        lambda *a: None,
        lambda *a: OK,
        lambda *a: None,
    )

    class_info_tool.add_plugin_entry(
        LINE_EDIT_KEY,
        "horizontal_layout_info",
        aggregation.create_ci_line_edit,
        -1,
        lambda o: o.abbreviation if o else "",
        aggregation.get_ci_text,
        aggregation.set_ci_text,
        aggregation.test_abbreviation,
        aggregation.set_class_abbreviation,
    )

    index = project.add_plugin_save_function(aggregation.trigger_save)
    aggregation.set_save_function_index(index)


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


def refresh_class_info_line_edit(
    main_window: Type[tool.MainWindow],
    class_info: Type[tool.ClassInfo],
    aggregation: Type[aw_tool.Aggregation],
):
    data_dict = class_info.generate_datadict()
    abbrev_filter = (
        main_window.get_active_class().abbreviation
        if class_info.get_mode() == 1
        else None
    )
    aggregation.class_info_line_edit_paint(data_dict, abbrev_filter)


def save_aggregations(view: Type[aw_tool.View], project: Type[tool.Project]):
    logging.info("Save Aggregations")
    proj = project.get()
    aggregations = sorted(proj.get_aggregations(filter=False), key=lambda x: x.name)
    uuid_dict = view.create_aggregation_scenes_dict(
        {ag: ag.uuid for ag in aggregations}
    )

    project.get().plugin_dict["AggregationScenes"] = uuid_dict
