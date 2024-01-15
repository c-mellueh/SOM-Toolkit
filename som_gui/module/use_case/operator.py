from som_gui.module.use_case.prop import UseCaseProperties
from som_gui.module.use_case.ui import UseCaseWindow


def menu_action_use_cases():
    if not UseCaseProperties.use_case_window:
        UseCaseProperties.use_case_window = UseCaseWindow()
    UseCaseProperties.use_case_window.show()
