from typing import Type, TYPE_CHECKING
from PySide6.QtWidgets import QLabel
from som_gui.module.object import OK

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.aggregation_window import tool as aw_tool


def init_main_window(object_tool: Type[tool.Object], aggregation: Type[aw_tool.Aggregation],
                     main_window: Type[tool.MainWindow]):
    object_tool.add_column_to_tree("Abkürzung", -1, lambda o: getattr(o, "abbreviation"))

    layout = main_window.get_object_name_horizontal_layout()
    line_edit = window.create_abbreviation_line_edit(layout)
    object_tool.add_object_activate_function(lambda o: line_edit.setText(o.abbreviation))
    object_tool.add_objects_infos_add_function("abbreviation", line_edit.text)
    object_tool.oi_add_plugin_entry("abbrev_text", "horizontal_layout_info", QLabel(layout.tr("Abkürzung")), -1,
                                    lambda *a: None, lambda *a: None, lambda *a: None, lambda *a: OK, lambda *a: None)
    object_info_line_edit = window.create_oi_line_edit()
    object_tool.oi_add_plugin_entry("abbreviation",
                                    "horizontal_layout_info",
                                    object_info_line_edit,
                                    -1,
                                    lambda o: o.abbreviation,
                                    object_info_line_edit.text,
                                    object_info_line_edit.setText,
                                    window.test_abbreviation,
                                    window.set_object_abbreviation)
    main_window.add_action("Modelle/Gruppen Generieren", lambda: main_window.open_grouping_window())
