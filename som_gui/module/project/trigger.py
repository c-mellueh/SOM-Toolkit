from som_gui.module import project
import som_gui
from som_gui.module.project import ui
import som_gui.core.project as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Datei/Neu", lambda: core.new_file_clicked(tool.Project, tool.Popups))
    tool.MainWindow.add_action("Datei/Projekt Öffnen",
                               lambda: core.open_file_clicked(tool.Project, tool.Appdata, tool.MainWindow,
                                                              tool.Popups))
    tool.MainWindow.add_action("Datei/Projekt Hinzufügen",
                               lambda: core.add_project(tool.Project, tool.Appdata, tool.Popups, tool.MainWindow))
    tool.MainWindow.add_action("Datei/Speichern",
                               lambda: core.save_clicked(tool.Project, tool.Popups, tool.Appdata, tool.MainWindow))
    tool.MainWindow.add_action("Datei/Speichern unter ...",
                               lambda: core.save_as_clicked(tool.Project, tool.Popups, tool.Appdata, tool.MainWindow))

    tool.Settings.add_page_to_toolbox(ui.SettingsGeneral, "pageGeneral",
                                      lambda: core.settings_accepted(tool.Project, tool.Appdata))
    tool.Settings.add_page_to_toolbox(ui.SettingsPath, "pageProject", lambda: None)



def settings_general_created(widget: ui.SettingsGeneral):
    core.settings_general_created(widget, tool.Project)


def settings_path_created(widget: ui.SettingsPath):
    core.settings_path_created(widget, tool.Project, tool.Appdata)


def retranslate_ui():
    pass
