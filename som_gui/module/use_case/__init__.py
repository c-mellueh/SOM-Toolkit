import som_gui
from . import ui, operator, prop


def register():
    som_gui.UseCaseProperties = prop.UseCaseProperties
