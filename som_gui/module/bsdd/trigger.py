from som_gui import tool
from som_gui.core import bsdd as core


def connect():
    core.define_dictionary_widget(tool.Bsdd)
    core.create_main_menu_actions(tool.Bsdd, tool.MainWindow)


def open_window():
    core.open_window(tool.Bsdd, tool.Appdata)


def retranslate_ui():
    core.retranslate_ui(tool.Bsdd, tool.Util)


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
