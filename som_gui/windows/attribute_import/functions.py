from __future__ import annotations  # make own class referencable

import logging
import os
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import QThreadPool, Qt, QModelIndex
from PySide6.QtGui import QBrush, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QDialog
from SOMcreator import classes, value_constants
from ifcopenshell.util.element import get_pset
from ...widgets import ifc_widget

from ... import settings
from ...icons import get_icon, get_settings_icon
from ...ifc_modification.modelcheck import get_identifier
from ...settings import EXISTING_ATTRIBUTE_IMPORT, RANGE_ATTRIBUTE_IMPORT, REGEX_ATTRIBUTE_IMPORT, \
    COLOR_ATTTRIBUTE_IMPORT
from ...widgets import property_widget

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow
    from som_gui.windows.attribute_import import gui
from ...qt_designs import ui_attribute_import_window, ui_attribute_import_settings_window

CLASS_DATA_ROLE = Qt.ItemDataRole.UserRole + 1
COUNT_ROLE = Qt.ItemDataRole.UserRole + 2
ENTITY_TYPE_ROLE = Qt.ItemDataRole.UserRole + 3


class ObjectModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def find_object(self, obj: classes.Object) -> QModelIndex | None:
        for row in range(self.rowCount()):
            model_index = self.index(row, 0)
            item: classes.Object = self.itemFromIndex(model_index).data(CLASS_DATA_ROLE)
            if item == obj:
                return model_index
        return None

    def find_property_set(self, property_set: classes.PropertySet, obj_index: QModelIndex) -> QModelIndex | None:
        for row in range(self.rowCount(obj_index)):
            model_index = self.index(row, 0, obj_index)
            item: classes.PropertySet = self.itemFromIndex(model_index).data(CLASS_DATA_ROLE)
            if item == property_set:
                return model_index
        return None


