from __future__ import annotations
from typing import Type, TYPE_CHECKING
from PySide6.QtWidgets import QLabel
from som_gui.module.object import OK

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.plugins.aggregation_window import tool as aw_tool


def init_main_window(object_tool: Type[tool.Object], aggregation: Type[aw_tool.Aggregation],
                     main_window: Type[tool.MainWindow]):
    object_tool.add_column_to_tree("Abkürzung", -1, lambda o: getattr(o, "abbreviation"))

    layout = main_window.get_object_name_horizontal_layout()
    line_edit = aggregation.create_abbreviation_line_edit(layout)
    object_tool.add_object_activate_function(lambda o: line_edit.setText(o.abbreviation))
    object_tool.add_objects_infos_add_function("abbreviation", line_edit.text)
    object_tool.oi_add_plugin_entry("abbrev_text", "horizontal_layout_info", QLabel(layout.tr("Abkürzung")), -1,
                                    lambda *a: None, lambda *a: None, lambda *a: None, lambda *a: OK, lambda *a: None)
    object_info_line_edit = aggregation.create_oi_line_edit()
    object_tool.oi_add_plugin_entry("abbreviation",
                                    "horizontal_layout_info",
                                    object_info_line_edit,
                                    -1,
                                    lambda o: o.abbreviation,
                                    object_info_line_edit.text,
                                    object_info_line_edit.setText,
                                    aggregation.test_abbreviation,
                                    aggregation.set_object_abbreviation)
    main_window.add_action("Modelle/Gruppen Generieren", lambda: aggregation.open_grouping_window(main_window.get()))


def export_building_structure(exports: Type[tool.Exports], aggregation: Type[aw_tool.Aggregation],
                              main_window: Type[tool.MainWindow],
                              project: Type[tool.Project]) -> None:
    """Exports dummy Building Structure for Desite"""
    path = exports.get_path(main_window.get(), "bs.xml")
    if path:
        aggregation.export_building_structure(project.get(), path)


def refresh_object_info_line_edit(object_tool: Type[tool.Object], aggregation: Type[aw_tool.Aggregation]):
    data_dict = object_tool.oi_get_values()
    abbrev_filter = object_tool.get_active_object().abbreviation if object_tool.oi_get_mode() == 1 else None
    aggregation.object_info_line_edit_paint(data_dict, abbrev_filter)
