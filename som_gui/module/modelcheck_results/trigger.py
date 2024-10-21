from som_gui.core import modelcheck_results as core
from som_gui import tool
def connect():
    pass


def last_modelcheck_finished(db_path):
    core.create_results(db_path, tool.ModelcheckResults, tool.ModelcheckWindow)

def on_new_project():
    pass


def retranslate_ui():
    pass
