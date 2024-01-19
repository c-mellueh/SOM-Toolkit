import logging

import SOMcreator
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import QTreeView, QMenu, QInputDialog, QLineEdit, QWidget
import som_gui.core.tool
from som_gui.tool.project import Project
from som_gui.module.use_case import data as use_case_data
import som_gui.module.use_case.constants
import som_gui
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from typing import TYPE_CHECKING
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui.module.use_case.prop import UseCaseProperties

USE_CASE = "Anwedungsfall"

class UseCase(som_gui.core.tool.UseCase):
    @classmethod
    def reset_use_case_data(cls):
        use_case_data.refresh()

    @classmethod
    def set_active_use_case(cls, value: str):
        proj = Project.get()
        proj.current_use_case = value

    @classmethod
    def get_active_use_case(cls):
        proj = Project.get()
        return proj.current_use_case

    @classmethod
    def set_use_case(cls, value: str):
        proj = Project.get()
        proj.current_use_case = value

    @classmethod
    def add_use_case_to_settings_window(cls):
        Project.add_project_setting(cls.get_active_use_case,
                                    cls.set_active_use_case, USE_CASE, cls.get_use_case_list)

    @classmethod
    def create_row(cls, entity: SOMcreator.Object | SOMcreator.Attribute | SOMcreator.PropertySet, use_case_list):
        entity_item = QStandardItem(entity.name)
        item_list = [entity_item]
        entity_item.setData(entity, CLASS_REFERENCE)
        if isinstance(entity, SOMcreator.Object):
            item_list.append(QStandardItem(entity.ident_value))
        for use_case in use_case_list:
            item = QStandardItem()
            item.setCheckable(True)
            cs = cls.get_use_case_state(use_case, entity)
            item.setCheckState(cs)
            item_list.append(item)
        return item_list

    @classmethod
    def get_use_case_state(cls, use_case_name,
                           entity: SOMcreator.Object | SOMcreator.Attribute | SOMcreator.PropertySet):
        prop: UseCaseProperties = som_gui.UseCaseProperties

        if isinstance(entity, SOMcreator.Object):
            data_dict = prop.object_dict
        elif isinstance(entity, SOMcreator.PropertySet):
            data_dict = prop.pset_dict
        elif isinstance(entity, SOMcreator.Attribute):
            data_dict = prop.attribute_dict
        if data_dict.get(entity) is None:
            data_dict[entity] = {name: True for name in cls.get_use_case_list()}

        check_state = data_dict[entity].get(use_case_name)
        if check_state is None:
            check_state = True

        return Qt.CheckState.Checked if check_state else Qt.CheckState.Unchecked

    @classmethod
    def update_object_use_cases(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        for obj, use_case_dict in prop.object_dict.items():
            for use_case_name, state in use_case_dict.items():
                obj.set_use_case(use_case_name, state)

    @classmethod
    def update_pset_use_cases(cls):
        for pset, use_case_dict in cls.get_pset_dict().items():
            for use_case_name, state in use_case_dict.items():
                pset.set_use_case(use_case_name, state)

    @classmethod
    def update_attribute_uses_cases(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        for attribute, use_case_dict in prop.attribute_dict.items():
            for use_case_name, state in use_case_dict.items():
                attribute.set_use_case(use_case_name, state)

    @classmethod
    def update_project_use_cases(cls):
        use_case_list = cls.get_use_case_list()
        proj = Project.get()

        old_use_cases = proj.get_use_case_list()
        for index, old_use_case in enumerate(old_use_cases):
            if index != 0:
                proj.remove_use_case(old_use_case)
        proj.rename_use_case(old_use_cases[0], use_case_list[0])
        for use_case in use_case_list[1:]:
            proj.add_use_case(use_case)

    @classmethod
    def delete_use_case_window(cls) -> QWidget:
        prop: UseCaseProperties = som_gui.UseCaseProperties
        old_window = prop.use_case_window
        prop.use_case_window = None
        prop.active_object = None
        use_case_data.refresh()
        return old_window

    @classmethod
    def add_use_case(cls, use_case_name: str) -> None:
        prop: UseCaseProperties = som_gui.UseCaseProperties
        prop.use_cases.append(use_case_name)
        for data_dict in [prop.object_dict, prop.pset_dict, prop.attribute_dict]:
            for use_case_dict in data_dict.values():
                use_case_dict[use_case_name] = True


    @classmethod
    def remove_use_case(cls, use_case_index: int):
        def remove_use_case_column(index: int, model: QStandardItemModel):
            title_length = cls.get_title_lenght_by_model(model)
            column = title_length + index
            model.removeColumn(column)

        prop: UseCaseProperties = som_gui.UseCaseProperties
        use_case_text = prop.use_cases[use_case_index]
        prop.use_cases.pop(use_case_index)
        remove_use_case_column(use_case_index, cls.get_object_model())
        remove_use_case_column(use_case_index, cls.get_pset_model())
        for data_dict in [prop.object_dict, prop.pset_dict, prop.attribute_dict]:
            for use_case_dict in data_dict.values():
                use_case_dict.pop(use_case_text)

    @classmethod
    def get_new_use_case_name(cls, standard_name: str):
        def loop_name(new_name):
            if new_name in existing_names:
                if new_name == standard_name:
                    return loop_name(f"{new_name}_1")
                index = int(new_name[-1])
                return loop_name(f"{new_name[:-1]}{index + 1}")
            return new_name

        existing_names = cls.get_use_case_list()
        return loop_name(standard_name)

    @classmethod
    def request_rename_use_case_name(cls, old_name):
        prop = som_gui.UseCaseProperties
        active_window = prop.use_case_window
        new_name, ok = QInputDialog.getText(active_window, "Anwendungsfall umbenennen", "Neuer Name:",
                                            QLineEdit.EchoMode.Normal, old_name)
        if not ok:
            return None
        return new_name

    @classmethod
    def rename_use_case(cls, use_case_index: int, new_name: str) -> None:
        prop: UseCaseProperties = som_gui.UseCaseProperties
        old_name = prop.use_cases[use_case_index]
        prop.use_cases[use_case_index] = new_name
        for data_dict in [prop.object_dict, prop.pset_dict, prop.attribute_dict]:
            for use_case_dict in data_dict.values():
                use_case_dict[new_name] = use_case_dict[old_name]
                use_case_dict.pop(old_name)

    @classmethod
    def create_context_menu(cls, global_pos, action_dict):
        """
        action_dict: dict of action name and collectable function
        """
        menu = QMenu()
        actions = list()
        for action_name, action_function in action_dict.items():
            action = QAction(action_name)
            actions.append(action)
            menu.addAction(action)
            action.triggered.connect(action_function)
        menu.exec(global_pos)

    @classmethod
    def get_object_tree_view(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        window = prop.use_case_window
        if window is None:
            return None
        return window.widget.object_tree

    @classmethod
    def create_tree(cls, entities: set[SOMcreator.Attribute | SOMcreator.Object], parent_item: QStandardItem,
                    use_case_list,
                    pre_header_text_length: int, model: QStandardItemModel):
        existing_entities_dict = {parent_item.child(index, 0).data(CLASS_REFERENCE): index for index in
                                  range(parent_item.rowCount())}
        old_entities = set(existing_entities_dict.keys())
        new_entities = entities.difference(old_entities)
        delete_entities = old_entities.difference(entities)
        for entity in reversed(sorted(delete_entities, key=lambda o: existing_entities_dict[o])):
            row_index = existing_entities_dict[entity]
            parent_item.removeRow(row_index)

        for new_entity in sorted(new_entities, key=lambda x: x.name):
            row = cls.create_row(new_entity, use_case_list)
            parent_item.appendRow(row)

        for child_row in range(parent_item.rowCount()):
            for child_column, _ in enumerate(use_case_list, start=pre_header_text_length):
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
                cls.create_tree(obj.get_all_children(), class_item, use_case_list, pre_header_text_length, model)

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
        for column, _ in enumerate(cls.get_use_case_list(), start=title_lenght):
            item = model.itemFromIndex(index.sibling(focus_row, column))
            res.append(item.isEnabled())
        return res

    @classmethod
    def get_check_statuses(cls, index: QModelIndex) -> list[bool]:
        model: QStandardItemModel = index.model()
        title_lenght = cls.get_title_lenght_by_model(model)
        res = list()
        focus_row = index.row()
        for column, _ in enumerate(cls.get_use_case_list(), start=title_lenght):
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
        return som_gui.UseCaseProperties.active_object

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
        prop: UseCaseProperties = som_gui.UseCaseProperties
        if not use_case_data.UseCaseData.is_loaded:
            use_case_data.UseCaseData.load()
        prop.use_cases = use_case_data.UseCaseData.data["data_classes"]
        logging.debug(f"Use Cases: {prop.use_cases}")
        object_dict = dict()
        pset_dict = dict()
        attribute_dict = dict()
        for obj in Project.get().get_all_objects():
            object_dict[obj] = obj.get_use_case_dict()
            for pset in obj.get_all_property_sets():
                pset_dict[pset] = pset.get_use_case_dict()
                for attribute in pset.get_all_attributes():
                    attribute_dict[attribute] = attribute.get_use_case_dict()

        prop.object_dict = object_dict
        prop.pset_dict = pset_dict
        prop.attribute_dict = attribute_dict

    @classmethod
    def create_tree_models(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        object_tree = prop.use_case_window.widget.object_tree
        object_tree.setModel(QStandardItemModel())
        property_set_tree = prop.use_case_window.widget.property_set_tree
        model = QStandardItemModel()
        property_set_tree.setModel(model)

    @classmethod
    def get_use_case_list(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.use_cases

    @classmethod
    def set_header_labels(cls, model: QStandardItemModel, labels: list[str]):
        model.setHorizontalHeaderLabels(labels)

    @classmethod
    def get_header_texts(cls):
        obj_title = list(som_gui.module.use_case.constants.OBJECT_TITLES)
        pset_titles = list(som_gui.module.use_case.constants.PSET_TITLES)
        return obj_title, pset_titles

    @classmethod
    def fill_object_tree(cls, root_objects: list[SOMcreator.Object]) -> None:

        object_header_texts, _ = cls.get_header_texts()
        model = cls.get_object_model()
        use_case_list = cls.get_use_case_list()
        cls.create_tree(set(root_objects), model.invisibleRootItem(), use_case_list, len(object_header_texts), model)

    @classmethod
    def get_title_count_by_index(cls, index) -> int:
        model = index.model()
        if model == cls.get_object_model():
            return len(som_gui.module.use_case.constants.OBJECT_TITLES)
        if model == cls.get_pset_model():
            return len(som_gui.module.use_case.constants.PSET_TITLES)
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
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.use_case_window.widget.object_tree.model()

    @classmethod
    def get_pset_model(cls) -> QStandardItemModel:
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.use_case_window.widget.property_set_tree.model()

    @classmethod
    def is_tree_clicked(cls) -> bool:
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.tree_is_clicked

    @classmethod
    def tree_activate_click_drag(cls, index: QModelIndex):
        prop: UseCaseProperties = som_gui.UseCaseProperties
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
        prop: UseCaseProperties = som_gui.UseCaseProperties
        prop.tree_is_clicked = False
        prop.active_check_state = None
        focus_index = index.sibling(index.row(), 0)

    @classmethod
    def get_active_checkstate(cls) -> Qt.CheckState:
        prop: UseCaseProperties = som_gui.UseCaseProperties
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
        prop: UseCaseProperties = som_gui.UseCaseProperties
        prop.active_object = obj
        cls.update_active_object_label()

    @classmethod
    def update_active_object_label(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        active_object = prop.active_object
        label = prop.use_case_window.widget.label_object
        if active_object is None:
            label.hide()
        else:
            label.show()
            label.setText(f"{active_object.name} ({active_object.ident_value})")

    @classmethod
    def update_pset_tree(cls):
        active_object = cls.get_active_object()
        prop: UseCaseProperties = som_gui.UseCaseProperties

        pset_tree = prop.use_case_window.widget.property_set_tree
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
                row = cls.create_row(new_pset, use_case_list)
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
                pset = root_item.child(child_row, 0).data(CLASS_REFERENCE)
                cls.create_tree(pset.get_all_attributes(), root_item.child(child_row, 0), use_case_list,
                                len(pset_header_texts), model)

        _, pset_header_texts = cls.get_header_texts()
        model = cls.get_pset_model()
        use_case_list = cls.get_use_case_list()
        root_item = model.invisibleRootItem()
        active_object_index = cls.get_index_by_object(active_object)
        check_states = cls.get_check_statuses(active_object_index)
        enable_states = cls.get_enabled_statuses(active_object_index)
        sub_enable_states = [all((c, e)) for c, e in zip(check_states, enable_states)]
        handle_psets(set(active_object.get_all_property_sets()))

    @classmethod
    def get_object_dict(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.object_dict

    @classmethod
    def get_pset_dict(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.pset_dict

    @classmethod
    def get_attribute_dict(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.attribute_dict

    @classmethod
    def update_pset_data(cls):
        model = cls.get_pset_model()
        use_cases = cls.get_use_case_list()
        pset_dict = cls.get_pset_dict()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            pset = index.data(CLASS_REFERENCE)
            check_statuses = cls.get_check_statuses(index)
            use_case_dict = {use_case: status for use_case, status in zip(use_cases, check_statuses)}
            pset_dict[pset] = use_case_dict

    @classmethod
    def update_attribute_data(cls):
        model = cls.get_pset_model()
        use_cases = cls.get_use_case_list()
        attribute_dict = cls.get_attribute_dict()
        for row in range(model.rowCount()):
            pset_index = model.index(row, 0)
            for attribute_row in range(model.rowCount(pset_index)):
                index = model.index(attribute_row, 0, pset_index)
                attribute = index.data(CLASS_REFERENCE)
                check_statuses = cls.get_check_statuses(index)
                use_case_dict = {use_case: status for use_case, status in zip(use_cases, check_statuses)}
                attribute_dict[attribute] = use_case_dict

    @classmethod
    def update_object_data(cls, obj: SOMcreator.Object):
        index = cls.get_index_by_object(obj)
        use_cases = cls.get_use_case_list()
        object_dict = cls.get_object_dict()
        check_statuses = cls.get_check_statuses(index)
        use_case_dict = {use_case: status for use_case, status in zip(use_cases, check_statuses)}
        object_dict[obj] = use_case_dict
