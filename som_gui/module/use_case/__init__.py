import som_gui
from som_gui.module.use_case import ui, operator, prop, window


def register():
    som_gui.UseCaseProperties = prop.UseCaseProperties


def load_ui_triggers():
    ui.load_triggers()