class IfcImportRunner(ifc_widget.IfcRunner):
    def __init__(self, ifc_paths: list[str], window: gui.AttributeImport, main_pset: str, main_attribute: str,
                 function_name: str):
        self.data_dict = dict()
        self.count_dict = dict()
        self.window: gui.AttributeImport = window
        self.project = self.window.project
        self.bk_dict: dict[str, classes.Object] = {obj.ident_value: obj for obj in self.project.objects}
        super(IfcImportRunner, self).__init__(ifc_paths, window.project, main_pset, main_attribute,
                                              function_name)

    @property
    def item_model(self) -> ObjectModel:
        return self.window.item_model

    def run_file_function(self, file_path: str | os.PathLike):
        def is_real_layer(e: ifcopenshell.entity_instance) -> bool:
            """filter that checks if layer is just grouping layer"""

            def get_parent_groups(internal_entity: ifcopenshell.entity_instance):
                parents = set()
                for rel in getattr(internal_entity, "HasAssignments", []):
                    if rel.is_a("IfcRelAssignsToGroup"):
                        parents.add(rel[6])
                return parents

            def get_layers(internal_entity: ifcopenshell.entity_instance) -> set[int]:
                parent_groups = get_parent_groups(internal_entity)
                _layers = set()

                if not parent_groups:
                    _layers.add(0)
                    return _layers

                for parent in parent_groups:
                    for layer in get_layers(parent):
                        _layers.add(layer + 1)

                return _layers

            layers = get_layers(e)
            values = [layer % 2 == 0 for layer in layers]
            if all(values):
                return False
            if any(values):
                logging.warning(f"Gruppenlayer von {e} kontrollieren!")
            else:
                return True

        ifc = super(IfcImportRunner, self).run_file_function(file_path)
        entities = ifc.by_type("IfcElement") + list(filter(is_real_layer, ifc.by_type("IfcGroup")))
        element_count = len(entities)
        for index, entity in enumerate(entities, start=1):
            if self.is_aborted:
                return
            if index % 10 == 0:
                self.signaller.status.emit(f"Check {index}/{element_count}")
                progress = index / element_count * 100
                self.signaller.progress.emit(progress)
            self.import_entity(entity)
        print(f"Row Count: {self.item_model.rowCount()}")

    def import_entity(self, entity: ifcopenshell.entity_instance):
        if self.is_aborted:
            return
        ident = get_identifier(entity, self.main_pset, self.main_attribute)
        obj = self.bk_dict.get(ident)
        if obj is None:
            return

        entity_type = entity.get_info()["type"]

        model_index = self.item_model.find_object(obj)
        if model_index is None:
            model_index = self.add_object_to_model(obj, entity_type)
        else:
            item = self.item_model.itemFromIndex(model_index)
            current_count = item.data(COUNT_ROLE)
            current_types = item.data(ENTITY_TYPE_ROLE)
            current_types.add(entity_type)
            item.setData(current_count + 1, COUNT_ROLE)
            item.setData(current_types, ENTITY_TYPE_ROLE)

        for property_set in obj.property_sets:
            self.import_property_set(model_index, property_set, entity)

    def import_property_set(self, obj_index: QModelIndex, property_set: classes.PropertySet,
                            entity: ifcopenshell.entity_instance):
        pset_name = property_set.name
        ifc_pset_dict = get_pset(entity, pset_name)

        if ifc_pset_dict is None:
            return

        pset_index = self.item_model.find_property_set(property_set, obj_index)
        if pset_index is None:
            pset_index = self.add_pset_to_model(obj_index, property_set)
        else:
            current_count = self.item_model.itemFromIndex(pset_index).data(COUNT_ROLE)
            self.item_model.itemFromIndex(pset_index).setData(current_count + 1, COUNT_ROLE)

        for attribute in property_set.attributes:
            self.import_attribute(pset_index, attribute, ifc_pset_dict)

    def import_attribute(self, pset_index: QModelIndex, attribute, ifc_pset_dict):
        attribute_name = attribute.name
        value = ifc_pset_dict.get(attribute_name)
        if value is None:
            return

        add_range = settings.get_setting_attribute_import_range()
        add_regex = settings.get_setting_attribute_import_regex()
        if attribute.value_type == value_constants.RANGE and not add_range:
            return
        if attribute.value_type == value_constants.FORMAT and not add_regex:
            return

        item = QStandardItem()
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        item.setData(attribute, CLASS_DATA_ROLE)
        item.setData(1, COUNT_ROLE)
        parent_item = self.item_model.itemFromIndex(pset_index)
        parent_item.appendRow(item)

    def add_object_to_model(self, obj: classes.Object, entity_type) -> QModelIndex:
        item = QStandardItem()
        item.setData(obj, CLASS_DATA_ROLE)
        item.setData(1, COUNT_ROLE)
        item.setData({entity_type}, ENTITY_TYPE_ROLE)
        self.item_model.invisibleRootItem().appendRow(item)
        return self.item_model.indexFromItem(item)

    def add_pset_to_model(self, object_index: QModelIndex, property_set: classes.PropertySet) -> QModelIndex:
        parent_item = self.item_model.itemFromIndex(object_index)
        item = QStandardItem()
        item.setData(property_set, CLASS_DATA_ROLE)
        item.setData(1, COUNT_ROLE)
        parent_item.appendRow(item)
        return self.item_model.indexFromItem(item)


