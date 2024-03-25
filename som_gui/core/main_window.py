from __future__ import annotations
from typing import TYPE_CHECKING, Type

import som_gui

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Settings, Project, Popups


def close_event(project_tool: Type[Project], settings_tool: Type[Settings],
                popups_tool: Type[Popups]):
    reply = popups_tool.request_save_before_exit()
    if reply is None:  # abort Dialog
        return False
    if reply is False:  # No
        return True
    som_gui.core.project.save_clicked(project_tool, popups_tool, settings_tool)
    return True


def set_main_window(window, main_window_tool: Type[MainWindow]):
    main_window_tool.set(window)


def add_label_to_statusbar(main_window_tool: Type[MainWindow]):
    main_window_tool.create_status_label()


def create_menus(main_window_tool: Type[MainWindow]):
    menu_dict = main_window_tool.get_menu_dict()
    menu_bar = main_window_tool.get_menu_bar()
    menu_dict["menu"] = menu_bar
    main_window_tool.create_actions(menu_dict, None)


def refresh_main_window(main_window_tool: Type[MainWindow], project_tool: Type[Project]):
    status = f"{project_tool.get_project_name()} {project_tool.get_project_version()}"
    main_window_tool.set_status_bar_text(status)
    main_window_tool.set_window_title(f"SOM-Toolkit v{som_gui.__version__}")


def fill_old_menus(main_window_tool: Type[MainWindow]):
    """
    fill menus of functions / windows that aren't refactored
    """
    from som_gui.filehandling import export as fh_export
    main_window = som_gui.MainUi.window
    main_window_tool.add_action("Datei/Export/Vestra", lambda: fh_export.export_vestra_mapping(main_window))
    main_window_tool.add_action("Datei/Export/Card1", lambda: fh_export.export_card_1(main_window))
    main_window_tool.add_action("Datei/Export/Excel", lambda: fh_export.export_excel(main_window))
    main_window_tool.add_action("Datei/Export/Allplan", lambda: fh_export.export_allplan_excel(main_window))
    main_window_tool.add_action("Datei/Export/Abkürzungen", lambda: fh_export.export_desite_abbreviation(main_window))
    main_window_tool.add_action("Datei/Mappings", lambda: main_window.open_mapping_window())
    main_window_tool.add_action("Modelle/Gruppen Generieren", lambda: main_window.open_grouping_window())
    main_window_tool.add_action("Modelle/Informationen einlesen", lambda: main_window.open_attribute_import_window())
    main_window_tool.add_action("Bauwerksstruktur", lambda: main_window.open_aggregation_window())

    main_window_tool.add_action("Desite/Lesezeichen", lambda: fh_export.export_bookmarks(main_window))
    main_window_tool.add_action("Desite/Mapping Script", lambda: fh_export.export_mapping_script(main_window))
