from som_gui.module.use_case.prop import UseCaseProperties
from som_gui.module.use_case.ui import UseCaseWindow
import som_gui.core.use_case as core
from som_gui.tool.use_case import UseCase
from som_gui.tool.project import Project


def menu_action_use_cases():
    if not UseCaseProperties.use_case_window:
        UseCaseProperties.use_case_window = UseCaseWindow()
    UseCaseProperties.use_case_window.show()
    core.load_use_cases(UseCase)


def refresh_object_tree():
    core.load_headers(UseCase)
    core.load_objects(UseCase, Project)
