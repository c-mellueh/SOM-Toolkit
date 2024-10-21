from som_gui import tool
from som_gui.core import exports as core
from . import ui
from PySide6.QtCore import QCoreApplication


def connect():
    core.create_main_menu_actions(tool.Exports, tool.MainWindow)
    tool.Settings.add_page_to_toolbox(lambda: core.create_settings_ui(tool.Exports, tool.Appdata), "pageExport",
                                      lambda: core.settings_accepted(tool.Exports, tool.Appdata))


def export_vestra():
    core.export_vestra_mapping(tool.Exports, tool.MainWindow, tool.Project, tool.Appdata)


def export_card1():
    core.export_card_1(tool.Exports, tool.MainWindow, tool.Project, tool.Appdata)


def export_excel():
    core.export_excel(tool.Exports, tool.MainWindow, tool.Project, tool.Appdata, tool.Popups)


def export_allplan():
    core.export_allplan_excel(tool.Exports, tool.MainWindow, tool.Project, tool.Popups, tool.Appdata)


def export_abbreviation():
    core.export_desite_abbreviation(tool.MainWindow, tool.Project, tool.Appdata, tool.Popups)


def export_bookmarks():
    core.export_bookmarks(tool.Exports, tool.MainWindow, tool.Project, tool.Popups, tool.Appdata)


def export_mapping_script():
    core.export_mapping_script(tool.Exports, tool.MainWindow, tool.Project, tool.Popups, tool.Appdata)


def retranslate_ui():
    core.retranslate_ui(tool.Exports)


def on_new_project():
    pass
