import som_gui
from . import prop, trigger


def register():
    som_gui.ViewProperties = prop.ViewProperties()


def activate():
    trigger.activate()

def deactivate():
    trigger.deactivate()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
