from __future__ import annotations
import som_gui.core.tool
from som_gui import tool
from som_gui.module.modelcheck.constants import ISSUE_PATH
from som_gui.module.modelcheck_window import ui, trigger
from som_gui.module.project.constants import CLASS_REFERENCE
import SOMcreator
from typing import TYPE_CHECKING, Callable
from PySide6.QtCore import Qt, QThreadPool, QSize, QRunnable
from PySide6.QtWidgets import QSplitter, QSizePolicy, QLayout, QWidget, QTreeView, QFileDialog, QLineEdit, QPushButton, \
    QLabel, QMenu
from PySide6.QtGui import QStandardItem, QStandardItemModel, QAction
import os

if TYPE_CHECKING:
    from som_gui.module.modelcheck_window.prop import ModelcheckWindowProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget


class ModelcheckWindow(som_gui.core.tool.ModelcheckWindow):

    @classmethod
    def create_context_menu(cls, pos, funcion_list: list[list[str, Callable]], widget: ui.ObjectTree | ui.PsetTree):
        global_pos = widget.viewport().mapToGlobal(pos)
        menu = QMenu()
        actions = list()
        for function_name, function in funcion_list:
            actions.append(QAction(function_name))
            menu.addAction(actions[-1])
            actions[-1].triggered.connect(function)
        menu.exec(global_pos)

    @classmethod
    def expand_selection(cls, widget: ui.ObjectTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            widget.expand(index)

    @classmethod
    def collapse_selection(cls, widget: ui.ObjectTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            widget.collapse(index)

    @classmethod
    def check_selection(cls, widget: ui.ObjectTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            if index.column() != 0:
                continue
            widget.model().setData(index, Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole)

    @classmethod
    def uncheck_selection(cls, widget: ui.ObjectTree | ui.PsetTree):
        indexes = [i for i in widget.selectedIndexes()]
        for index in indexes:
            if index.column() != 0:
                continue
            widget.model().setData(index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)

    @classmethod
    def resize_object_tree(cls):
        cls.get_properties().checkbox_widget.widget.object_tree.resizeColumnToContents(0)

    @classmethod
    def get_selected_items(cls, widget: ui.ObjectTree | ui.PsetTree):
        return [i.data(CLASS_REFERENCE) for i in widget.selectedIndexes()]

    @classmethod
    def is_initial_paint(cls):
        if cls.get_properties().initial_paint:
            cls.get_properties().initial_paint = False
            return True
        return False

    @classmethod
    def set_abort_button_text(cls, text: str):
        button = cls.get_properties().abort_button
        button.setText(text)

    @classmethod
    def set_run_button_enabled(cls, state):
        cls.get_properties().run_button.setEnabled(state)

    @classmethod
    def modelcheck_is_running(cls):
        return cls.get_modelcheck_threadpool().activeThreadCount() > 0

    @classmethod
    def connect_ifc_import_runner(cls, runner: QRunnable):
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def connect_modelcheck_runner(cls, runner: QRunnable):
        trigger.connect_modelcheck_runner(runner)

    @classmethod
    def create_import_runner(cls, ifc_import_path: str):
        status_label = cls.get_properties().status_label
        runner = tool.IfcImporter.create_runner(status_label, ifc_import_path)
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
    def set_progress(cls, value: int):
        cls.get_ifc_import_widget().widget.progress_bar.setValue(value)

    @classmethod
    def set_status(cls, text: str):
        cls.get_properties().status_label.setText(text)

    @classmethod
    def set_export_line_text(cls, text: str):
        cls.get_properties().export_line_edit.setText(text)

    @classmethod
    def read_inputs(cls):
        widget = cls.get_properties().ifc_import_widget
        ifc_paths = tool.IfcImporter.get_ifc_paths(widget)
        export_path = cls.get_properties().export_line_edit.text()
        main_pset = tool.IfcImporter.get_main_pset(widget)
        main_attribute = tool.IfcImporter.get_main_attribute(widget)
        return ifc_paths, export_path, main_pset, main_attribute

    @classmethod
    def get_modelcheck_threadpool(cls):
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def get_export_path(cls, widget: IfcImportWidget):
        return widget.widget.line_edit_export.text()

    @classmethod
    def open_export_dialog(cls, base_path: os.PathLike | str, file_text: str):
        path = QFileDialog.getSaveFileName(cls.get_properties().active_window, "Export", base_path, file_text)[0]
        return path

    @classmethod
    def set_pset_tree_title(cls, text: str):
        prop = cls.get_properties()
        prop.checkbox_widget.widget.label_object.setText(text)

    @classmethod
    def show_pset_tree_title(cls, show: bool):
        prop = cls.get_properties()
        prop.checkbox_widget.widget.label_object.setVisible(show)

    @classmethod
    def set_selected_object(cls, obj: SOMcreator.Object):
        prop = cls.get_properties()
        prop.selected_object = obj

    @classmethod
    def get_selected_object(cls) -> SOMcreator.Object | None:
        return cls.get_properties().selected_object

    @classmethod
    def get_object_tree(cls):
        prop = cls.get_properties()
        return prop.checkbox_widget.widget.object_tree

    @classmethod
    def get_pset_tree(cls):
        prop = cls.get_properties()
        return prop.checkbox_widget.widget.property_set_tree

    @classmethod
    def get_item_status_dict(cls):
        checkstate_dict = cls.get_item_checkstate_dict()

    @classmethod
    def get_item_checkstate_dict(cls):
        """
        returns item checkstate in TreeView
        """
        prop = cls.get_properties()
        data_dict = dict()
        if not prop.check_state_dict:
            for obj in tool.Project.get().get_objects(filter=True):
                data_dict[obj] = True
                for property_set in obj.property_sets:
                    data_dict[property_set] = True
                    for attribute in property_set.attributes:
                        data_dict[attribute] = True
            prop.check_state_dict = data_dict

        return prop.check_state_dict

    @classmethod
    def get_item_check_state(cls,
                             item: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute) -> Qt.CheckState:
        cd = cls.get_item_checkstate_dict()
        if cd.get(item) is None:
            cd[item] = True
        check_state = Qt.CheckState.Checked if cd[item] else Qt.CheckState.Unchecked
        return check_state

    @classmethod
    def set_item_check_state(cls, item: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute,
                             cs: Qt.CheckState) -> None:
        cs = True if cs == Qt.CheckState.Checked else False
        cd = cls.get_item_checkstate_dict()
        cd[item] = cs

    @classmethod
    def get_properties(cls) -> ModelcheckWindowProperties:
        return som_gui.ModelcheckWindowProperties

    @classmethod
    def create_checkbox_widget(cls):
        prop = cls.get_properties()
        prop.checkbox_widget = ui.ObjectCheckWidget()
        cls.show_pset_tree_title(False)
        return prop.checkbox_widget

    @classmethod
    def autofill_export_path(cls):
        export_path = tool.Appdata.get_path(ISSUE_PATH)
        if export_path:
            cls.get_properties().export_line_edit.setText(export_path)

    @classmethod
    def create_export_line(cls, widget: IfcImportWidget):
        export_line_edit = QLineEdit()
        export_line_edit.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))
        widget.widget.gridLayout.addWidget(QLabel("Export Pfad"), 5, 0, 1, 2)
        widget.widget.gridLayout.addWidget(export_line_edit, 6, 0, 1, 2)
        export_button = QPushButton()
        export_button.setMaximumSize(QSize(25, 16777215))
        widget.widget.gridLayout.addWidget(export_button, 6, 2, 1, 1)
        export_button.show()
        export_button.setText("...")
        cls.get_properties().export_button = export_button
        cls.get_properties().export_line_edit = export_line_edit
        cls.autofill_export_path()

    @classmethod
    def set_importer_widget(cls, widget: IfcImportWidget):
        prop = cls.get_properties()
        prop.ifc_import_widget = widget
        prop.ifc_button = widget.widget.button_ifc
        prop.ifc_line_edit = widget.widget.line_edit_ifc
        prop.run_button = widget.widget.button_run
        prop.abort_button = widget.widget.button_close
        prop.status_label = widget.widget.label_status

    @classmethod
    def get_buttons(cls) -> tuple[QPushButton, QPushButton, QPushButton, QPushButton]:
        ifc = cls.get_properties().ifc_button
        export = cls.get_properties().export_button
        run = cls.get_properties().run_button
        abort = cls.get_properties().abort_button
        return ifc, export, run, abort

    @classmethod
    def is_window_allready_build(cls):
        return bool(cls.get_properties().active_window)

    @classmethod
    def get_window(cls) -> ui.ModelcheckWindow:
        return cls.get_properties().active_window

    @classmethod
    def create_window(cls):
        prop = cls.get_properties()
        prop.active_window = ui.ModelcheckWindow()
        return prop.active_window

    @classmethod
    def close_window(cls):
        cls.get_properties().active_window.hide()

    @classmethod
    def connect_check_widget(cls, widget: ui.ObjectCheckWidget):
        trigger.connect_object_check_tree(widget.widget.object_tree)

    @classmethod
    def connect_buttons(cls, buttons):
        trigger.connect_buttons(*buttons)

    @classmethod
    def add_splitter(cls, layout: QLayout, orientation: Qt.Orientation, widget_1: QWidget, widget_2: QWidget):
        splitter = QSplitter(orientation)
        layout.addWidget(splitter)
        splitter.addWidget(widget_1)
        splitter.addWidget(widget_2)

    @classmethod
    def create_object_tree_row(cls, obj: SOMcreator.Object):
        item_list = [QStandardItem(obj.name), QStandardItem(obj.ident_value)]
        item_list[0].setFlags(item_list[0].flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable)
        item_list[0].setCheckable(True)
        item_list[0].setCheckState(Qt.CheckState.Checked)
        [i.setData(obj, CLASS_REFERENCE) for i in item_list]
        return item_list

    @classmethod
    def update_object_tree_row(cls, parent_item: QStandardItem, row_index):
        items = [parent_item.child(row_index, col) for col in range(parent_item.columnCount())]
        obj = items[0].data(CLASS_REFERENCE)
        texts = [obj.name, obj.ident_value]

        for column, text in enumerate(texts):
            if items[column].text() != text:
                items[column].setText(text)

        cs = cls.get_item_check_state(items[0].data(CLASS_REFERENCE))
        if items[0].checkState() != cs:
            items[0].setCheckState(cs)

        enabled = True if parent_item.isEnabled() and parent_item.checkState() == Qt.CheckState.Checked else False
        if parent_item == parent_item.model().invisibleRootItem():
            enabled = True

        for item in items:
            item.setEnabled(enabled)
        return items[0], obj

    @classmethod
    def fill_object_tree(cls, entities: set[SOMcreator.Object], parent_item: QStandardItem, model: QStandardItemModel,
                         tree: QTreeView):
        existing_entities_dict = {parent_item.child(index, 0).data(CLASS_REFERENCE): index for index in
                                  range(parent_item.rowCount())}

        old_entities = set(existing_entities_dict.keys())
        new_entities = entities.difference(old_entities)
        delete_entities = old_entities.difference(entities)
        for entity in reversed(sorted(delete_entities, key=lambda o: existing_entities_dict[o])):
            row_index = existing_entities_dict[entity]
            parent_item.removeRow(row_index)

        for new_entity in sorted(new_entities, key=lambda x: x.name):
            row = cls.create_object_tree_row(new_entity)
            parent_item.appendRow(row)

        for child_row in range(parent_item.rowCount()):
            class_item, obj = cls.update_object_tree_row(parent_item, child_row)
            if tree.isExpanded(parent_item.index()) or parent_item == model.invisibleRootItem():
                cls.fill_object_tree(obj.get_all_children(), class_item, model, tree)

    @classmethod
    def create_pset_tree_row(cls, entity: SOMcreator.PropertySet | SOMcreator.Attribute, parent_item: QStandardItem):
        item = QStandardItem(entity.name)
        item.setData(entity, CLASS_REFERENCE)
        item.setCheckable(True)
        item.setCheckState(Qt.CheckState.Checked)
        parent_item.appendRow(item)
        if not isinstance(entity, SOMcreator.PropertySet):
            return
        for attribute in entity.attributes:
            cls.create_pset_tree_row(attribute, item)

    @classmethod
    def _update_pset_row(cls, item: QStandardItem, enabled: bool):
        pset = item.data(CLASS_REFERENCE)
        check_state = item.checkState()
        new_check_state = cls.get_item_check_state(pset)
        if new_check_state != check_state:
            item.setCheckState(new_check_state)
        item.setEnabled(enabled)
        if not isinstance(pset, SOMcreator.PropertySet):
            return
        enabled = True if new_check_state == Qt.CheckState.Checked and enabled else False
        for row in range(item.rowCount()):
            attribute_item = item.child(row, 0)
            cls._update_pset_row(attribute_item, enabled)

    @classmethod
    def fill_pset_tree(cls, property_sets: set[SOMcreator.PropertySet], enabled: bool, tree: QTreeView):
        root_item: QStandardItem = tree.model().invisibleRootItem()
        existing_psets_dict = {root_item.child(row, 0).data(CLASS_REFERENCE): row for row in
                               range(root_item.rowCount())}
        old_psets = set(existing_psets_dict.keys())
        new_psets = property_sets.difference(old_psets)
        delete_entities = old_psets.difference(property_sets)

        for entity in reversed(sorted(delete_entities, key=lambda o: existing_psets_dict[o])):
            row_index = existing_psets_dict[entity]
            root_item.removeRow(row_index)

        for new_entity in sorted(new_psets, key=lambda x: x.name):
            cls.create_pset_tree_row(new_entity, root_item)

        for row in range(root_item.rowCount()):
            item = root_item.child(row, 0)
            cls._update_pset_row(item, enabled)

    @classmethod
    def get_ifc_import_widget(cls) -> IfcImportWidget:
        return cls.get_properties().ifc_import_widget
