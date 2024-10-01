import som_gui.core.object_filter as core
from som_gui import tool
from . import ui, constants

def connect():
    tool.MainWindow.add_action("Bearbeiten/Anwendungsfall \\ Leistungsphase",
                               lambda: core.open_window(tool.ObjectFilter, tool.Project))
    core.add_compare_widget(tool.ObjectFilterCompare, tool.AttributeCompare, tool.CompareWindow)
    tool.Settings.add_page_to_toolbox(ui.SettingsWidget, constants.SETTINGS_TAB_NAME, constants.SETTINGS_PAGE_NAME,
                                      lambda: core.settings_accepted(tool.ObjectFilter, tool.Project, tool.Popups))


def refresh_object_tree():
    core.refresh_object_tree(tool.ObjectFilter, tool.Project)

def filter_tab_object_tree_selection_changed(widget):
    core.filter_tab_object_tree_selection_changed(widget, tool.AttributeCompare, tool.ObjectFilterCompare)


def on_new_project():
    core.on_startup(tool.ObjectFilter, tool.Project)


def settings_widget_created(widget: ui.SettingsWidget):
    core.settings_widget_created(widget, tool.ObjectFilter, tool.Project)


def settings_combobox_changed():
    core.settings_combobox_changed(tool.ObjectFilter, tool.Project, tool.Util)
