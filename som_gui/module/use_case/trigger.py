from som_gui.module.use_case.prop import UseCaseProperties
from som_gui.module.use_case.ui import UseCaseWindow, load_triggers
import som_gui.core.use_case as core
from som_gui.tool.use_case import UseCase
from PySide6.QtCore import Qt, QPoint

def menu_action_use_cases():
    if not UseCaseProperties.use_case_window:
        UseCaseProperties.use_case_window = UseCaseWindow()
        load_triggers()
    UseCaseProperties.use_case_window.show()
    core.load_use_cases(UseCase)
    header = UseCaseProperties.use_case_window.widget.object_tree.header()
    header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)


def header_context_menu_called(pos:QPoint):
    pass
