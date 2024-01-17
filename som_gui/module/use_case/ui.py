from __future__ import annotations
from som_gui import MainUi
import som_gui.module.use_case as use_case
from som_gui import icons
from som_gui.core import use_case as core
from som_gui.tool.use_case import UseCase
from som_gui.tool.project import Project
from PySide6.QtWidgets import QTreeView, QWidget, QAbstractItemView
from PySide6.QtGui import QMouseEvent
import som_gui


class UseCaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = use_case.window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())


def load_triggers():
    prop: use_case.prop.UseCaseProperties = som_gui.UseCaseProperties
    MainUi.ui.action_use_cases.triggered.connect(use_case.trigger.menu_action_use_cases)
    use_case_window = prop.use_case_window

    if not use_case_window:
        return
    object_tree = prop.use_case_window.widget.object_tree
    object_tree.expanded.connect(lambda: core.resize_tree(object_tree, UseCase))
    pset_tree = prop.use_case_window.widget.property_set_tree
    pset_tree.expanded.connect(lambda: core.resize_tree(pset_tree, UseCase))
    header =object_tree.header()
    header.customContextMenuRequested.connect(lambda pos: core.create_header_context_menu(pos,object_tree,UseCase,Project))
    header.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
    use_case_window.widget.buttonBox.accepted.connect(lambda: core.accept_changes(UseCase))
    use_case_window.widget.buttonBox.rejected.connect(lambda: core.reject_changes(UseCase))

class ObjectTreeView(QTreeView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.is_already_pressed = False
        self.check_state = None
        self.title_count = 2

    def paintEvent(self, event):
        super().paintEvent(event)
        core.refresh_object_tree(UseCase, Project)

    def mousePressEvent(self, event: QMouseEvent):
        index = self.indexAt(event.pos())
        if core.tree_mouse_press_event(index, UseCase):
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        core.tree_mouse_move_event(self.indexAt(event.pos()), UseCase)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        core.tree_mouse_release_event(index, UseCase)
