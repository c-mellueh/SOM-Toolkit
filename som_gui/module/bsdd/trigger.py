from som_gui import tool
from som_gui.core import bsdd as core
def connect():
    core.define_dictionary_widget(tool.Bsdd)
    tool.MainWindow.add_action("Datei/Export/bsDD",
                               lambda: core.open_window(tool.Bsdd, tool.Appdata))


def retranslate_ui():
    pass
def on_new_project():
    core.reset(tool.Bsdd)


def paint_dictionary():
    core.paint_dictionary(tool.Bsdd, tool.Project)


def dict_attribute_changed(value, widget):
    core.dict_attribute_changed(value, widget, tool.Bsdd)


def path_button_clicked():
    core.export_path_requested(tool.Bsdd, tool.Popups, tool.Appdata)


def run_clicked():
    core.export_dictionary(tool.Bsdd, tool.Project, tool.Popups)
