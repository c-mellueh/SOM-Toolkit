from __future__ import annotations

import os
from typing import Callable, TYPE_CHECKING

from PySide6.QtCore import QRunnable, QThreadPool, Qt
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialogButtonBox, QLabel, QMenu, QTreeView, QLayoutItem

import SOMcreator
import som_gui.core.tool
from som_gui import tool
from som_gui.module.modelcheck.constants import ISSUE_PATH
from som_gui.module.modelcheck_window import trigger, ui
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.tool.ifc_importer import IfcImportRunner
from som_gui.module.util import ui as util_ui

if TYPE_CHECKING:
    from som_gui.module.modelcheck_window.prop import ModelcheckWindowProperties
    from som_gui.tool.modelcheck import ModelcheckRunner


class ModelcheckWindow(som_gui.core.tool.ModelcheckWindow):
    @classmethod
    def get_properties(cls) -> ModelcheckWindowProperties:
        return som_gui.ModelcheckWindowProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def connect_class_tree(cls, tree_widget: ui.ClassTree):
        prop = cls.get_properties()
        if prop.class_tree_model is None:
            prop.class_tree_model = tree_widget.model()
            prop.class_tree_selection_model = tree_widget.selectionModel()
        else:
            tree_widget.setModel(prop.class_tree_model)
        model: QStandardItemModel = tree_widget.model()
        model.itemChanged.connect(lambda item: trigger.class_checkstate_changed(item))
        tree_widget.selectionModel().selectionChanged.connect(
            lambda: trigger.class_selection_changed(tree_widget.selectionModel())
        )
        tree_widget.customContextMenuRequested.connect(
            lambda pos: trigger.class_tree_context_menu_requested(pos, tree_widget)
        )

    @classmethod
    def connect_pset_tree(self, tree_widget: ui.PsetTree):

        tree_widget.model().itemChanged.connect(trigger.pset_checkstate_changed)
        tree_widget.customContextMenuRequested.connect(
            lambda pos: trigger.pset_context_menu_requested(pos, tree_widget)
        )

    @classmethod
    def create_context_menu(
        cls,
        pos,
        funcion_list: list[list[str, Callable]],
        widget: ui.ClassTree | ui.PsetTree,
    ):
        global_pos = widget.viewport().mapToGlobal(pos)
        menu = QMenu()
        actions = list()
        for function_name, function in funcion_list:
            actions.append(QAction(function_name))
            menu.addAction(actions[-1])
            actions[-1].triggered.connect(function)
        menu.exec(global_pos)

    @classmethod
    def expand_selection(cls, widget: ui.ClassTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            widget.expand(index)

    @classmethod
    def collapse_selection(cls, widget: ui.ClassTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            widget.collapse(index)

    @classmethod
    def check_selection(cls, widget: ui.ClassTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            if index.column() != 0:
                continue
            widget.model().setData(
                index, Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole
            )

    @classmethod
    def uncheck_selection(cls, widget: ui.ClassTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            if index.column() != 0:
                continue
            widget.model().setData(
                index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole
            )

    @classmethod
    def resize_class_tree(cls, tree):
        tree.resizeColumnToContents(0)

    @classmethod
    def get_selected_items(cls, widget: ui.ClassTree | ui.PsetTree):
        return [i.data(CLASS_REFERENCE) for i in widget.selectedIndexes()]

    @classmethod
    def is_initial_paint(cls):
        if cls.get_properties().initial_paint:
            cls.get_properties().initial_paint = False
            return True
        return False

    @classmethod
    def show_buttons(cls, buttons):
        cls.get_window().ui.buttonBox.setStandardButtons(buttons)

    @classmethod
    def reset_butons(cls):
        cls.show_buttons(
            QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.Cancel
        )
        cls.get_window().ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply)

    @classmethod
    def modelcheck_is_running(cls):
        return cls.get_modelcheck_threadpool().activeThreadCount() > 0

    @classmethod
    def connect_ifc_import_runner(cls, runner: IfcImportRunner):
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def connect_modelcheck_runner(cls, runner: QRunnable):
        trigger.connect_modelcheck_runner(runner)

    @classmethod
    def create_import_runner(cls, progress_bar, ifc_import_path: str):
        runner = tool.IfcImporter.create_runner(progress_bar, ifc_import_path)
        cls.get_properties().ifc_import_runners.append(runner)
        return runner

    @classmethod
    def destroy_import_runner(cls, runner: QRunnable):
        cls.get_properties().ifc_import_runners.remove(runner)

    @classmethod
    def check_export_path(cls, export_path):
        export_folder_path = os.path.dirname(export_path)
        if not os.path.isdir(export_folder_path):
            tool.Popups.create_folder_dne_warning(export_folder_path)
            return False
        return True

    @classmethod
    def set_progress(cls, runner: ModelcheckRunner, value: int):
        runner.signaller.progress.emit(value)

    @classmethod
    def set_status(cls, runner: ModelcheckRunner, status: str):
        runner.signaller.status.emit(status)

    @classmethod
    def read_inputs(cls):
        window = cls.get_window()
        ifc_paths = tool.Util.get_path_from_fileselector(window.ui.widget_import)
        export_path = tool.Util.get_path_from_fileselector(window.ui.widget_export)[0]
        main_pset, main_property = tool.Util.get_property(
            window.ui.main_property_widget
        )
        return ifc_paths, export_path, main_pset, main_property

    @classmethod
    def get_modelcheck_threadpool(cls):
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def set_pset_tree_title(cls, text: str):
        prop = cls.get_properties()
        prop.class_label.setText(text)

    @classmethod
    def show_pset_tree_title(cls, show: bool):
        cls.get_properties().class_label.setVisible(show)

    @classmethod
    def set_selected_class(cls, som_class: SOMcreator.SOMClass):
        prop = cls.get_properties()
        prop.selected_class = som_class

    @classmethod
    def get_selected_class(cls) -> SOMcreator.SOMClass | None:
        return cls.get_properties().selected_class

    @classmethod
    def get_class_tree(cls):
        return cls.get_properties().class_tree

    @classmethod
    def get_pset_tree(cls):
        prop = cls.get_properties()
        return prop.property_set_tree

    @classmethod
    def get_item_checkstate_dict(cls):
        """
        returns item checkstate in TreeView
        """
        prop = cls.get_properties()
        data_dict = dict()
        if not prop.check_state_dict:
            for som_class in tool.Project.get().get_classes(filter=True):
                data_dict[som_class] = True
                for property_set in som_class.get_property_sets(filter=True):
                    data_dict[property_set] = True
                    for som_property in property_set.get_properties(filter=True):
                        data_dict[som_property] = True
            prop.check_state_dict = data_dict
        return prop.check_state_dict

    @classmethod
    def get_item_check_state(
        cls,
        item: SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty,
    ) -> Qt.CheckState:
        cd = cls.get_item_checkstate_dict()
        if cd.get(item) is None:
            cd[item] = True
        check_state = Qt.CheckState.Checked if cd[item] else Qt.CheckState.Unchecked
        return check_state

    @classmethod
    def set_item_check_state(
        cls,
        item: SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty,
        cs: Qt.CheckState,
    ) -> None:
        cs = True if cs == Qt.CheckState.Checked else False
        cd = cls.get_item_checkstate_dict()
        cd[item] = cs

    @classmethod
    def autofill_export_path(cls):
        export_path = tool.Appdata.get_path(ISSUE_PATH)
        if export_path:
            cls.get_properties().export_line_edit.setText(export_path)

    @classmethod
    def is_window_allready_build(cls):
        return bool(cls.get_properties().active_window)

    @classmethod
    def get_window(cls) -> ui.ModelcheckWindow:
        return cls.get_properties().active_window

    @classmethod
    def create_window(cls):
        prop = cls.get_properties()
        window = ui.ModelcheckWindow()
        prop.active_window = window
        prop.property_set_tree = window.ui.property_set_tree
        prop.class_tree = window.ui.class_tree
        prop.class_label = window.ui.label_class
        return prop.active_window

    @classmethod
    def close_window(cls):
        cls.get_properties().active_window.hide()

    @classmethod
    def connect_buttons(cls):
        bb = cls.get_window().ui.buttonBox
        bb.clicked.connect(trigger.button_box_clicked)

    @classmethod
    def create_class_tree_row(cls, som_class: SOMcreator.SOMClass):
        item_list = [
            QStandardItem(som_class.name),
            QStandardItem(som_class.ident_value),
        ]
        item_list[0].setFlags(
            item_list[0].flags()
            | Qt.ItemFlag.ItemIsUserCheckable
            | Qt.ItemFlag.ItemIsSelectable
        )
        item_list[0].setCheckable(True)
        item_list[0].setCheckState(Qt.CheckState.Checked)
        [i.setData(som_class, CLASS_REFERENCE) for i in item_list]
        return item_list

    @classmethod
    def update_class_tree_row(cls, parent_item: QStandardItem, row_index):
        items = [
            parent_item.child(row_index, col)
            for col in range(parent_item.columnCount())
        ]
        som_class:SOMcreator.SOMClass = items[0].data(CLASS_REFERENCE)
        texts = [som_class.name, som_class.ident_value]

        for column, text in enumerate(texts):
            if items[column].text() != text:
                items[column].setText(text)

        cs = cls.get_item_check_state(items[0].data(CLASS_REFERENCE))
        if items[0].checkState() != cs:
            items[0].setCheckState(cs)

        enabled = (
            True
            if parent_item.isEnabled()
            and parent_item.checkState() == Qt.CheckState.Checked
            else False
        )
        if parent_item == parent_item.model().invisibleRootItem():
            enabled = True

        for item in items:
            item.setEnabled(enabled)
        return items[0], som_class

    @classmethod
    def fill_class_tree(
        cls,
        entities: set[SOMcreator.SOMClass],
        parent_item: QStandardItem,
        model: QStandardItemModel,
        tree: QTreeView,
    ):
        existing_entities_dict = {
            parent_item.child(index, 0).data(CLASS_REFERENCE): index
            for index in range(parent_item.rowCount())
        }

        old_entities = set(existing_entities_dict.keys())
        new_entities = entities.difference(old_entities)
        delete_entities = old_entities.difference(entities)
        for entity in reversed(
            sorted(delete_entities, key=lambda o: existing_entities_dict[o])
        ):
            row_index = existing_entities_dict[entity]
            parent_item.removeRow(row_index)

        for new_entity in sorted(new_entities, key=lambda x: x.name):
            row = cls.create_class_tree_row(new_entity)
            parent_item.appendRow(row)

        for child_row in range(parent_item.rowCount()):
            class_item, som_class = cls.update_class_tree_row(parent_item, child_row)
            som_class: SOMcreator.SOMClass
            if (
                tree.isExpanded(parent_item.index())
                or parent_item == model.invisibleRootItem()
            ):
                cls.fill_class_tree(
                    set(som_class.get_children(filter=False)), class_item, model, tree
                )

    @classmethod
    def create_pset_tree_row(
        cls,
        entity: SOMcreator.SOMPropertySet | SOMcreator.SOMProperty,
        parent_item: QStandardItem,
    ):
        item = QStandardItem(entity.name)
        item.setData(entity, CLASS_REFERENCE)
        item.setCheckable(True)
        item.setCheckState(Qt.CheckState.Checked)
        parent_item.appendRow(item)
        if not isinstance(entity, SOMcreator.SOMPropertySet):
            return
        for som_property in entity.get_properties(filter=True):
            cls.create_pset_tree_row(som_property, item)

    @classmethod
    def _update_pset_row(cls, item: QStandardItem, enabled: bool):
        pset = item.data(CLASS_REFERENCE)
        check_state = item.checkState()
        new_check_state = cls.get_item_check_state(pset)
        if new_check_state != check_state:
            item.setCheckState(new_check_state)
        item.setEnabled(enabled)
        if not isinstance(pset, SOMcreator.SOMPropertySet):
            return
        enabled = (
            True if new_check_state == Qt.CheckState.Checked and enabled else False
        )
        for row in range(item.rowCount()):
            property_item = item.child(row, 0)
            cls._update_pset_row(property_item, enabled)

    @classmethod
    def fill_pset_tree(
        cls,
        property_sets: set[SOMcreator.SOMPropertySet],
        enabled: bool,
        tree: QTreeView,
    ):
        root_item: QStandardItem = tree.model().invisibleRootItem()
        existing_psets_dict = {
            root_item.child(row, 0).data(CLASS_REFERENCE): row
            for row in range(root_item.rowCount())
        }
        old_psets = set(existing_psets_dict.keys())
        new_psets = property_sets.difference(old_psets)
        delete_entities = old_psets.difference(property_sets)

        for entity in reversed(
            sorted(delete_entities, key=lambda o: existing_psets_dict[o])
        ):
            row_index = existing_psets_dict[entity]
            root_item.removeRow(row_index)

        for new_entity in sorted(new_psets, key=lambda x: x.name):
            cls.create_pset_tree_row(new_entity, root_item)

        for row in range(root_item.rowCount()):
            item = root_item.child(row, 0)
            cls._update_pset_row(item, enabled)

    @classmethod
    def set_progressbar_visible(cls, runner: IfcImportRunner, state: bool):
        runner.progress_bar.setVisible(state)

    @classmethod
    def clear_progress_bars(cls):
        scroll_area = cls.get_window().ui.verticalLayout_3
        while scroll_area.count():
            item: QLayoutItem = scroll_area.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @classmethod
    def set_progress_bar_layout_visible(cls, state: bool):
        cls.get_window().ui.scroll_area_progress_bar.setVisible(state)

    @classmethod
    def add_progress_bar(cls, progress_bar: util_ui.Progressbar):
        cls.get_window().ui.verticalLayout_3.addWidget(progress_bar)
