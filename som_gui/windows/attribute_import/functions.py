from __future__ import annotations  # make own class referencable

import logging
import os
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItem, QStandardItemModel
from SOMcreator import classes
from ifcopenshell.util.element import get_pset
from ...widgets import ifc_widget

from ... import settings
from ...ifc_modification.modelcheck import get_identifier

if TYPE_CHECKING:
    from som_gui.windows.attribute_import import gui

CLASS_DATA_ROLE = Qt.ItemDataRole.UserRole + 1
COUNT_ROLE = Qt.ItemDataRole.UserRole + 2
ENTITY_TYPE_ROLE = Qt.ItemDataRole.UserRole + 3
REFERENCE_ROLE = Qt.ItemDataRole.UserRole + 4
VALUE_ROLE = Qt.ItemDataRole.UserRole + 5
OLD_CHECK_STATE = Qt.ItemDataRole.UserRole+6
PSET_NAME_ROLE = Qt.ItemDataRole.UserRole+7
ATTRIBUTE_NAME_ROLE = Qt.ItemDataRole.UserRole+8
ALL = "Alles"


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

    def find_attribute(self, attribute, pset_index: QModelIndex) -> QModelIndex | None:
        for row in range(self.rowCount(pset_index)):
            model_index = self.index(row, 0, pset_index)
            item: classes.Attribute = self.itemFromIndex(model_index).data(CLASS_DATA_ROLE)
            if item == attribute:
                return model_index
        return None

    def get_all_property_sets(self) -> list[QModelIndex]:
        property_sets = list()
        for row in range(self.rowCount()):
            object_index = self.index(row,0)
            for pset_row in range(self.rowCount(object_index)):
                property_sets.append(self.index(pset_row,0,object_index))
        return property_sets

    def count_property_set(self,property_set_name:str) -> int:
        property_sets  = self.get_all_property_sets()
        counter = 0
        for property_set_index in property_sets:
            if property_set_index.data(CLASS_DATA_ROLE).name == property_set_name:
                counter += property_set_index.data(COUNT_ROLE)
        return counter

    def get_all_attributes(self,property_set_name:str) -> list[QModelIndex]:
        attributes = list()
        property_sets  = self.get_all_property_sets()
        for property_set_index in property_sets:
            if property_set_index.data(CLASS_DATA_ROLE).name!= property_set_name:
                continue
            for attribute_row in range(self.rowCount(property_set_index)):
                attributes.append(self.index(attribute_row,0,property_set_index))
        return attributes

    def count_attributes(self,pset_name,attribute_name):
        attributes = self.get_all_attributes(pset_name)
        counter = 0
        for attribute_index in attributes:
            if attribute_index.data(CLASS_DATA_ROLE).name == attribute_name:
                counter += attribute_index.data(COUNT_ROLE)
        return counter

    def get_all_values(self,pset_name,attribute_name) -> list[QModelIndex]:
        values = list()
        attributes = self.get_all_attributes(pset_name)
        for attribute_index in attributes:
            if attribute_index.data(CLASS_DATA_ROLE).name != attribute_name:
                continue
            for value_row in range(self.rowCount(attribute_index)):
                v = self.index(value_row,0,attribute_index)
                if v is None:
                    continue
                values.append(v)
        return values

    def count_values(self,pset_name,attribute_name,value_name):
        values = self.get_all_values(pset_name,attribute_name)
        counter =  0
        for value_index in values:
            if value_index.data(VALUE_ROLE) == value_name:
                counter+= value_index.data(COUNT_ROLE)
        return counter

    def get_value_check_state(self,pset_name:str,attribute_name:str,value_name:str):
        values = self.get_all_values(pset_name, attribute_name)
        for value in values:
            if value.data(VALUE_ROLE) != value_name:
                continue
            state = value.data(Qt.ItemDataRole.CheckStateRole)
            if state == 0 or state == Qt.CheckState.Unchecked:
                return Qt.CheckState.Unchecked

        return Qt.CheckState.Checked
    def set_value_check_state(self,pset_name:str,attribute_name:str,value_name:str,check_state:Qt.CheckState):
        values = self.get_all_values(pset_name, attribute_name)
        for value in values:
            if value.data(VALUE_ROLE) != value_name:
                continue
            print(f"set CheckState {check_state}")
            self.setData(value,check_state,Qt.ItemDataRole.CheckStateRole)

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
        attribute_index = self.item_model.find_attribute(attribute, pset_index)
        value = ifc_pset_dict.get(attribute.name)

        if attribute_index is None:
            self.add_attribute_to_model(pset_index, attribute, value)
            return
        item = self.item_model.itemFromIndex(attribute_index)
        current_count = item.data(COUNT_ROLE)
        item.setData(current_count + 1, COUNT_ROLE)

        for row in range(self.item_model.rowCount(attribute_index)):
            value_index = self.item_model.index(row, 0, attribute_index)
            existing_value = value_index.data(VALUE_ROLE)
            if value == existing_value:
                count_data = self.item_model.data(value_index, COUNT_ROLE)
                self.item_model.setData(value_index, count_data + 1, COUNT_ROLE)
                return

        self.add_value_to_model(attribute_index, value)

    def add_object_to_model(self, obj: classes.Object, entity_type) -> QModelIndex:
        item = QStandardItem()
        item.setData(obj.name)
        item.setData(obj, CLASS_DATA_ROLE)
        item.setData(1, COUNT_ROLE)
        item.setData({entity_type}, ENTITY_TYPE_ROLE)
        self.item_model.invisibleRootItem().appendRow(item)
        return self.item_model.indexFromItem(item)

    def add_pset_to_model(self, object_index: QModelIndex, property_set: classes.PropertySet) -> QModelIndex:
        parent_item = self.item_model.itemFromIndex(object_index)
        item = QStandardItem(property_set.name)
        item.setData(property_set.name)
        item.setData(property_set, CLASS_DATA_ROLE)
        item.setData(1, COUNT_ROLE)
        parent_item.appendRow(item)
        return self.item_model.indexFromItem(item)

    def add_attribute_to_model(self, pset_index: QModelIndex, attribute: classes.Attribute,
                               value: str | int | float | None) -> QModelIndex:
        parent_item = self.item_model.itemFromIndex(pset_index)
        item = QStandardItem(attribute.name)
        item.setData(attribute.name)
        item.setData(attribute, CLASS_DATA_ROLE)
        item.setData(1, COUNT_ROLE)
        parent_item.appendRow(item)
        self.add_value_to_model(item.index(), value)

        return self.item_model.indexFromItem(item)

    def add_value_to_model(self, attribute_index: QModelIndex, value):
        parent_item = self.item_model.itemFromIndex(attribute_index)
        text = "undefined" if value is None else str(value)
        item = QStandardItem(text)
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        item.setData(value, VALUE_ROLE)
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
        window.widget.table_widget_property_set.clicked.connect(lambda index: pset_table_clicked(window, index))
        window.widget.table_widget_attribute.clicked.connect(lambda index: attribute_table_clicked(window, index))
        window.widget.table_widget_attribute.doubleClicked.connect(attribute_table_double_clicked)
        window.widget.table_widget_value.clicked.connect(lambda index: value_table_clicked(window, index))

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
    texts.append(ALL)
    window.widget.combo_box_group.addItems(texts)
    pass


