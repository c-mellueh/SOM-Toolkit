import som_gui.core.object_filter as core
from som_gui import tool
from . import ui

def connect():
    tool.MainWindow.add_action("Bearbeiten/Objektfilter", lambda: core.open_use_case_window(tool.ObjectFilter))
    core.add_object_filter_widget(tool.ObjectFilterCompare, tool.AttributeCompare, tool.CompareWindow)
    tool.Settings.add_page_to_toolbox(ui.SettingsWidget, "Filter", "General",
                                      lambda: core.settings_accepted(tool.ObjectFilter))

def filter_tab_object_tree_selection_changed(widget):
    core.filter_tab_object_tree_selection_changed(widget, tool.AttributeCompare, tool.ObjectFilterCompare)


def on_new_project():
    core.on_startup(tool.ObjectFilter)


def settings_widget_created(widget: ui.SettingsWidget):
    core.settings_widget_created(widget, tool.ObjectFilter)
