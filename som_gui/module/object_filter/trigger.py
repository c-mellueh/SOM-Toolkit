import som_gui.core.object_filter as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Datei/Objektfilter", lambda: core.open_use_case_window(tool.ObjectFilter))
    core.add_object_filter_widget(tool.ObjectFilterCompare, tool.AttributeCompare, tool.CompareWindow)


def filter_tab_object_tree_selection_changed(widget):
    core.filter_tab_object_tree_selection_changed(widget, tool.AttributeCompare, tool.ObjectFilterCompare)


def on_new_project():
    core.on_startup(tool.ObjectFilter)
