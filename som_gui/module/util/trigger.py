from som_gui.core import util as core
from som_gui import tool
def connect():
    pass


def on_new_project():
    pass


def fileselector_clicked(widget):
    core.filesector_clicked(widget, tool.Util)


def paint_file_selector(widget):
    core.update_file_selector(widget)


def main_attribute_selector_created(widget):
    core.fill_main_attribute_selector(widget, tool.Util, tool.Project)
