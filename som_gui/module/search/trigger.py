from som_gui import tool
from som_gui.core import search as core


def connect():
    pass


def on_new_project():
    pass


def refresh_window():
    core.refresh_search_window(tool.Search)


def retranslate_ui():
    core.retranslate_ui(tool.Search)
