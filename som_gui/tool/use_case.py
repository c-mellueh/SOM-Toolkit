import SOMcreator
from PySide6.QtCore import Qt
import som_gui.core.tool
from som_gui.tool.project import Project
from som_gui.module.use_case.data import UseCaseData
import som_gui
from PySide6.QtGui import QStandardItemModel, QStandardItem
from typing import TYPE_CHECKING
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui.module.use_case.prop import UseCaseProperties


class UseCase(som_gui.core.tool.UseCase):
    @classmethod
    def create_use_case(cls):
        pass

    @classmethod
    def load_use_cases(cls):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        object_tree = prop.use_case_window.widget.object_tree
        object_tree.setModel(QStandardItemModel())
        property_set_tree = prop.use_case_window.widget.property_set_tree
        property_set_tree.setModel(QStandardItemModel())

    @classmethod
    def get_use_case_list(cls):
        if not UseCaseData.is_loaded:
            UseCaseData.load()
        return UseCaseData.data["data_classes"]

    @classmethod
    def set_header_labels(cls, labels: list[str]):
        prop: UseCaseProperties = som_gui.UseCaseProperties
        object_tree = prop.use_case_window.widget.object_tree
        object_tree.model().setHorizontalHeaderLabels(labels)

    @classmethod
    def get_object_dict(cls) -> dict[SOMcreator.Object, dict[str, bool]]:
        objects = Project.get_all_objects()
        return {obj: obj.get_use_case_dict() for obj in objects}

    @classmethod
    def fill_object_tree(cls, root_objects: list[SOMcreator.Object]):
        def create_row(obj: SOMcreator.Object):
            obj_item = QStandardItem(obj.name)
            obj_item.setData(obj, CLASS_REFERENCE)
            item_list = [obj_item, QStandardItem(obj.ident_value)]
            for use_case in use_case_list:
                item = QStandardItem()
                item.setCheckable(True)
                cs = (
                    Qt.CheckState.Checked
                    if obj.get_use_case_state(use_case)
                    else Qt.CheckState.Unchecked
                )
                item.setCheckState(cs)
                item_list.append(item)
            return item_list

        def iter_tree(objects: set[SOMcreator.Object], parent_item: QStandardItem):
            existing_objects_dict = {
                parent_item.child(index, 0).data(CLASS_REFERENCE): index
                for index in range(parent_item.rowCount())
            }
            existing_objects = set(existing_objects_dict.keys())
            new_objects = objects.difference(existing_objects)
            delete_objects = existing_objects.difference(objects)

            for obj in reversed(
                sorted(delete_objects, key=lambda o: existing_objects_dict[o])
            ):
                row_index = existing_objects_dict[obj]
                parent_item.removeRow(row_index)

            for new_object in new_objects:
                row = create_row(new_object)
                parent_item.appendRow(row)
                iter_tree(new_object.children, row[0])

        prop: UseCaseProperties = som_gui.UseCaseProperties
        model = prop.use_case_window.widget.object_tree.model()
        use_case_list = cls.get_use_case_list()
        iter_tree(set(root_objects), model.invisibleRootItem())
