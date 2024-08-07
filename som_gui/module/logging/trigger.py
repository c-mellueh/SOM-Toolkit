from som_gui.core import logging as core
from som_gui import tool


def connect():
    core.create_logger(tool.Logging, tool.Util, tool.MainWindow)


def on_new_project():
    pass
