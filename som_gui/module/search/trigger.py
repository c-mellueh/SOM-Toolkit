from som_gui import tool
from som_gui.core import search as core


def connect():
    core.connect_signals(tool.Search)


def on_new_project():
    pass


def refresh_window(dialog):
    core.update_filter_table(dialog,tool.Search)

def item_double_clicked(dialog):
    core.save_selected_element(dialog, tool.Search)


def retranslate_ui():
    core.retranslate_ui(tool.Search)

def set_strict_state(state:bool):
    core.set_strict_state(state,tool.Appdata)