from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtGui import QBrush, QPalette, QColor, QIcon
from PySide6.QtCore import Qt, QModelIndex
from som_gui import tool
import SOMcreator
from som_gui.module.compare import ui
import som_gui.core.tool
import som_gui
from PySide6.QtWidgets import QTableWidgetItem, QSizePolicy, QCheckBox, QTreeWidgetItem, QTreeWidget, QTableWidget, \
    QWidget, QHBoxLayout
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.compare import trigger

if TYPE_CHECKING:
    from som_gui.module.compare.prop import CompareAttributesProperties, CompareWindowProperties, \
        CompareProjectSelectProperties, ObjectFilterCompareProperties

style_list = [
    [None, [0, 1]],
    ["#897e00", [0, 1]],  # Yellow
    ["#006605", [1]],  # green
    ["#840002", [0]]  # red

]


class CompareProjectSelector(som_gui.core.tool.CompareProjectSelector):
    @classmethod
    def get_properties(cls) -> CompareProjectSelectProperties:
        return som_gui.CompareProjectSelectProperties

    @classmethod
    def create_project_select_dialog(cls):
        dialog = ui.ProjectSelectDialog()
        cls.get_properties().proj_select_dialog = dialog
        cls.get_properties().layout_proj0 = dialog.widget.layout_top
        cls.get_properties().layout_proj1 = dialog.widget.layout_bottom
        cls.get_properties().label_project = dialog.widget.label_project
        cls.get_properties().layout_input = dialog.widget.layout_input
        return dialog

    @classmethod
    def get_project_select_dialog(cls) -> ui.ProjectSelectDialog:
        return cls.get_properties().proj_select_dialog

    @classmethod
    def connect_project_select_dialog(cls, dialog: ui.ProjectSelectDialog):
        dialog.widget.button.clicked.connect(trigger.project_button_clicked)
        dialog.widget.button_switch.clicked.connect(trigger.switch_button_clicked)

    @classmethod
    def fill_project_select_dialog(cls, project, open_path):
        cls.set_project_select_path(open_path)
        name = f"{project.name} v{project.version}"
        cls.get_properties().label_project.setText(name)

    @classmethod
    def get_project_layouts(cls):
        prop = cls.get_properties()
        return prop.layout_proj0, prop.layout_proj1

    @classmethod
    def get_input_layout(cls):
        return cls.get_properties().layout_input

    @classmethod
    def get_project_label(cls):
        return cls.get_properties().label_project

    @classmethod
    def toggle_current_project_as_input(cls):
        prop = cls.get_properties()
        prop.is_current_proj_input = not prop.is_current_proj_input

    @classmethod
    def is_current_project_input(cls):
        return cls.get_properties().is_current_proj_input

    @classmethod
    def set_project_select_path(cls, project_path: str):
        cls.get_project_select_dialog().widget.line_edit.setText(project_path)

    @classmethod
    def get_project_select_path(cls) -> str:
        return cls.get_project_select_dialog().widget.line_edit.text()

    @classmethod
    def accept_clicked(cls):
        trigger.accept_clicked()