def type_index_changed(window: gui.AttributeImport):
    current_type = window.widget.combo_box_group.currentText()
    items = list()
    for row in range(window.item_model.rowCount()):
        item = window.item_model.item(row, 0)
        if current_type in item.data(ENTITY_TYPE_ROLE) or current_type == ALL:
            items.append(item)

    texts = [format_object_for_combobox(item.data(CLASS_DATA_ROLE)) for item in items if
             item.data(CLASS_DATA_ROLE) is not None]
    texts.append(ALL)
    window.widget.combo_box_name.clear()
    window.widget.combo_box_name.addItems(texts)


def object_index_changed(window: gui.AttributeImport):
    model = window.item_model
    current_text = window.widget.combo_box_name.currentText()
    if current_text == ALL:
        window.combi_mode = True
        combi_mode_activated(window)
        return
    else:
        window.combi_mode = False
    object_items = list(model.item(row, 0) for row in range(model.rowCount()))
    current_item: QStandardItem | None = {format_object_for_combobox(o.data(CLASS_DATA_ROLE)): o for o in
                                          object_items}.get(current_text)
    if current_item is None:
        return
    object_count = current_item.data(COUNT_ROLE)
    window.set_object_count(object_count)

    property_set_items = list()
    for row in range(model.rowCount(current_item.index())):
        pset_index = model.index(row, 0, current_item.index())
        property_set_items.append(model.itemFromIndex(pset_index))

    table_model = window.widget.table_widget_property_set.model()
    window.clear_table(window.widget.table_widget_property_set)
    window.clear_table(window.widget.table_widget_attribute)
    window.clear_table(window.widget.table_widget_value)
    for pset_item in sorted(property_set_items, key=lambda item: item.data(CLASS_DATA_ROLE).name):
        new_item = pset_item.clone()
        new_item.setData(pset_item.index(), REFERENCE_ROLE)
        count_item = QStandardItem(str(pset_item.data(COUNT_ROLE)))
        table_model.appendRow([new_item, count_item])
    window.widget.table_widget_property_set.setModel(table_model)


