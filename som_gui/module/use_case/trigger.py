from som_gui.module.use_case.prop import UseCaseProperties
from som_gui.module.use_case.ui import UseCaseWindow, load_triggers
import som_gui.core.use_case as core
from som_gui.tool.use_case import UseCase
from PySide6.QtCore import Qt, QPoint
import som_gui
from som_gui import tool
from PySide6.QtWidgets import QAbstractItemView

def menu_action_use_cases():
    prop: UseCaseProperties = som_gui.UseCaseProperties
    if not prop.use_case_window:
        prop.use_case_window = UseCaseWindow()
    prop.use_case_window.show()
    core.load_use_cases(UseCase)
    header = prop.use_case_window.widget.object_tree.header()
    header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    use_case_window = prop.use_case_window
    if not use_case_window:
        return
    object_tree = prop.use_case_window.widget.object_tree
    object_tree.expanded.connect(lambda: core.resize_tree(object_tree, UseCase))
    pset_tree = prop.use_case_window.widget.property_set_tree
    pset_tree.expanded.connect(lambda: core.resize_tree(pset_tree, UseCase))
    header = object_tree.header()
    header.customContextMenuRequested.connect(
        lambda pos: core.create_header_context_menu(pos, object_tree, UseCase, tool.Project))
    header.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
    use_case_window.widget.buttonBox.accepted.connect(lambda: core.accept_changes(UseCase))
    use_case_window.widget.buttonBox.rejected.connect(lambda: core.reject_changes(UseCase))


def on_new_project():
    core.on_startup(UseCase)
