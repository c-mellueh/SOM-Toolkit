import som_gui.core.project as core
from som_gui import tool
from som_gui.module.project import ui


def connect():
    core.create_main_menu_actions(tool.Project, tool.MainWindow)

    tool.Settings.add_page_to_toolbox(ui.SettingsGeneral, "pageGeneral",
                                      lambda: core.settings_accepted(tool.Project, tool.Appdata))
    tool.Settings.add_page_to_toolbox(ui.SettingsPath, "pageProject", lambda: None)


def new_clicked():
    core.new_file_clicked(tool.Project, tool.Popups)


def open_clicked():
    core.open_file_clicked(tool.Project, tool.Appdata, tool.MainWindow, tool.Popups)


def add_clicked():
    core.add_project(tool.Project, tool.Appdata, tool.Popups, tool.MainWindow, tool.Util)


def save_clicked():
    core.save_clicked(tool.Project, tool.Popups, tool.Appdata, tool.MainWindow)


def save_as_clicked():
    core.save_as_clicked(tool.Project, tool.Popups, tool.Appdata, tool.MainWindow)


def settings_general_created(widget: ui.SettingsGeneral):
    core.settings_general_created(widget, tool.Project)


def settings_path_created(widget: ui.SettingsPath):
    core.settings_path_created(widget, tool.Project, tool.Appdata)


def retranslate_ui():
    core.retranslate_ui(tool.Project)