def combi_mode_activated(window:gui.AttributeImport):
    window.clear_table(window.widget.table_widget_property_set)
    window.clear_table(window.widget.table_widget_attribute)
    window.clear_table(window.widget.table_widget_value)
    model = window.item_model
    object_count = sum([model.item(row,0).data(COUNT_ROLE) for  row in range(model.rowCount())])
    window.set_object_count(object_count)

    property_sets = window.item_model.get_all_property_sets()

    property_set_names = {index.data(CLASS_DATA_ROLE).name for index in property_sets}
    for property_set in property_set_names:
        pset_name_item = QStandardItem(property_set)
        pset_count_item = QStandardItem(str(window.item_model.count_property_set(property_set)))
        window.widget.table_widget_property_set.model().appendRow([pset_name_item,pset_count_item])

def combi_model_pset_clicked(window:gui.AttributeImport, pset_index:QModelIndex):
    pset_index = window.widget.table_widget_property_set.model().index(pset_index.row(),0)
    window.clear_table(window.widget.table_widget_attribute)
    model = window.item_model
    pset_name = pset_index.data()
    attributes = model.get_all_attributes(pset_name)
    attribute_names = {index.data(CLASS_DATA_ROLE).name for index in attributes}
    for attribute_name in attribute_names:
        attribute_name_item = QStandardItem(attribute_name)
        attribute_name_item.setData(pset_name,CLASS_DATA_ROLE)
        attribute_count_item = QStandardItem(str(model.count_attributes(pset_name,attribute_name)))
        values = model.get_all_values(pset_name,attribute_name)
        attribute_distinct_item = QStandardItem(str(len({index.data(VALUE_ROLE) for index in values})))
        window.widget.table_widget_attribute.model().appendRow([attribute_name_item, attribute_count_item,attribute_distinct_item])

def combi_model_attribute_clicked(window:gui.AttributeImport,attribute_index:QModelIndex):
    attribute_index = window.widget.table_widget_attribute.model().index(attribute_index.row(),0)
    pset_name = attribute_index.data(CLASS_DATA_ROLE)
    attribute_name = attribute_index.data()
    model = window.item_model
    values = model.get_all_values(pset_name,attribute_name)
    value_texts = {index.data(VALUE_ROLE) for index in values}
    window.clear_table(window.widget.table_widget_value)
    for value in value_texts:
        value_text_item = QStandardItem(value)
        value_text_item.setData(pset_name,PSET_NAME_ROLE)
        value_text_item.setData(attribute_name,ATTRIBUTE_NAME_ROLE)
        value_count_item = QStandardItem(str(model.count_values(pset_name,attribute_name,value)))
        value_text_item.setCheckable(True)
        check_state = model.get_value_check_state(pset_name,attribute_name,value)
        value_text_item.setData(check_state,OLD_CHECK_STATE)
        value_text_item.setData(check_state,Qt.ItemDataRole.CheckStateRole)
        window.widget.table_widget_value.model().appendRow([value_text_item, value_count_item])


