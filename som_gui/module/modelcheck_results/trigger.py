from som_gui import tool
from som_gui.core import modelcheck_results as core


def connect():
    pass


def last_modelcheck_finished(db_path):
    core.create_results(
        db_path, tool.ModelcheckResults, tool.ModelcheckWindow, tool.Popups
    )


def on_new_project():
    pass


def retranslate_ui():
    pass
