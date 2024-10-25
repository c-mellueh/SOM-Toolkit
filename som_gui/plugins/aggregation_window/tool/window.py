from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import SOMcreator
import som_gui
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication
import som_gui.plugins.aggregation_window.core.tool
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.module.window import ui as ui_window
from som_gui.plugins.aggregation_window.module.window import trigger

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.window.prop import WindowProperties
    from PySide6.QtWidgets import QMenuBar, QStatusBar
    from som_gui.module.util.prop import MenuDict


class Window(som_gui.plugins.aggregation_window.core.tool.Window):

    @classmethod
    def get_properties(cls) -> WindowProperties:
        return som_gui.WindowProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def create_window(cls) -> ui_window.AggregationWindow:
        window = ui_window.AggregationWindow()
        cls.get_properties().aggregation_window = window
        return window

    @classmethod
    def connect_menu(cls, window: ui_window.AggregationWindow):
        window.ui.actionAdd_View.triggered.connect(trigger.create_new_scene)
        window.ui.actionRename_View.triggered.connect(trigger.rename_view)
        window.ui.actionDelete_current_View.triggered.connect(trigger.delete_active_scene)
        window.ui.actionFilter_View.triggered.connect(trigger.filter_scenes)
        window.ui.actionReset_Filter.triggered.connect(trigger.reset_filters)
        window.ui.actionSearch_for_Node.triggered.connect(trigger.find_aggregation)
        window.ui.actionCopy_selected_Nodes.triggered.connect(trigger.copy_selected_nodes)
        window.ui.actionPaste_Nodes.triggered.connect(trigger.paste_nodes)

    @classmethod
    def create_combobox_context_menu(cls, pos):
        menu = QMenu()
        action = QAction(QCoreApplication.translate("Aggregation", "Rename"))
        action.triggered.connect(cls.request_scene_rename)
        menu.addAction(action)
        menu.exec(cls.get_combo_box().mapToGlobal(pos))

    @classmethod
    def request_scene_rename(cls):
        trigger.request_scene_rename()

    @classmethod
    def get_combo_box(cls) -> ui_window.ComboBox:
        return cls.get_window().ui.comboBox

    @classmethod
    def get_combo_box_texts(cls) -> list[str]:
        cb = cls.get_combo_box()
        return [cb.itemText(i) for i in range(cb.count())]

    @classmethod
    def get_combo_box_text(cls) -> str:
        return cls.get_combo_box().currentText()

    @classmethod
    def get_window(cls) -> ui_window.AggregationWindow:
        return cls.get_properties().aggregation_window

    @classmethod
    def get_menu_list(cls) -> list[tuple[str, Callable]]:
        return cls.get_properties().menu_list

    @classmethod
    def set_combo_box(cls, text: str) -> None:
        combo_box = cls.get_combo_box()
        combo_box.setCurrentText(text)

    @classmethod
    def is_filter_activated(cls) -> bool:
        return cls.get_properties().filter_is_activated

    @classmethod
    def activate_filter(cls) -> None:
        cls.get_properties().filter_is_activated = True

    @classmethod
    def remove_filter(cls) -> None:
        cls.get_properties().filter_is_activated = False
        cls.set_filter_object(None)

    @classmethod
    def get_allowed_scenes(cls) -> list:
        if not cls.is_filter_activated():
            return aw_tool.View.get_all_scenes()
        return cls.get_properties().allowed_scenes

    @classmethod
    def set_allowed_scenes(cls, scene_list: list) -> None:
        cls.get_properties().allowed_scenes = scene_list

    @classmethod
    def set_filter_object(cls, obj: SOMcreator.Object | None) -> None:
        cls.get_properties().filter_object = obj

    @classmethod
    def get_status_bar(cls) -> QStatusBar:
        return cls.get_window().statusBar()

    @classmethod
    def calculate_statusbar_text(cls) -> str:
        filter_object = cls.get_properties().filter_object
        texts = list()
        if filter_object is not None:
            status_text = QCoreApplication.translate("Aggregation", "Filter by {}").format(filter_object.name)
            texts.append(status_text)
        return " | ".join(texts)
