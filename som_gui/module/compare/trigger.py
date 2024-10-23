from som_gui.core import compare as core
from som_gui import tool


def connect():
    core.create_main_menu_actions(tool.CompareWindow, tool.MainWindow)


def open_window():
    core.open_project_selection_window(tool.CompareWindow,
                                       tool.CompareProjectSelector,
                                       tool.Appdata, tool.Project)

def retranslate_ui():
    core.retranslate_ui(tool.CompareWindow)

def on_new_project():
    pass


def accept_clicked():
    core.open_compare_window(tool.CompareWindow, tool.CompareProjectSelector, tool.Project, tool.Appdata, tool.Popups)


def switch_button_clicked():
    core.switch_clicked(tool.CompareProjectSelector)


def project_button_clicked():
    core.project_button_clicked(tool.CompareProjectSelector, tool.Popups, tool.Appdata)


def object_tree_selection_changed(widget, ):
    core.object_tree_selection_changed(widget, tool.AttributeCompare)


def pset_tree_selection_changed(widget):
    core.pset_tree_selection_changed(widget, tool.AttributeCompare)


def draw_branches(tree, painter, rect, index):
    return core.draw_tree_branch(tree, painter, rect, index, tool.AttributeCompare)


def download_clicked():
    core.download_changelog(tool.CompareWindow, tool.Popups, tool.Appdata)