class AttributeCompare(som_gui.core.tool.Compare):
    @classmethod
    def get_properties(cls) -> CompareAttributesProperties:
        return som_gui.CompareAttributesProperties

    @classmethod
    def get_level(cls, index):
        parent = index.parent()
        level = 1
        while parent.isValid():
            parent = parent.parent()
            level += 1
        return level

    @classmethod
    def get_branch_color(cls, index: QModelIndex):
        color = index.data(CLASS_REFERENCE + 1)
        return QColor(color) if isinstance(color, str) else None

    @classmethod
    def set_branch_color(cls, tree: QTreeWidget, index: QModelIndex, color: str):
        model = tree.model()
        model.setData(index, color, CLASS_REFERENCE + 1)

        if index.parent().isValid():
            cls.set_branch_color(tree, index.parent(), color)

    @classmethod
    def get_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = ui.AttributeWidget()
        return cls.get_properties().widget

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.projects = [None, None]
        prop.uuid_dicts = [None, None]
        prop.ident_dicts = [None, None]
        prop.object_dicts = [None, None]
        prop.missing_objects = [None, None]
        prop.object_tree_item_dict = dict()
        prop.pset_lists = dict()
        prop.attributes_lists = dict()
        prop.values_lists = dict()
        prop.widget = None

    @classmethod
    def create_tree_selection_trigger(cls, widget: ui.AttributeWidget):
        widget.widget.tree_widget_object.itemSelectionChanged.connect(
            lambda: trigger.object_tree_selection_changed(widget))
        widget.widget.tree_widget_propertysets.itemSelectionChanged.connect(
            lambda: trigger.pset_tree_selection_changed(widget))

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.Project:
        return cls.get_properties().projects[index]

    @classmethod
    def get_uuid_dict(cls, index=1) -> dict:
        uuid_dict = cls.get_properties().uuid_dicts[index]
        project = cls.get_project(index)
        if uuid_dict is None:
            d = {hi.uuid: hi for hi in project.get_all_hirarchy_items()}
            cls.get_properties().uuid_dicts[index] = d
        return cls.get_properties().uuid_dicts[index]

    @classmethod
    def get_ident_dict(cls, index=1) -> dict:
        uuid_dict = cls.get_properties().ident_dicts[index]
        project = cls.get_project(index)
        if uuid_dict is None:
            d = {obj.ident_value: obj for obj in project.get_all_objects()}
            cls.get_properties().ident_dicts[index] = d
        return cls.get_properties().ident_dicts[index]

    @classmethod
    def find_matching_object(cls, obj: SOMcreator.Object, index=1) -> SOMcreator.Object | None:
        uuid_dict = cls.get_uuid_dict(index)
        ident_dict = cls.get_ident_dict(index)

        uuid_match = uuid_dict.get(obj.uuid)
        if uuid_match:
            return uuid_match
        ident_match = ident_dict.get(obj.ident_value)

        if ident_match:
            return ident_match
        return None

    @classmethod
    def find_matching_entity(cls, entity_0, uuid_dict1,
                             name_dict1) -> SOMcreator.PropertySet | SOMcreator.Attribute | None:
        if entity_0.uuid in uuid_dict1:
            return uuid_dict1[entity_0.uuid]
        if entity_0.name in name_dict1:
            return name_dict1[entity_0.name]
        return None

    @classmethod
    def compare_objects(cls, obj0: None | SOMcreator.Object, obj1: None | SOMcreator.Object):
        property_set_uuid_dict1 = {p.uuid: p for p in obj1.get_all_property_sets()} if obj1 is not None else dict()
        property_set_name_dict1 = {p.name: p for p in obj1.get_all_property_sets()} if obj1 is not None else dict()
        pset_list = list()

        missing_property_sets1 = list(obj1.get_all_property_sets()) if obj1 is not None else []
        if obj0 is not None:
            for property_set0 in obj0.get_all_property_sets():
                match = cls.find_matching_entity(property_set0, property_set_uuid_dict1, property_set_name_dict1)
                if match is not None:
                    missing_property_sets1.remove(match)
                    pset_list.append((property_set0, match))
                    cls.compare_psets(property_set0, match)
                else:
                    pset_list.append((property_set0, None))

        for property_set1 in missing_property_sets1:
            pset_list.append((None, property_set1))
        if obj0 is not None:
            cls.get_properties().pset_lists[obj0] = pset_list
        if obj1 is not None:
            cls.get_properties().pset_lists[obj1] = pset_list

    @classmethod
    def compare_psets(cls, pset0: SOMcreator.PropertySet, pset1: SOMcreator.PropertySet):
        attribute_uuid_dict1 = {a.uuid: a for a in pset1.get_all_attributes()}
        attribute_name_dict1 = {a.name: a for a in pset1.get_all_attributes()}
        missing_attributes1 = list(pset1.get_all_attributes())
        attributes_list = list()
        for attribute0 in pset0.get_all_attributes():
            match = cls.find_matching_entity(attribute0, attribute_uuid_dict1, attribute_name_dict1)
            if match is not None:
                missing_attributes1.remove(match)
                attributes_list.append((attribute0, match))
            else:
                attributes_list.append((attribute0, None))
        for attribute1 in missing_attributes1:
            attributes_list.append((None, attribute1))

        for a1, a2 in attributes_list:
            cls.compare_attributes(a1, a2)

        cls.get_properties().attributes_lists[pset0] = attributes_list
        cls.get_properties().attributes_lists[pset1] = attributes_list

    @classmethod
    def compare_attributes(cls, attribute0: SOMcreator.Attribute, attribute1: SOMcreator.Attribute):
        if attribute0 is not None:
            values0 = set(attribute0.value)
        else:
            values0 = set()
        if attribute1 is not None:
            values1 = set(attribute1.value)
        else:
            values1 = set()

        unique0 = values0.difference(values1)
        main = values0.intersection(values1)
        unique1 = values1.difference(values0)

        value_list = [(v, v) for v in main] + [(v, None) for v in unique0] + [(None, v) for v in unique1]
        if attribute0 is not None:
            cls.get_properties().values_lists[attribute0] = value_list
        if attribute1 is not None:
            cls.get_properties().values_lists[attribute1] = value_list

    @classmethod
    def create_object_dicts(cls):
        if cls.get_properties().missing_objects[0] is not None:
            return
        project_0 = cls.get_project(0)
        project_1 = cls.get_project(1)
        missing_objects_0 = list()
        missing_objects_1 = list(project_1.get_all_objects())
        object_dict0 = dict()
        object_dict1 = dict()
        for obj in project_0.get_all_objects():
            match = cls.find_matching_object(obj, 1)
            if match is not None:
                object_dict0[obj] = match
                object_dict1[match] = obj
                missing_objects_1.remove(match)
                cls.compare_objects(obj, match)
            else:
                object_dict0[obj] = None
                missing_objects_0.append(obj)
                cls.compare_objects(obj, None)
        for obj in missing_objects_1:
            object_dict1[obj] = None
            cls.compare_objects(None, obj)

        cls.get_properties().missing_objects = [missing_objects_0, missing_objects_1]
        cls.get_properties().object_dicts = [object_dict0, object_dict1]

    @classmethod
    def get_object_dict(cls, index=1) -> dict:
        return cls.get_properties().object_dicts[index]

    @classmethod
    def get_missing_objects(cls, index=1) -> list:
        return cls.get_properties().missing_objects[index]

    @classmethod
    def add_object_to_item(cls, obj: SOMcreator.Object, item: QTreeWidgetItem, index: int):
        start_index = index
        ident_text = f"({obj.ident_value})" if obj.ident_value else ""
        text = f"{obj.name} {ident_text}"
        item.setText(start_index, text)
        item.setData(start_index, CLASS_REFERENCE, obj)
        cls.get_properties().object_tree_item_dict[obj] = item

    @classmethod
    def fill_object_tree_layer(cls, objects: list[SOMcreator.Object], parent_item: QTreeWidgetItem, add_missing: bool):
        obj_dict0, obj_dict1 = cls.get_object_dict(0), cls.get_object_dict(1)

        for obj in objects:
            match_obj = obj_dict0.get(obj)
            item = QTreeWidgetItem()
            cls.add_object_to_item(obj, item, 0)
            if match_obj:
                cls.add_object_to_item(match_obj, item, 1)

            if match_obj is not None or add_missing:
                parent_item.addChild(item)
            cls.fill_object_tree_layer(list(obj.get_all_children()), item, add_missing)

    @classmethod
    def fill_object_tree(cls, tree: QTreeWidget, add_missing: bool = True):
        proj0, proj1 = cls.get_project(0), cls.get_project(1)
        tree_root = tree.invisibleRootItem()
        root_objects = tool.Project.get_root_objects(False, proj0)
        cls.fill_object_tree_layer(root_objects, tree_root, add_missing)
        if add_missing:
            cls.add_missing_objects_to_tree(tree, tool.Project.get_root_objects(False, proj1))

    @classmethod
    def find_existing_parent(cls, obj: SOMcreator.Object):
        object_tree_item_dict = cls.get_properties().object_tree_item_dict
        parent = obj.parent
        while parent is not None:
            if parent in object_tree_item_dict:
                return object_tree_item_dict[parent]
            parent = parent.parent
        return None

    @classmethod
    def add_missing_objects_to_tree(cls, tree: QTreeWidget, root_objects: list[SOMcreator.Object]):
        missing_objects = cls.get_missing_objects(1)
        for obj in root_objects:
            if obj in missing_objects:
                parent = cls.find_existing_parent(obj)
                parent = parent if parent is not None else tree.invisibleRootItem()
                item = QTreeWidgetItem()
                cls.add_object_to_item(obj, item, 1)
                parent.addChild(item)
            cls.add_missing_objects_to_tree(tree, list(obj.get_all_children()))

    @classmethod
    def fill_pset_tree(cls, tree: QTreeWidget, obj: SOMcreator.Object, add_missing: bool = True):

        pset_list = cls.get_properties().pset_lists.get(obj)
        root = tree.invisibleRootItem()
        for child_index in reversed(range(tree.invisibleRootItem().childCount())):
            root.removeChild(root.child(child_index))

        if pset_list is None:
            return

        for pset0, pset1 in pset_list:
            item = QTreeWidgetItem()
            if pset0:
                item.setText(0, pset0.name)
                item.setData(0, CLASS_REFERENCE, pset0)
            if pset1:
                item.setText(1, pset1.name)
                item.setData(1, CLASS_REFERENCE, pset1)

            if (pset0 and pset1) or add_missing:
                root.addChild(item)
                cls.add_attribute_to_psetitem(item, add_missing)

    @classmethod
    def add_attribute_to_psetitem(cls, pset_item: QTreeWidgetItem, add_missing: bool):
        pset0: SOMcreator.PropertySet | None = pset_item.data(0, CLASS_REFERENCE)
        pset1: SOMcreator.PropertySet | None = pset_item.data(1, CLASS_REFERENCE)

        if pset0 is not None and pset1 is None:
            attribute_list = [(a, None) for a in pset0.get_all_attributes()]
        elif pset1 is not None and pset0 is None:
            attribute_list = [(None, a) for a in pset1.get_all_attributes()]
        else:
            pset0: SOMcreator.PropertySet
            attribute_list = cls.get_properties().attributes_lists.get(pset0)

        if attribute_list is None:
            return

        attribute_list: list[tuple[SOMcreator.Attribute | None, SOMcreator.Attribute | None]]

        for attribute0, attribute1 in attribute_list:
            item = QTreeWidgetItem()
            if attribute0 is not None:
                item.setText(0, attribute0.name)
                item.setData(0, CLASS_REFERENCE, attribute0)
            if attribute1 is not None:
                item.setText(1, attribute1.name)
                item.setData(1, CLASS_REFERENCE, attribute1)

            if (attribute0 and attribute1) or add_missing:
                pset_item.addChild(item)

    @classmethod
    def get_selected_item_from_tree(cls,
                                    tree) -> SOMcreator.PropertySet | SOMcreator.Attribute | SOMcreator.Object | None:
        selected_items = tree.selectedItems()
        if not selected_items:
            return None
        item = selected_items[0]
        data = item.data(0, CLASS_REFERENCE)
        if data is None:
            data = item.data(1, CLASS_REFERENCE)
        return data

    @classmethod
    def fill_value_table(cls, table: QTableWidget, attribute: SOMcreator.Attribute):

        value_list = cls.get_properties().values_lists.get(attribute)
        table.setRowCount(0)

        if value_list is None:
            return

        for value0, value1 in value_list:
            item0 = QTableWidgetItem()
            item1 = QTableWidgetItem()

            if value0 is not None:
                item0.setText(value0)

            if value1 is not None:
                item1.setText(value1)

            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, item0)
            table.setItem(table.rowCount() - 1, 1, item1)

    @classmethod
    def are_attributes_identical(cls, attribute0: SOMcreator.Attribute, attribute1: SOMcreator.Attribute):
        if attribute0 is None or attribute1 is None:
            return False
        values = set(attribute0.value) == set(attribute1.value)
        data_types = attribute0.data_type == attribute1.data_type
        value_types = attribute0.value_type == attribute1.value_type
        names = attribute0.name == attribute1.name
        return all((values, data_types, value_types, names))

    @classmethod
    def are_property_sets_identical(cls, property_set0: SOMcreator.PropertySet, property_set1: SOMcreator.PropertySet):
        if property_set0 is None or property_set1 is None:
            return False
        names = property_set0.name == property_set1.name
        attribute_list = cls.get_properties().attributes_lists.get(property_set0)
        if not attribute_list:
            return False
        attributes_are_matching = all(cls.are_attributes_identical(a0, a1) for a0, a1 in attribute_list)
        return all((names, attributes_are_matching))

    @classmethod
    def are_objects_identical(cls, object0: SOMcreator.Object, object1: SOMcreator.Object):
        if object0 is None or object1 is None:
            return
        names = object0.name == object1.name
        identifier = object0.ident_value == object1.ident_value
        property_set_list = cls.get_properties().pset_lists.get(object0)
        if not property_set_list:
            return False
        psets_are_matching = all(cls.are_property_sets_identical(p0, p1) for p0, p1 in property_set_list)
        return all((names, identifier, psets_are_matching))

    @classmethod
    def set_tree_row_color(cls, item: QTreeWidgetItem, style_index):
        item.setData(0, CLASS_REFERENCE + 1, style_index)
        color, column_list = style_list[style_index]
        for column in column_list:
            brush = QBrush(QColor(color)) if color is not None else QPalette().base()
            item.setBackground(column, brush)

    @classmethod
    def style_parent_item(cls, item: QTreeWidgetItem, style: int):
        parent = item.parent()
        if parent is None or parent == item.treeWidget().invisibleRootItem():
            return
        parent_style_index = parent.data(0, CLASS_REFERENCE + 1)
        if parent_style_index < style:
            cls.set_tree_row_color(parent, style)
            cls.style_parent_item(parent, style)

    @classmethod
    def style_tree_item(cls, item: QTreeWidgetItem):
        obj0 = item.data(0, CLASS_REFERENCE)
        obj1 = item.data(1, CLASS_REFERENCE)

        if obj0 is None:
            style = 2
        elif obj1 is None:
            style = 3
        else:
            if isinstance(obj0, SOMcreator.Object):
                compare_func = cls.are_objects_identical
            elif isinstance(obj0, SOMcreator.PropertySet):
                compare_func = cls.are_property_sets_identical
            else:
                compare_func = cls.are_attributes_identical

            style = 0 if compare_func(obj0, obj1) else 1

        cls.set_tree_row_color(item, style)
        if (isinstance(obj0, SOMcreator.Object) or isinstance(obj1, SOMcreator.Object)) and style > 0:
            parent = item.parent()
            index = item.treeWidget().indexFromItem(parent, 0)
            cls.set_branch_color(item.treeWidget(), index, style_list[1][0])

        for child_index in range(item.childCount()):
            if not isinstance(obj0, SOMcreator.Attribute):
                cls.style_tree_item(item.child(child_index))

    @classmethod
    def set_header_labels(cls, object_tree, pset_tree, value_table, h0: str, h1: str):
        object_tree.setHeaderLabels([h0, h1])
        pset_tree.setHeaderLabels([h0, h1])
        value_table.setHorizontalHeaderLabels([h0, h1])

    @classmethod
    def get_header_name_from_project(cls, project: SOMcreator.Project):
        return f"{project.name} v{project.version}"

    @classmethod
    def get_object_tree(cls, widget: ui.AttributeWidget):
        return widget.widget.tree_widget_object

    @classmethod
    def get_pset_tree(cls, widget: ui.AttributeWidget):
        return widget.widget.tree_widget_propertysets

    @classmethod
    def get_value_table(cls, widget: ui.AttributeWidget):
        return widget.widget.table_widget_values