def init(window: gui.AttributeImport):
    def connect():
        window.widget.button_ifc.clicked.connect(lambda: ifc_button_clicked(window))  # IFC Auswahl
        window.widget.combo_box_name.currentIndexChanged.connect(lambda: object_index_changed(window))
        window.widget.combo_box_group.currentIndexChanged.connect(lambda: type_index_changed(window))
        window.widget.check_box_values.clicked.connect(lambda: main_checkbox_clicked(window))
        window.widget.button_run.clicked.connect(lambda: button_run_clicked(window))
        window.widget.button_accept.clicked.connect(lambda: button_accept_clicked(window))
        window.widget.button_settings.clicked.connect(lambda: settings_clicked(window))
        window.widget.button_abort.clicked.connect(lambda: abort_clicked(window))
        window.widget.table_widget_property_set.clicked.connect(pset_table_clicked)
        window.widget.table_widget_attribute.clicked.connect(attribute_table_clicked)
        window.widget.table_widget_attribute.doubleClicked.connect(attribute_table_double_clicked)
        window.widget.table_widget_value.clicked.connect(value_table_clicked)

    connect()
    ifc_widget.set_main_attribute(window.project, window.widget.line_edit_ident_pset,
                                  window.widget.line_edit_ident_attribute)
    ifc_widget.auto_set_ifc_path(window.widget.line_edit_ifc)


def ifc_button_clicked(window: gui.AttributeImport) -> None:
    path = ifc_widget.ifc_file_dialog(window, window.widget.line_edit_ifc)
    if path is None:
        return


def button_run_clicked(window: gui.AttributeImport) -> None:
    path = window.widget.line_edit_ifc.text()
    paths = path.split(settings.PATH_SEPERATOR)
    main_property_set_name = window.widget.line_edit_ident_pset.text()
    main_attribute_name = window.widget.line_edit_ident_attribute.text()
    import_ifc(window, paths, main_property_set_name, main_attribute_name)


def import_ifc(window: gui.AttributeImport, paths: list[str], main_property_set_name: str,
               main_attribute_name: str) -> None:
    runner = IfcImportRunner(paths, window, main_property_set_name, main_attribute_name, "ImportIFC")
    connect_runner_signals(window, runner)
    window.thread_pool.start(runner)


def connect_runner_signals(window: gui.AttributeImport, runner: IfcImportRunner):
    runner.signaller.started.connect(lambda: runner_started(window))
    runner.signaller.finished.connect(lambda text: runner_finished(window, text))
    runner.signaller.progress.connect(window.widget.progress_bar.setValue)
    runner.signaller.status.connect(lambda text: update_status(window, text))


def runner_started(window: gui.AttributeImport):
    logging.info(f"Runner Started")
    hide_progress_bar(window, False)
    window.widget.button_run.hide()
    window.widget.button_accept.show()
    window.widget.button_accept.setEnabled(False)


def update_status(window: gui.AttributeImport, status):
    logging.info(f"Runner Status: {status}")
    window.widget.label_status.setText(status)


def runner_finished(window: gui.AttributeImport, text):
    logging.info(f"Runner finished: {text}")
    hide_progress_bar(window, True)
    hide_tables(window, False)
    window.widget.button_accept.setEnabled(True)
    fill_type_combobox(window)


def fill_type_combobox(window: gui.AttributeImport):
    model = window.item_model
    all_entity_types = set()
    for row in range(model.rowCount()):
        entity_types = model.item(row, 0).data(ENTITY_TYPE_ROLE)
        all_entity_types.update(entity_types)

    window.widget.combo_box_group.clear()
    texts = [str(t) for t in sorted(all_entity_types) if t is not None]
    window.widget.combo_box_group.addItems(texts)
    pass


def object_index_changed(window: gui.AttributeImport):
    pass


def type_index_changed(window: gui.AttributeImport):
    pass


def pset_table_clicked():
    pass


def attribute_table_clicked():
    pass


def attribute_table_double_clicked():
    pass


def value_table_clicked():
    pass


def main_checkbox_clicked():
    pass


def settings_clicked():
    pass


def abort_clicked():
    pass


def button_accept_clicked(window: gui.AttributeImport):
    pass


def hide_progress_bar(window: gui.AttributeImport, value: bool) -> None:
    items = [window.widget.label_status, window.widget.progress_bar]
    window.hide_items(items, value)


def hide_tables(window: gui.AttributeImport, value: bool) -> None:
    items = [window.widget.splitter_tables, window.widget.combo_box_group, window.widget.combo_box_name,
             window.widget.label_object_count, window.widget.label_status]
    window.hide_items(items, value)
