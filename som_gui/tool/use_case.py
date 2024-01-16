import SOMcreator
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import QTreeView
import som_gui.core.tool
from som_gui.tool.project import Project
from som_gui.module.use_case import data as use_case_data
import som_gui.module.use_case.constants
import som_gui
from PySide6.QtGui import QStandardItemModel, QStandardItem
from typing import TYPE_CHECKING
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui.module.use_case.prop import UseCaseProperties


def create_row(entity: SOMcreator.Object | SOMcreator.Attribute | SOMcreator.PropertySet, use_case_list):
    entity_item = QStandardItem(entity.name)
    item_list = [entity_item]
    entity_item.setData(entity, CLASS_REFERENCE)
    if isinstance(entity, SOMcreator.Object):
        item_list.append(QStandardItem(entity.ident_value))

    for use_case in use_case_list:
        item = QStandardItem()
        item.setCheckable(True)
        cs = Qt.CheckState.Checked if entity.get_use_case_state(use_case) else Qt.CheckState.Unchecked
        item.setCheckState(cs)
        item_list.append(item)
    return item_list


class UseCase(som_gui.core.tool.UseCase):
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

        for new_entity in new_entities:
            row = create_row(new_entity, use_case_list)
            parent_item.appendRow(row)

        for child_row in range(parent_item.rowCount()):
            for child_column, _ in enumerate(use_case_list, start=pre_header_text_length):
                child_item = parent_item.child(child_row, child_column)
                cls.update_enable_status(child_item, model)
            class_item = parent_item.child(child_row, 0)
            obj = class_item.data(CLASS_REFERENCE)
            if isinstance(obj, SOMcreator.Object):
                cls.create_tree(obj.get_all_children(), class_item, use_case_list, pre_header_text_length, model)

    @classmethod
    def get_title_lenght_by_model(cls, model: QStandardItemModel):
        """
        checks if model is object or pset model and looks up the titles
        """
        object_titles, pset_titles = cls.get_header_texts()
        title_lenght = 0
        if model == cls.get_object_model():
            title_lenght = len(object_titles)
        elif model == cls.get_pset_model():
            title_lenght = len(pset_titles)
        return title_lenght

    @classmethod
    def get_enabled_status(cls, index: QModelIndex):
        model: QStandardItemModel = index.model()
        title_lenght = cls.get_title_lenght_by_model(model)
        res = list()
        focus_row = index.row()
        for column, _ in enumerate(cls.get_use_case_list(), start=title_lenght):
            item = model.itemFromIndex(index.sibling(focus_row, column))
            res.append(item.isEnabled())
        return res

    @classmethod
    def get_check_status(cls, index: QModelIndex):
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
    def create_use_case(cls):
        use_case_data.refresh()

    @classmethod
    def load_use_cases(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        object_tree = prop.use_case_window.widget.object_tree
        object_tree.setModel(QStandardItemModel())
        property_set_tree = prop.use_case_window.widget.property_set_tree
        property_set_tree.setModel(QStandardItemModel())

    @classmethod
    def get_use_case_list(cls):
        if not use_case_data.UseCaseData.is_loaded:
            use_case_data.UseCaseData.load()
        return use_case_data.UseCaseData.data["data_classes"]

    @classmethod
    def set_header_labels(cls, model: QStandardItemModel, labels: list[str]):
        model.setHorizontalHeaderLabels(labels)

    @classmethod
    def get_header_texts(cls):
        obj_title = list(som_gui.module.use_case.constants.OBJECT_TITLES)
        pset_titles = list(som_gui.module.use_case.constants.PSET_TITLES)
        return obj_title, pset_titles

    @classmethod
    def get_object_dict(cls) -> dict[SOMcreator.Object, dict[str, bool]]:
        objects = Project.get_all_objects()
        return {obj: obj.get_use_case_dict() for obj in objects}

    @classmethod
    def fill_object_tree(cls, root_objects: list[SOMcreator.Object]) -> None:

        def iter_tree(objects: set[SOMcreator.Object], parent_item: QStandardItem):
            old_object_dict = {parent_item.child(index, 0).data(CLASS_REFERENCE): index for index in
                               range(parent_item.rowCount())}
            old_objects = set(old_object_dict.keys())
            existing_objects = objects.intersection(old_objects)
            new_objects = objects.difference(old_objects)
            delete_objects = old_objects.difference(objects)

            for obj in reversed(
                    sorted(delete_objects, key=lambda o: old_object_dict[o])
            ):
                row_index = old_object_dict[obj]
                parent_item.removeRow(row_index)

            for new_object in new_objects:
                row = create_row(new_object, use_case_list)
                parent_item.appendRow(row)
                iter_tree(new_object.children, row[0])

            for existing_object in existing_objects:
                row_index = old_object_dict[existing_object]
                iter_tree(existing_object.children, parent_item.child(row_index, 0))
            if parent_item == model.invisibleRootItem():
                return
            for child_row in range(parent_item.rowCount()):
                for child_column, _ in enumerate(use_case_list, start=len(object_header_texts)):
                    cls.update_enable_status(parent_item.child(child_row, child_column), model)

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
        if isinstance(focus_index.data(CLASS_REFERENCE), SOMcreator.Object):
            cls.object_tree_clicked(focus_index)

    @classmethod
    def get_active_checkstate(cls) -> Qt.CheckState:
        prop: UseCaseProperties = som_gui.UseCaseProperties
        return prop.active_check_state

    @classmethod
    def object_tree_clicked(cls, index):
        pass

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
                row = create_row(new_pset, use_case_list)
                root_item.appendRow(row)

            for child_row in range(root_item.rowCount()):
                for child_column, enable_state in enumerate(sub_enable_states, start=len(pset_header_texts)):
                    root_item.child(child_row, child_column).setEnabled(enable_state)
                pset = root_item.child(child_row, 0).data(CLASS_REFERENCE)
                cls.create_tree(pset.get_all_attributes(), root_item.child(child_row, 0), use_case_list,
                                len(pset_header_texts), model)

        _, pset_header_texts = cls.get_header_texts()
        model = cls.get_pset_model()
        use_case_list = cls.get_use_case_list()
        root_item = model.invisibleRootItem()
        active_object_index = cls.get_index_by_object(active_object)
        check_states = cls.get_check_status(active_object_index)
        enable_states = cls.get_enabled_status(active_object_index)
        sub_enable_states = [all((c, e)) for c, e in zip(check_states, enable_states)]
        handle_psets(set(active_object.get_all_property_sets()))
