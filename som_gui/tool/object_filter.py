from __future__ import annotations
import logging

import SOMcreator
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
from PySide6.QtWidgets import QTreeView, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QCheckBox, QSizePolicy
import som_gui.core.tool
from som_gui.tool.project import Project
from som_gui.module.object_filter import data as object_filter_data
from som_gui.module.object_filter import trigger
from som_gui.module import object_filter
import som_gui.module.object_filter.constants
import som_gui
from som_gui import tool
from typing import TYPE_CHECKING, Type, TextIO
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.attribute import ui as attribute_ui

if TYPE_CHECKING:
    from som_gui.module.object_filter.prop import ObjectFilterProperties, ObjectFilterCompareProperties
    from som_gui.module.object_filter import ui
USE_CASE = "Anwedungsfall"
YELLOW = "#897e00"


class ObjectFilter(som_gui.core.tool.ObjectFilter):
    @classmethod
    def set_header_data(cls, header_data: list[list[str, int, int]]):
        prop = cls.get_objectfilter_properties()
        prop.header_data = header_data

    @classmethod
    def get_filter_names(cls):
        prop = cls.get_objectfilter_properties()
        return [li[0] for li in prop.header_data]

    @classmethod
    def get_filter_indexes(cls):
        prop = cls.get_objectfilter_properties()
        return [[li[1], li[2]] for li in prop.header_data]

    @classmethod
    def get_filter_matrix(cls):
        return Project.get().get_filter_matrix()

    @classmethod
    def create_header_data(cls, filter_matrix: list[list[bool]]) -> list[list[str | int]]:
        use_case_list = Project.get().get_use_case_list()
        project_phase_list = Project.get().get_project_phase_list()
        header_data = list()
        for pp_index, pp in enumerate(project_phase_list):
            for uc_index, uc in enumerate(use_case_list):
                if filter_matrix[pp_index][uc_index]:
                    name = f"{pp.name}-{uc.name}"
                    header_data.append([name, pp_index, uc_index])
        return header_data

    @classmethod
    def get_widget(cls):
        return cls.get_objectfilter_properties().object_filter_window.widget

    @classmethod
    def format_object_tree_header(cls):
        header = cls.get_object_tree().header()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    @classmethod
    def get_object_tree(cls):
        return cls.get_objectfilter_properties().object_filter_window.widget.object_tree

    @classmethod
    def get_pset_tree(cls):
        return cls.get_objectfilter_properties().object_filter_window.widget.property_set_tree

    @classmethod
    def get_objectfilter_properties(cls) -> ObjectFilterProperties:
        return som_gui.ObjectFilterProperties

    @classmethod
    def create_window(cls):
        window = cls.get_objectfilter_properties().object_filter_window

        if not window:
            window = object_filter.ui.ObjectFilterWindow()
        cls.get_objectfilter_properties().object_filter_window = window
        return window

    @classmethod
    def reset_use_case_data(cls):
        object_filter_data.refresh()

    @classmethod
    def get_active_use_case(cls):
        proj = Project.get()
        return proj.current_use_case

    @classmethod
    def get_active_use_case_name(cls):
        return cls.get_active_use_case().name

    @classmethod
    def set_use_case(cls, use_case_name: str):
        proj = Project.get()
        uc = proj.get_use_case_by_name(use_case_name)
        if uc is None:
            return
        proj.current_use_case = uc

    @classmethod
    def add_use_case_to_settings_window(cls):
        Project.add_project_setting(cls.get_active_use_case_name,
                                    cls.set_use_case, USE_CASE, cls.get_use_case_name_list)

    @classmethod
    def create_row(cls, entity: SOMcreator.Object | SOMcreator.Attribute | SOMcreator.PropertySet,
                   filter_index_list: list[list[str | int]]):
        entity_item = QStandardItem(entity.name)
        item_list = [entity_item]
        entity_item.setData(entity, CLASS_REFERENCE)
        if isinstance(entity, SOMcreator.Object):
            item_list.append(QStandardItem(entity.ident_value))
        for project_phase_index, use_case_index in filter_index_list:
            item = QStandardItem()
            item.setCheckable(True)
            cs = cls.get_check_state(project_phase_index, use_case_index, entity)
            item.setCheckState(cs)
            item_list.append(item)
        return item_list

    @classmethod
    def get_check_state(cls, project_phase_index: int, use_case_index: int,
                        entity: SOMcreator.Object | SOMcreator.Attribute | SOMcreator.PropertySet):
        prop = cls.get_objectfilter_properties()

        if isinstance(entity, SOMcreator.Object):
            data_dict = prop.object_dict
        elif isinstance(entity, SOMcreator.PropertySet):
            data_dict = prop.pset_dict
        elif isinstance(entity, SOMcreator.Attribute):
            data_dict = prop.attribute_dict
        else:
            data_dict = dict()
        if data_dict.get(entity) is None:
            data_dict[entity] = list()
            for __ in Project.get().get_project_phase_list():
                data_dict[entity].append([True for _ in Project.get().get_use_case_list()])
        check_state = data_dict[entity][project_phase_index][use_case_index]
        if check_state is None:
            check_state = True
        return Qt.CheckState.Checked if check_state else Qt.CheckState.Unchecked

    @classmethod
    def update_object_use_cases(cls):
        prop = cls.get_objectfilter_properties()
        proj = Project.get()
        project_use_case_list = proj.get_use_case_list()
        project_phase_list = proj.get_project_phase_list()
        for obj, filter_matrix in prop.object_dict.items():
            obj: SOMcreator.Object
            for phase_index, use_case_list in enumerate(filter_matrix):
                phase = project_phase_list[phase_index]
                for use_case_index, value in enumerate(use_case_list):
                    use_c = project_use_case_list[use_case_index]
                    obj.set_filter_state(phase, use_c, value)

    @classmethod
    def update_pset_use_cases(cls):
        proj = Project.get()
        project_use_case_list = proj.get_use_case_list()
        project_phase_list = proj.get_project_phase_list()
        for pset, filter_matrix in cls.get_pset_dict().items():
            for phase_index, use_case_list in enumerate(filter_matrix):
                phase = project_phase_list[phase_index]
                for use_case_index, value in enumerate(use_case_list):
                    use_c = project_use_case_list[use_case_index]
                    pset.set_filter_state(phase, use_c, value)

    @classmethod
    def update_attribute_uses_cases(cls):
        prop = cls.get_objectfilter_properties()
        proj = Project.get()
        project_use_case_list = proj.get_use_case_list()
        project_phase_list = proj.get_project_phase_list()
        for attribute, filter_matrix in prop.attribute_dict.items():
            for phase_index, use_case_list in enumerate(filter_matrix):
                phase = project_phase_list[phase_index]
                for use_case_index, value in enumerate(use_case_list):
                    use_c = project_use_case_list[use_case_index]
                    attribute.set_filter_state(phase, use_c, value)

    @classmethod
    def delete_use_case_window(cls) -> QWidget:
        prop = cls.get_objectfilter_properties()
        old_window = prop.object_filter_window
        prop.object_filter_window = None
        prop.active_object = None
        object_filter_data.refresh()
        return old_window

    @classmethod
    def create_tree(cls, entities: set[SOMcreator.Attribute | SOMcreator.Object], parent_item: QStandardItem,
                    filter_index_list: list[[int, int]], pre_header_text_length: int, model: QStandardItemModel,
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
            row = cls.create_row(new_entity, filter_index_list)
            parent_item.appendRow(row)

        for child_row in range(parent_item.rowCount()):
            for child_column, _ in enumerate(filter_index_list, start=pre_header_text_length):
                child_item = parent_item.child(child_row, child_column)
                if child_item is None:
                    child_item = QStandardItem()
                    child_item.setCheckable(True)
                    child_item.setCheckState(Qt.CheckState.Checked)
                    parent_item.setChild(child_row, child_column, child_item)
                cls.update_enable_status(child_item, model)
            class_item = parent_item.child(child_row, 0)
            obj = class_item.data(CLASS_REFERENCE)
            if isinstance(obj, SOMcreator.Object):
                if tree.isExpanded(parent_item.index()) or parent_item == model.invisibleRootItem():
                    cls.create_tree(obj.get_all_children(), class_item, filter_index_list, pre_header_text_length,
                                    model, tree)

    @classmethod
    def get_title_lenght_by_model(cls, model: QStandardItemModel):
        """
        checks if model is objects or pset model and looks up the titles
        """
        object_titles, pset_titles = cls.get_header_texts()
        title_lenght = 0
        if model == cls.get_object_model():
            title_lenght = len(object_titles)
        elif model == cls.get_pset_model():
            title_lenght = len(pset_titles)
        return title_lenght

    @classmethod
    def get_enabled_statuses(cls, index: QModelIndex):
        model: QStandardItemModel = index.model()
        title_lenght = cls.get_title_lenght_by_model(model)
        res = list()
        focus_row = index.row()
        for column, _ in enumerate(cls.get_filter_names(), start=title_lenght):
            item = model.itemFromIndex(index.sibling(focus_row, column))
            res.append(item.isEnabled())
        return res

    @classmethod
    def get_check_statuses(cls, index: QModelIndex) -> list[bool]:
        model: QStandardItemModel = index.model()
        title_lenght = cls.get_title_lenght_by_model(model)
        res = list()
        focus_row = index.row()
        for column, _ in enumerate(cls.get_filter_names(), start=title_lenght):
            item = model.itemFromIndex(index.sibling(focus_row, column))
            res.append(item.checkState() == Qt.CheckState.Checked)
        return res

    @classmethod
    def update_enable_status(cls, item: QStandardItem, model: QStandardItemModel):
        index = item.index()
        parent_index = index.sibling(index.row(), 0).parent()
        parent_item = model.itemFromIndex(parent_index.sibling(parent_index.row(), index.column()))
        if parent_item is None:
            item.setEnabled(True)
        elif not parent_item.isEnabled() or parent_item.checkState() == Qt.CheckState.Unchecked:
            item.setEnabled(False)
        else:
            item.setEnabled(True)

    @classmethod
    def get_active_object(cls):
        return cls.get_objectfilter_properties().active_object

    @classmethod
    def get_index_by_object(cls, obj: SOMcreator.Object) -> QModelIndex:
        def iter_items(parent_item: QStandardItem):
            for child_row in range(parent_item.rowCount()):
                child_item = parent_item.child(child_row, 0)
                if child_item.data(CLASS_REFERENCE) == obj:
                    return child_item
                else:
                    res = iter_items(child_item)
                    if res is not None:
                        return res
            return None

        object_model = cls.get_object_model()
        return iter_items(object_model.invisibleRootItem()).index()

    @classmethod
    def load_use_cases(cls):
        prop = cls.get_objectfilter_properties()
        if not object_filter_data.ObjectFilterData.is_loaded:
            object_filter_data.ObjectFilterData.load()
        prop.use_cases = object_filter_data.ObjectFilterData.data["data_classes"]
        logging.debug(f"Use Cases: {prop.use_cases}")
        object_dict = dict()
        pset_dict = dict()
        attribute_dict = dict()
        for obj in Project.get().get_all_objects():
            object_dict[obj] = obj.get_filter_matrix()
            for pset in obj.get_all_property_sets():
                pset_dict[pset] = pset.get_filter_matrix()
                for attribute in pset.get_all_attributes():
                    attribute_dict[attribute] = attribute.get_filter_matrix()
        prop.object_dict = object_dict
        prop.pset_dict = pset_dict
        prop.attribute_dict = attribute_dict

    @classmethod
    def create_tree_models(cls):
        prop = cls.get_objectfilter_properties()
        object_tree = prop.object_filter_window.widget.object_tree
        object_tree.setModel(QStandardItemModel())
        property_set_tree = prop.object_filter_window.widget.property_set_tree
        model = QStandardItemModel()
        property_set_tree.setModel(model)

    @classmethod
    def get_use_case_name_list(cls) -> list[str]:
        project = tool.Project.get()
        return [uc.name for uc in project.get_use_case_list()]

    @classmethod
    def set_header_labels(cls, model: QStandardItemModel, labels: list[str]):
        model.setHorizontalHeaderLabels(labels)

    @classmethod
    def get_header_texts(cls):
        obj_title = list(som_gui.module.object_filter.constants.OBJECT_TITLES)
        pset_titles = list(som_gui.module.object_filter.constants.PSET_TITLES)
        return obj_title, pset_titles

    @classmethod
    def fill_object_tree(cls, root_objects: list[SOMcreator.Object]) -> None:
        object_header_texts, _ = cls.get_header_texts()
        model = cls.get_object_model()
        use_case_list = cls.get_filter_indexes()
        tree = cls.get_object_tree()
        cls.create_tree(set(root_objects), model.invisibleRootItem(), use_case_list, len(object_header_texts), model,
                        tree)

    @classmethod
    def get_title_count_by_index(cls, index) -> int:
        model = index.model()
        if model == cls.get_object_model():
            return len(som_gui.module.object_filter.constants.OBJECT_TITLES)
        if model == cls.get_pset_model():
            return len(som_gui.module.object_filter.constants.PSET_TITLES)
        return 0

    @classmethod
    def is_object_enabled(cls, index: QModelIndex) -> bool:
        model = index.model()
        return model.itemFromIndex(index).isEnabled()

    @classmethod
    def toggle_checkstate(cls, index: QModelIndex) -> Qt.CheckState:
        old_check_state = cls.get_checkstate(index)
        new_check_state = (
            Qt.CheckState.Unchecked
            if old_check_state in (2, Qt.CheckState.Checked)
            else Qt.CheckState.Checked
        )
        model = index.model()
        model.setData(index, new_check_state, Qt.ItemDataRole.CheckStateRole)
        return new_check_state

    @classmethod
    def get_checkstate(cls, index: QModelIndex) -> int:
        return index.data(Qt.ItemDataRole.CheckStateRole)

    @classmethod
    def get_object_model(cls) -> QStandardItemModel:
        prop = cls.get_objectfilter_properties()
        return prop.object_filter_window.widget.object_tree.model()

    @classmethod
    def get_pset_model(cls) -> QStandardItemModel:
        prop = cls.get_objectfilter_properties()
        return prop.object_filter_window.widget.property_set_tree.model()

    @classmethod
    def is_tree_clicked(cls) -> bool:
        prop = cls.get_objectfilter_properties()
        return prop.tree_is_clicked

    @classmethod
    def tree_activate_click_drag(cls, index: QModelIndex):
        prop = cls.get_objectfilter_properties()
        prop.tree_is_clicked = True
        checkstate = index.data(Qt.ItemDataRole.CheckStateRole)
        prop.active_check_state = checkstate

    @classmethod
    def tree_move_click_drag(cls, index: QModelIndex):
        if index.column() < cls.get_title_count_by_index(index):
            return
        active_checkstate = cls.get_active_checkstate()
        if active_checkstate is None:
            return
        model = index.model()
        if not model.itemFromIndex(index).isEnabled():
            return
        model.setData(index, active_checkstate, Qt.ItemDataRole.CheckStateRole)

    @classmethod
    def tree_release_click_drag(cls, index: QModelIndex):
        prop = cls.get_objectfilter_properties()
        prop.tree_is_clicked = False
        prop.active_check_state = None

    @classmethod
    def get_active_checkstate(cls) -> Qt.CheckState:
        prop = cls.get_objectfilter_properties()
        return prop.active_check_state

    @classmethod
    def resize_tree(cls, tree: QTreeView):
        columns = tree.model().columnCount()
        for index in range(columns):
            tree.resizeColumnToContents(index)

    @classmethod
    def get_linked_data(cls, index: QModelIndex):
        focus_index = index.sibling(index.row(), 0)
        return focus_index.data(CLASS_REFERENCE)

    @classmethod
    def set_active_object(cls, obj: SOMcreator.Object):
        prop = cls.get_objectfilter_properties()
        prop.active_object = obj
        cls.update_active_object_label()

    @classmethod
    def update_active_object_label(cls):
        prop = cls.get_objectfilter_properties()
        active_object = prop.active_object
        label = prop.object_filter_window.widget.label_object
        if active_object is None:
            label.hide()
        else:
            label.show()
            label.setText(f"{active_object.name} ({active_object.ident_value})")

    @classmethod
    def update_pset_tree(cls):
        active_object = cls.get_active_object()
        prop = cls.get_objectfilter_properties()

        pset_tree = prop.object_filter_window.widget.property_set_tree
        if active_object is None:
            pset_tree.setModel(QStandardItemModel())
            return

        def handle_psets(property_sets: set[SOMcreator.PropertySet]):
            old_pset_dict = {
                root_item.child(index, 0).data(CLASS_REFERENCE): index
                for index in range(root_item.rowCount())
            }
            old_property_sets = set(old_pset_dict.keys())
            new_property_sets = property_sets.difference(old_property_sets)
            delete_property_sets = old_property_sets.difference(property_sets)
            for pset in reversed(sorted(delete_property_sets, key=lambda o: old_pset_dict[o])):
                row_index = old_pset_dict[pset]
                root_item.removeRow(row_index)

            for new_pset in new_property_sets:
                row = cls.create_row(new_pset, filter_index_list)
                root_item.appendRow(row)

            for child_row in range(root_item.rowCount()):
                for child_column, enable_state in enumerate(sub_enable_states, start=len(pset_header_texts)):
                    child_item = root_item.child(child_row, child_column)
                    if child_item is None:
                        child_item = QStandardItem()
                        child_item.setCheckable(True)
                        child_item.setCheckState(Qt.CheckState.Checked)
                        root_item.setChild(child_row, child_column, child_item)
                    child_item.setEnabled(enable_state)
                pset: SOMcreator.PropertySet = root_item.child(child_row, 0).data(CLASS_REFERENCE)
                cls.create_tree(pset.get_all_attributes(), root_item.child(child_row, 0), filter_index_list,
                                len(pset_header_texts), model, cls.get_pset_tree())

        _, pset_header_texts = cls.get_header_texts()
        model = cls.get_pset_model()
        filter_index_list = cls.get_filter_indexes()
        root_item = model.invisibleRootItem()
        active_object_index = cls.get_index_by_object(active_object)
        check_states = cls.get_check_statuses(active_object_index)
        enable_states = cls.get_enabled_statuses(active_object_index)
        sub_enable_states = [all((c, e)) for c, e in zip(check_states, enable_states)]
        handle_psets(set(active_object.get_all_property_sets()))

    @classmethod
    def get_object_dict(cls):
        prop = cls.get_objectfilter_properties()
        return prop.object_dict

    @classmethod
    def get_pset_dict(cls):
        prop = cls.get_objectfilter_properties()
        return prop.pset_dict

    @classmethod
    def get_attribute_dict(cls):
        prop = cls.get_objectfilter_properties()
        return prop.attribute_dict

    @classmethod
    def update_pset_data(cls):
        model = cls.get_pset_model()
        filter_indexes = cls.get_filter_indexes()
        pset_dict = cls.get_pset_dict()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            pset = index.data(CLASS_REFERENCE)
            check_statuses = cls.get_check_statuses(index)
            for [phase_index, use_case_index], status in zip(filter_indexes, check_statuses):
                pset_dict[pset][phase_index][use_case_index] = status

    @classmethod
    def update_attribute_data(cls):
        model = cls.get_pset_model()
        filter_indexes = cls.get_filter_indexes()
        attribute_dict = cls.get_attribute_dict()
        for row in range(model.rowCount()):
            pset_index = model.index(row, 0)
            for attribute_row in range(model.rowCount(pset_index)):
                index = model.index(attribute_row, 0, pset_index)
                attribute = index.data(CLASS_REFERENCE)
                check_statuses = cls.get_check_statuses(index)
                for [phase_index, use_case_index], status in zip(filter_indexes, check_statuses):
                    attribute_dict[attribute][phase_index][use_case_index] = status

    @classmethod
    def update_object_data(cls, obj: SOMcreator.Object):
        index = cls.get_index_by_object(obj)
        filter_indexes = cls.get_filter_indexes()
        object_dict = cls.get_object_dict()
        check_statuses = cls.get_check_statuses(index)
        for [phase_index, use_case_index], status in zip(filter_indexes, check_statuses):
            object_dict[obj][phase_index][use_case_index] = status

    @classmethod
    def connect_settings_widget(cls, widget: ui.SettingsWidget):
        widget.ui.cb_phase.currentIndexChanged.connect(trigger.settings_combobox_changed)
        widget.ui.cb_usecase.currentIndexChanged.connect(trigger.settings_combobox_changed)

    @classmethod
    def set_settings_widget(cls, widget: ui.SettingsWidget):
        cls.get_objectfilter_properties().settings_widget = widget

    @classmethod
    def get_settings_widget(cls) -> ui.SettingsWidget:
        return cls.get_objectfilter_properties().settings_widget

    @classmethod
    def get_allowed_usecases_by_phase(cls, project: SOMcreator.Project, phase: SOMcreator.classes.Phase):
        usecase_list = project.get_use_case_list()
        filter_matrix = project.get_filter_matrix()
        phase_index = project.get_phase_index(phase)
        return [uc for uc, state in zip(usecase_list, filter_matrix[phase_index]) if state]

    @classmethod
    def get_allowed_phases_by_usecase(cls, project: SOMcreator.Project, usecase: SOMcreator.classes.UseCase):
        phase_list = project.get_project_phase_list()
        usecase_index = project.get_use_case_index(usecase)
        filter_matrix = project.get_filter_matrix()
        return [phase for phase, value_list in zip(phase_list, filter_matrix) if value_list[usecase_index]]


class ObjectFilterCompare(som_gui.core.tool.ObjectFilterCompare):
    @classmethod
    def get_properties(cls) -> ObjectFilterCompareProperties:
        return som_gui.ObjectFilterCompareProperties

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.usecase_list = list()
        prop.use_case_indexes = list()
        prop.phase_list = list()
        prop.phase_indexes = list()
        prop.projects = [None, None]
        prop.widget = None

    @classmethod
    def create_tree_selection_trigger(cls, widget: attribute_ui.AttributeWidget):
        widget.widget.tree_widget_object.itemSelectionChanged.connect(
            lambda: trigger.filter_tab_object_tree_selection_changed(widget))

    @classmethod
    def find_matching_usecases(cls, proj0: SOMcreator.Project = None, proj1: SOMcreator.Project = None):
        proj0 = proj0 or cls.get_project(0)
        proj1 = proj1 or cls.get_project(1)

        if not cls.get_usecase_list():
            usecases = set(proj0.get_use_case_list()).intersection(set(proj1.get_use_case_list()))
            cls.set_usecase_list(sorted(usecases, key=lambda x: x.name))
            for usecase in cls.get_usecase_list():
                index0 = proj0.get_use_case_index(usecase)
                index1 = proj1.get_use_case_index(usecase)
                cls.add_use_case_index_tuple((index0, index1))
        return cls.get_usecase_list()

    @classmethod
    def find_matching_phases(cls, proj0: SOMcreator.Project = None, proj1: SOMcreator.Project = None):
        proj0 = proj0 or cls.get_project(0)
        proj1 = proj1 or cls.get_project(1)

        if not cls.get_properties().phase_list:
            phases = set(proj0.get_project_phase_list()).intersection(set(proj1.get_project_phase_list()))
            cls.set_phase_list(sorted(phases, key=lambda x: x.name))
            for phase in cls.get_phase_list():
                index0 = proj0.get_phase_index(phase)
                index1 = proj1.get_phase_index(phase)
                cls.add_phase_index_tuple((index0, index1))
        return cls.get_phase_list()

    @classmethod
    def append_collumns(cls, object_tree_widget: QTreeWidget, pset_tree_widget: QTreeWidget):
        object_header_text = cls.get_existing_header_texts(object_tree_widget)
        pset_header_text = cls.get_existing_header_texts(pset_tree_widget)

        match_list = cls.get_match_list()
        extra_header_texts = [f"{pp.name} - {uc.name}" for uc, pp in match_list]
        count = len(extra_header_texts)

        object_tree_widget.setColumnCount(object_tree_widget.columnCount() + count)
        pset_tree_widget.setColumnCount(pset_tree_widget.columnCount() + count)
        object_tree_widget.setHeaderLabels(object_header_text + extra_header_texts)
        pset_tree_widget.setHeaderLabels(pset_header_text + extra_header_texts)

    @classmethod
    def get_filter_list(cls, entity0, entity1) -> list[tuple[None | bool, None | bool]]:
        filter_list = list()
        for column, [usecase, phase] in enumerate(cls.get_match_list(), start=2):
            filter_list.append(
                (entity0.get_filter_state(phase, usecase) if entity0 is not None else None,
                 entity1.get_filter_state(phase, usecase) if entity1 is not None else None))
        return filter_list

    @classmethod
    def are_all_filters_identical(cls, filter_list: list[tuple[None | bool, None | bool]]) -> bool:
        return all(f0 == f1 for f0, f1 in filter_list if f0 is not None and f1 is not None)

    @classmethod
    def are_objects_identical(cls, obj0: SOMcreator.Object, obj1: SOMcreator.Object) -> bool:
        filter_list = cls.get_filter_list(obj0, obj1)
        objects_are_identical = cls.are_all_filters_identical(filter_list)
        if not objects_are_identical:
            return False
        pset_lists = tool.AttributeCompare.get_pset_list(obj0)
        if pset_lists is None:
            return True
        for p0, p1 in pset_lists:
            if not cls.are_psets_identical(p0, p1):
                return False
        return True

    @classmethod
    def are_psets_identical(cls, pset0: SOMcreator.PropertySet, pset1: SOMcreator.PropertySet) -> bool:
        filter_list = cls.get_filter_list(pset0, pset1)
        all_psets_are_identical = cls.are_all_filters_identical(filter_list)
        if not all_psets_are_identical:
            return False
        attribute_lists = tool.AttributeCompare.get_attribute_list(pset0)
        if attribute_lists is None:
            return True
        for a0, a1 in attribute_lists:
            if not cls.are_attributes_identical(a0, a1):
                return False
        return True

    @classmethod
    def are_attributes_identical(cls, attribute0: SOMcreator.Attribute, attribute1: SOMcreator.Attribute):
        filter_list = cls.get_filter_list(attribute0, attribute1)
        return cls.are_all_filters_identical(filter_list)

    @classmethod
    def fill_tree_with_checkstates(cls, item: QTreeWidgetItem) -> None:
        tree = item.treeWidget()
        entity_0, entity_1 = tool.AttributeCompare.get_entities_from_item(item)
        filter_list = cls.get_filter_list(entity_0, entity_1)
        for column, filter_state in enumerate(filter_list, start=2):
            widget = cls.create_combobox_widget(filter_state[0], filter_state[1])
            tree.setItemWidget(item, column, widget)
            if filter_state[0] != filter_state[1]:
                cls.set_tree_item_column_color(item, column, YELLOW)

        for child_index in range(item.childCount()):
            cls.fill_tree_with_checkstates(item.child(child_index))

    @classmethod
    def make_header_wordwrap(cls, tree: QTreeWidget) -> None:
        """because of long header texts make header wordwrap"""
        header = attribute_ui.WordWrapHeaderView(Qt.Orientation.Horizontal)
        tree.setHeader(header)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap)

    @classmethod
    def style_object_tree(cls, item: QTreeWidgetItem):
        entity_0: SOMcreator.Object = item.data(0, CLASS_REFERENCE)
        entity_1: SOMcreator.Object = item.data(1, CLASS_REFERENCE)
        for column, filter_state in enumerate(cls.get_filter_list(entity_0, entity_1), start=2):
            if filter_state[0] != filter_state[1]:
                cls.set_tree_item_column_color(item, column, YELLOW)

        if not cls.are_objects_identical(entity_0, entity_1):
            cls.set_tree_item_column_color(item, 0, YELLOW)

        for child_index in range(item.childCount()):
            cls.style_object_tree(item.child(child_index))

    @classmethod
    def create_combobox_widget(cls, checkstate0: bool | None, checkstate1: bool | None):
        widget = QWidget()
        layout = QHBoxLayout()
        cb0 = QCheckBox()
        if checkstate0 is not None:
            cb0.setChecked(checkstate0)
        cb1 = QCheckBox()
        cb1.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        if checkstate1 is not None:
            cb1.setChecked(checkstate1)
        layout.addWidget(cb0)
        layout.addWidget(cb1)
        widget.setLayout(layout)
        cb0.setEnabled(False)
        cb1.setEnabled(False)
        return widget

    @classmethod
    def export_write_statechange(cls, file: TextIO, type_name: str, filter_list, indent: int):
        matches = cls.get_match_list()
        for index, (f0, f1) in enumerate(filter_list):
            if f0 == f1:
                continue
            usecase, phase = matches[index]
            file.write(f"{'   ' * indent}{type_name} [{usecase.name}][{phase.name}] state changed from {f0} to {f1}\n")

    @classmethod
    def export_object_filter_differences(cls, file: TextIO, attribute_compare: Type[tool.AttributeCompare]):
        project_0 = cls.get_project(0)
        object_dict = attribute_compare.get_object_dict()
        for obj0 in sorted(project_0.get_all_objects(), key=lambda x: x.name):
            obj1 = object_dict[obj0]
            if obj1 is None:
                continue
            if cls.are_objects_identical(obj0, obj1):
                continue
            filter_list = cls.get_filter_list(obj0, obj1)
            file.write(f"\nObject '{obj0.name}' ({obj0.ident_value}):\n")
            cls.export_write_statechange(file, "Object", filter_list, 1)
            pset_list = attribute_compare.get_properties().pset_lists.get(obj0)
            cls.export_pset_filter_differences(file, pset_list, attribute_compare)

    @classmethod
    def export_pset_filter_differences(cls, file, pset_list, attribute_compare: Type[tool.AttributeCompare]):
        if pset_list is None:
            return
        for p0, p1 in sorted(pset_list, key=lambda x: x[0].name if x[0] is not None else "aaa"):
            if p0 is None or p1 is None:
                continue
            if cls.are_psets_identical(p0, p1):
                continue
            file.write(f"   PropertySet '{p0.name}':\n")
            filter_list = cls.get_filter_list(p0, p1)
            cls.export_write_statechange(file, "PropertySet", filter_list, 2)
            attribute_list = attribute_compare.get_properties().attributes_lists.get(p0)
            cls.export_attribute_filter_differences(file, attribute_list)

    @classmethod
    def export_attribute_filter_differences(cls, file, attribute_list):
        matches = cls.get_match_list()

        if attribute_list is None:
            return
        for a0, a1 in sorted(attribute_list, key=lambda x: x[0].name if x[0] is not None else "aaa"):
            if a0 is None or a1 is None:
                continue
            if cls.are_attributes_identical(a0, a1):
                continue
            filter_list = cls.get_filter_list(a0, a1)
            for index, (f0, f1) in enumerate(filter_list):
                if f0 == f1:
                    continue
                usecase, phase = matches[index]
                use_case_phase_text = f"[{usecase.name}][{phase.name}]"
                text = "      Attribut {0:30} {1:30} state changed from {2:5} to {3:5}\n"
                file.write(text.format(f"'{a0.name}'", use_case_phase_text, str(f0), str(f1)))

    # GETTER & SETTER

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.Project:
        return cls.get_properties().projects[index]

    @classmethod
    def get_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = attribute_ui.AttributeWidget()
            cls.get_properties().widget.widget.table_widget_values.hide()
        return cls.get_properties().widget

    @classmethod
    def get_object_tree(cls):
        return cls.get_widget().widget.tree_widget_object

    @classmethod
    def get_usecase_list(cls) -> list[SOMcreator.classes.UseCase]:
        return cls.get_properties().usecase_list

    @classmethod
    def set_usecase_list(cls, usecase_list: list[SOMcreator.classes.UseCase]):
        cls.get_properties().usecase_list = usecase_list

    @classmethod
    def get_use_case_index_list(cls) -> list[tuple[int, int]]:
        return cls.get_properties().use_case_indexes

    @classmethod
    def add_use_case_index_tuple(cls, value: tuple[int, int]):
        cls.get_properties().use_case_indexes.append(value)

    @classmethod
    def get_phase_list(cls) -> list[SOMcreator.classes.Phase]:
        return cls.get_properties().phase_list

    @classmethod
    def set_phase_list(cls, phase_list: list[SOMcreator.classes.Phase]):
        cls.get_properties().phase_list = phase_list

    @classmethod
    def get_phase_index_list(cls) -> list[tuple[int, int]]:
        return cls.get_properties().phase_indexes

    @classmethod
    def add_phase_index_tuple(cls, value: tuple[int, int]):
        cls.get_properties().phase_indexes.append(value)

    @classmethod
    def get_match_list(cls) -> list[tuple[SOMcreator.classes.UseCase, SOMcreator.classes.Phase]]:
        usecases = cls.get_usecase_list()
        phases = cls.get_phase_list()
        if not cls.get_properties().match_list:
            cls.get_properties().match_list = [(usecase, phase) for usecase in usecases for phase in phases]
        return cls.get_properties().match_list

    @classmethod
    def get_extra_column_count(cls):
        return len(cls.get_match_list())

    @classmethod
    def get_existing_header_texts(cls, tree_widget: QTreeWidget) -> list[str]:
        header = tree_widget.headerItem()
        return [header.text(index) for index in range(header.columnCount())]

    @classmethod
    def set_tree_item_column_color(cls, item: QTreeWidgetItem, column: int, color: str):
        tree = item.treeWidget()
        index = tree.indexFromItem(item, 0)
        tool.AttributeCompare.set_branch_color(tree, index, color)
        color = QColor(color)
        item.setBackground(column, color)
        item.setData(CLASS_REFERENCE + 1, column, 1)
        item.setBackground(0, color)
        item.setBackground(1, color)
        item.setData(0, CLASS_REFERENCE + 1, 1)

