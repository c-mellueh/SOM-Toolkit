from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.class_.ui import ObjectTreeWidget
from som_gui import tool
from som_gui.core import class_info as core


def on_new_project():
    pass


def connect():
    widget: ObjectTreeWidget = tool.Class.get_class_tree()
    widget.itemDoubleClicked.connect(item_double_clicked)

    main_ui = tool.MainWindow.get_ui()
    main_ui.button_objects_add.clicked.connect(
        lambda: core.create_class_info_widget(
            0,tool.Class, tool.ClassInfo, tool.PredefinedPropertySet, tool.Util
        )
    )


def item_double_clicked():
    core.create_class_info_widget(
        mode=1,
        class_tool= tool.Class,
        class_info=tool.ClassInfo,
        predefined_property_set=tool.PredefinedPropertySet,
        util=tool.Util,
    )


def object_info_paint_event():
    core.class_info_refresh(tool.Class,tool.ClassInfo)
    pass


def retranslate_ui():
    core.retranslate_ui(tool.ClassInfo)


def create_object_info_widget(mode: int):
    core.create_class_info_widget(
        mode,tool.Class,  tool.ClassInfo, tool.PredefinedPropertySet, tool.Util
    )
