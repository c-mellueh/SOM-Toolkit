from som_gui.module import project
import som_gui
from som_gui.module.project import ui
import som_gui.core.project as core
from som_gui import tool


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


def menu_action_open_file():
    core.open_file_clicked(tool.Project)
