from som_gui.core import compare as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Datei/SOM-Vergleichen",
                               lambda: core.open_project_selection_window(tool.CompareWindow,
                                                                          tool.CompareProjectSelector,
                                                                          tool.Settings, tool.Project))

    core.add_attribute_compare_widget(tool.AttributeCompare, tool.CompareWindow)
    core.add_object_filter_widget(tool.ObjectFilterCompare, tool.AttributeCompare, tool.CompareWindow)

def on_new_project():
    pass


def accept_clicked():
    core.open_compare_window(tool.CompareWindow, tool.CompareProjectSelector, tool.Project, tool.Settings, tool.Popups)


def switch_button_clicked():
    core.switch_clicked(tool.CompareProjectSelector)


def project_button_clicked():
    core.project_button_clicked(tool.CompareProjectSelector, tool.Popups, tool.Settings)


def object_tree_selection_changed(widget, style: bool):
    core.object_tree_selection_changed(widget, style, tool.AttributeCompare)


def pset_tree_selection_changed(widget):
    core.pset_tree_selection_changed(widget, tool.AttributeCompare)
