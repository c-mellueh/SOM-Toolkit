from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.class_tree.ui import ClassTreeWidget
from som_gui import tool
from som_gui.core import class_info as core


def on_new_project():
    pass


def connect():
    widget: ClassTreeWidget = tool.ClassTree.get_class_tree()
    widget.itemDoubleClicked.connect(item_double_clicked)

    main_ui = tool.MainWindow.get_ui()
    main_ui.button_classes_add.clicked.connect(
        lambda: core.create_class_info_widget(
            0, tool.ClassTree, tool.ClassInfo, tool.PredefinedPropertySet, tool.Util
        )
    )


def item_double_clicked():
    core.create_class_info_widget(
        mode=1,
        class_tool=tool.ClassTree,
        class_info=tool.ClassInfo,
        predefined_property_set=tool.PredefinedPropertySet,
        util=tool.Util,
    )


def class_info_paint_event():
    core.class_info_refresh(tool.ClassTree, tool.ClassInfo)
    pass


def retranslate_ui():
    core.retranslate_ui(tool.ClassInfo)


def create_class_info_widget(mode: int):
    core.create_class_info_widget(
        mode, tool.ClassTree, tool.ClassInfo, tool.PredefinedPropertySet, tool.Util
    )