class CompareWindow(som_gui.core.tool.CompareWindow):
    @classmethod
    def get_properties(cls) -> CompareWindowProperties:
        return som_gui.CompareWindowProperties

    @classmethod
    def add_tab(cls, name: str, widget, init_func, _tool):
        prop = cls.get_properties()
        prop.names.append(name)
        prop.widgets.append(widget)
        prop.init_functions.append(init_func)
        prop.tools.append(_tool)

    @classmethod
    def create_window(cls):
        cls.get_properties().window = ui.CompareDialog()
        return cls.get_window()

    @classmethod
    def get_window(cls) -> ui.CompareDialog:
        return cls.get_properties().window

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_tabwidget(cls):
        return cls.get_window().widget.tabWidget

    @classmethod
    def init_tabs(cls, project0, project1):
        names = cls.get_properties().names
        widgets = cls.get_properties().widgets
        init_functions = cls.get_properties().init_functions
        tab_widget = cls.get_tabwidget()
        for name, widget_getter, init_func in zip(names, widgets, init_functions):
            tab_widget.addTab(widget_getter(), QIcon(), name)
            init_func(project0, project1)

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.window = None
        for _tool in cls.get_properties().tools:
            _tool.reset()


class ObjectFilterCompare(som_gui.core.tool.ObjectFilterCompare):
    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.Project:
        return cls.get_properties().projects[index]

    @classmethod
    def get_properties(cls) -> ObjectFilterCompareProperties:
        return som_gui.ObjectFilterCompareProperties

    @classmethod
    def get_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = ui.AttributeWidget()
        return cls.get_properties().widget

    @classmethod
    def get_object_tree(cls):
        return cls.get_widget().widget.tree_widget_object

    @classmethod
    def create_tree_selection_trigger(cls, widget: ui.AttributeWidget):
        widget.widget.tree_widget_object.itemSelectionChanged.connect(
            lambda: trigger.filter_tab_object_tree_selection_changed(widget))

    @classmethod
    def get_matching_usecases(cls, proj0: SOMcreator.Project = None, proj1: SOMcreator.Project = None):
        if proj0 is None:
            proj0 = cls.get_project(0)
        if proj1 is None:
            proj1 = cls.get_project(1)
        if not cls.get_properties().usecase_list:
            usecases = set(proj0.get_use_case_list()).intersection(set(proj1.get_use_case_list()))
            usecases = sorted(usecases, key=lambda x: x.name)

            cls.get_properties().usecase_list = usecases
            for usecase in usecases:
                cls.get_properties().use_case_indexes.append(
                    [proj0.get_use_case_index(usecase), proj1.get_use_case_index(usecase)])
        return cls.get_properties().usecase_list

    @classmethod
    def get_matching_phases(cls, proj0: SOMcreator.Project = None, proj1: SOMcreator.Project = None):
        if proj0 is None:
            proj0 = cls.get_project(0)
        if proj1 is None:
            proj1 = cls.get_project(1)
        if not cls.get_properties().phase_list:
            phases = set(proj0.get_project_phase_list()).intersection(set(proj1.get_project_phase_list()))
            phases = sorted(phases, key=lambda x: x.name)

            cls.get_properties().phase_list = phases
            for phase in phases:
                cls.get_properties().phase_indexes.append(
                    [proj0.get_phase_index(phase), proj1.get_phase_index(phase)])
        return cls.get_properties().phase_list

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.usecase_list = list()
        prop.use_case_indexes = list()
        prop.phase_list = list()
        prop.phase_indexes = list()
        prop.column_count = None
        prop.projects = [None, None]
        prop.widget = None


    @classmethod
    def append_collumns(cls, count: int, object_tree_widget: QTreeWidget, pset_tree_widget: QTreeWidget):
        object_header = object_tree_widget.headerItem()
        object_header_text = [object_header.text(index) for index in range(object_header.columnCount())]

        pset_header = pset_tree_widget.headerItem()
        pset_header_text = [pset_header.text(index) for index in range(pset_header.columnCount())]

        match_list = cls.get_match_list()
        header_texts = [f"{pp.name} - {uc.name}" for uc, pp in match_list]

        object_tree_widget.setColumnCount(object_tree_widget.columnCount() + count)
        pset_tree_widget.setColumnCount(pset_tree_widget.columnCount() + count)
        object_tree_widget.setHeaderLabels(object_header_text + header_texts)
        pset_tree_widget.setHeaderLabels(pset_header_text + header_texts)

    @classmethod
    def get_extra_column_count(cls):
        if cls.get_properties().column_count is None:
            usecases = cls.get_matching_usecases()
            phases = cls.get_matching_phases()
            cls.get_properties().column_count = len(usecases) * len(phases)
        return cls.get_properties().column_count

    @classmethod
    def get_match_list(cls):
        usecases = cls.get_matching_usecases()
        phases = cls.get_matching_phases()
        if not cls.get_properties().match_list:
            cls.get_properties().match_list = [[usecase, phase] for usecase in usecases for phase in phases]
        return cls.get_properties().match_list

    @classmethod
    def get_filter_list(cls, entity0: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute,
                        entity1: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute) -> list[
        tuple[None | bool, None | bool]]:
        filter_list = list()
        for column, [usecase, phase] in enumerate(cls.get_match_list(), start=2):
            filter_state = [None, None]
            if entity0 is not None:
                filter_state[0] = entity0.get_filter_state(phase, usecase)
            if entity1 is not None:
                filter_state[1] = entity1.get_filter_state(phase, usecase)
            filter_list.append(tuple(filter_state))
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
        pset_lists = tool.AttributeCompare.get_properties().pset_lists.get(obj0)
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
        attribute_lists = tool.AttributeCompare.get_properties().attributes_lists.get(pset0)
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
    def fill_tree_with_checkstates(cls, item: QTreeWidgetItem):
        tree = item.treeWidget()
        entity_0: SOMcreator.Object = item.data(0, CLASS_REFERENCE)
        entity_1: SOMcreator.Object = item.data(1, CLASS_REFERENCE)
        filter_list = cls.get_filter_list(entity_0, entity_1)
        for column, filter_state in enumerate(filter_list, start=2):
            widget = cls._create_combobox_widget(filter_state[0], filter_state[1])
            tree.setItemWidget(item, column, widget)
            if filter_state[0] != filter_state[1]:
                cls.set_tree_item_column_color(item, column, style_list[1][0])

        for child_index in range(item.childCount()):
            cls.fill_tree_with_checkstates(item.child(child_index))

    @classmethod
    def _create_combobox_widget(cls, cs0: bool | None, cs1: bool | None):
        widget = QWidget()
        layout = QHBoxLayout()
        cb0 = QCheckBox()
        if cs0 is not None:
            cb0.setChecked(cs0)
        cb1 = QCheckBox()
        cb1.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        if cs1 is not None:
            cb1.setChecked(cs1)
        layout.addWidget(cb0)
        layout.addWidget(cb1)
        widget.setLayout(layout)
        cb0.setEnabled(False)
        cb1.setEnabled(False)
        return widget

    @classmethod
    def set_wordwrap_header(cls, tree: QTreeWidget):
        header = ui.WordWrapHeaderView(Qt.Orientation.Horizontal)
        tree.setHeader(header)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap)

    @classmethod
    def set_tree_item_column_color(cls, item: QTreeWidgetItem, column, color):
        tree = item.treeWidget()
        index = tree.indexFromItem(item, 0)
        tool.AttributeCompare.set_branch_color(tree, index, color)
        color = QColor(color)
        item.setBackground(column, color)
        item.setData(CLASS_REFERENCE + 1, column, 1)
        item.setBackground(0, color)
        item.setBackground(1, color)
        item.setData(0, CLASS_REFERENCE + 1, 1)

    @classmethod
    def style_object_tree(cls, item: QTreeWidgetItem):
        entity_0: SOMcreator.Object = item.data(0, CLASS_REFERENCE)
        entity_1: SOMcreator.Object = item.data(1, CLASS_REFERENCE)
        for column, filter_state in enumerate(cls.get_filter_list(entity_0, entity_1), start=2):
            if filter_state[0] != filter_state[1]:
                cls.set_tree_item_column_color(item, column, style_list[1][0])

        if not cls.are_objects_identical(entity_0, entity_1):
            cls.set_tree_item_column_color(item, 0, style_list[1][0])

        for child_index in range(item.childCount()):
            cls.style_object_tree(item.child(child_index))
