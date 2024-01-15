from som_gui import MainUi
from som_gui.qt_designs import ui_project_phase_window
from PySide6.QtWidgets import QWidget
import som_gui.module.use_case as use_case


class UseCaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)


def load_triggers():
    MainUi.ui.action_use_cases.triggered.connect(
        use_case.operator.menu_action_use_cases
    )