def combi_model_value_clicked(window:gui.AttributeImport,value_index:QModelIndex):
    value_index = window.widget.table_widget_value.model().index(value_index.row(), 0)
    pset_name = value_index.data(PSET_NAME_ROLE)
    attribute_name = value_index.data(ATTRIBUTE_NAME_ROLE)
    old_check_state = value_index.data(OLD_CHECK_STATE)
    model = window.item_model
    new_check_state = value_index.data(Qt.ItemDataRole.CheckStateRole)
    if old_check_state == new_check_state:
        return
    model.setData(value_index,new_check_state,OLD_CHECK_STATE)
    model.set_value_check_state(pset_name,attribute_name,value_index.data(),new_check_state)


def pset_table_clicked(window: gui.AttributeImport, index: QModelIndex):
    window.clear_table(window.widget.table_widget_attribute)
    window.clear_table(window.widget.table_widget_value)
    window.widget.check_box_values.setEnabled(False)
    if window.combi_mode:
        combi_model_pset_clicked(window, index)
        return

    pset_index: QModelIndex = index.model().index(index.row(), 0).data(REFERENCE_ROLE)
    model = window.item_model
    attribute_table_model: QStandardItemModel = window.widget.table_widget_attribute.model()

    for row in range(model.rowCount(pset_index)):
        attribute_index = model.index(row, 0, pset_index)
        new_attribute_item = model.itemFromIndex(attribute_index).clone()
        new_attribute_item.setData(attribute_index, REFERENCE_ROLE)
        count_item = QStandardItem(str(new_attribute_item.data(COUNT_ROLE)))
        distinct_item = QStandardItem(str(model.rowCount(attribute_index)))
        attribute_table_model.appendRow([new_attribute_item, count_item, distinct_item])


def attribute_table_clicked(window: gui.AttributeImport, index: QModelIndex):
    window.clear_table(window.widget.table_widget_value)
    window.widget.check_box_values.setEnabled(True)
    if window.combi_mode:
        combi_model_attribute_clicked(window,index)
        are_all_values_checked(window)
        return
    attribute_index: QModelIndex = index.model().index(index.row(), 0).data(REFERENCE_ROLE)

    model = window.item_model
    value_table_model: QStandardItemModel = window.widget.table_widget_value.model()

    for row in range(model.rowCount(attribute_index)):
        value_index = model.index(row, 0, attribute_index)
        new_item = model.itemFromIndex(value_index).clone()
        new_item.setCheckable(True)
        new_item.setData(value_index, REFERENCE_ROLE)
        count_item = QStandardItem(str(new_item.data(COUNT_ROLE)))
        value_table_model.appendRow([new_item, count_item])

    are_all_values_checked(window)

def attribute_table_double_clicked():
    pass


def value_table_clicked(window: gui.AttributeImport, index: QModelIndex):
    if window.combi_mode:
        combi_model_value_clicked(window,index)
    else:
        value_index: QModelIndex = index.model().index(index.row(), 0).data(REFERENCE_ROLE)
        new_check_state = index.data(Qt.ItemDataRole.CheckStateRole)
        window.item_model.setData(value_index, new_check_state, Qt.ItemDataRole.CheckStateRole)
    are_all_values_checked(window)



def are_all_values_checked(window: gui.AttributeImport):
    model = window.widget.table_widget_value.model()
    for row in range(model.rowCount()):
        state = model.index(row, 0).data(Qt.ItemDataRole.CheckStateRole)
        if state == Qt.CheckState.Unchecked or state == 0:
            window.widget.check_box_values.setChecked(False)
            return
    window.widget.check_box_values.setChecked(True)



def main_checkbox_clicked(window: gui.AttributeImport):
    new_check_state = window.widget.check_box_values.checkState()
    model = window.widget.table_widget_value.model()
    for row in range(model.rowCount()):
        index = model.index(row, 0)
        model.setData(index, new_check_state, Qt.ItemDataRole.CheckStateRole)

    for row in range(model.rowCount()):
        index = model.index(row, 0)
        value_table_clicked(window, index)


def settings_clicked(window: gui.AttributeImport):
    pass


def abort_clicked(window: gui.AttributeImport):
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


def format_object_for_combobox(obj: classes.Object) -> str:
    return f"{obj.name} ({obj.ident_value})"
