from som_gui.module import project
import som_gui
from som_gui.module.project import ui
import som_gui.core.project as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Datei/Neu", lambda: core.new_file_clicked(tool.Project, tool.Popups))
    tool.MainWindow.add_action("Datei/Projekt Öffnen",
                               lambda: core.open_file_clicked(tool.Project, tool.Settings, tool.MainWindow,
                                                              tool.Popups))
    tool.MainWindow.add_action("Datei/Projekt Hinzufügen",
                               lambda: core.add_project(tool.Project, tool.Settings, tool.Popups, tool.MainWindow))
    tool.MainWindow.add_action("Datei/Speichern",
                               lambda: core.save_clicked(tool.Project, tool.Popups, tool.Settings, tool.MainWindow))
    tool.MainWindow.add_action("Datei/Speichern unter ...",
                               lambda: core.save_as_clicked(tool.Project, tool.Popups, tool.Settings, tool.MainWindow))
    tool.MainWindow.add_action("Datei/Einstellungen", menu_action_settings)


def menu_action_settings():
    prop: project.prop.ProjectProperties = som_gui.ProjectProperties
    prop.settings_window = ui.SettingsDialog()
    core.fill_settings_dialog(tool.Project)
    if prop.settings_window.exec():
        core.update_settings(tool.Project)
    else:
        core.reset_settings_dialog(tool.Project)


def repaint_event():
    core.repaint_settings_dialog(tool.Project)
