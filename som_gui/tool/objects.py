from __future__ import annotations

import logging
import copy as cp
import uuid

import som_gui.core.tool
import som_gui.tool as tool
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget, QAbstractItemView, QLineEdit, QCompleter, QMenu
from PySide6.QtCore import Qt, QPoint
import som_gui
from typing import TYPE_CHECKING, TypedDict, Callable
from SOMcreator.Template import IFC_4_1

if TYPE_CHECKING:
    from som_gui.module.objects.prop import ObjectProperties, ContextMenuDict
    from som_gui.main_window import MainWindow


class ObjectDataDict(TypedDict):
    name: str
    is_group: bool
    abbreviation: str
    ident_pset_name: str
    ident_attribute_name: str
    ident_value: str
    ifc_mappings: list[str]


class Objects(som_gui.core.tool.Object):
    @classmethod
    def autofit_tree(cls):
        if cls.get_object_properties().first_paint:
            cls.resize_tree()
            cls.get_object_properties().first_paint = False

    @classmethod
    def resize_tree(cls):
        tree = cls.get_object_tree()
        for col in reversed(range(tree.columnCount())):
            tree.resizeColumnToContents(col)

    @classmethod
    def group_objects(cls, parent: SOMcreator.Object, children: set[SOMcreator.Object]):
        for child in children:
            parent.add_child(child)

    @classmethod
    def create_object(cls, data_dict: ObjectDataDict):
        name = data_dict["name"]
        is_group = data_dict["is_group"]
        abbreviation = data_dict.get("abbreviation")
        ident_pset_name = data_dict.get("ident_pset_name")
        ident_attribute_name = data_dict.get("ident_attribute_name")
        ident_value = data_dict.get("ident_value")
        ifc_mappings = data_dict.get("ifc_mappings")

        if ident_pset_name and ident_attribute_name and ident_value and not is_group:
            if not cls.identifier_is_allowed(ident_value):
                return som_gui.module.objects.IDENT_ISSUE, None
            if not cls.abbreviation_is_allowed(abbreviation):
                return som_gui.module.objects.ABBREV_ISSUE, None
            pset = SOMcreator.PropertySet(ident_pset_name)
            attribute = SOMcreator.Attribute(pset, ident_attribute_name, value=[ident_value],
                                             value_type=SOMcreator.value_constants.LABEL)
            obj = SOMcreator.Object(name, attribute, project=tool.Project.get())
        else:
            id = str(uuid.uuid4())
            obj = SOMcreator.Object(name, id, uuid=id, project=tool.Project.get())
        if ifc_mappings:
            obj.ifc_mapping = ifc_mappings
        if abbreviation:
            obj.abbreviation = abbreviation
        return som_gui.module.objects.OK, obj

    @classmethod
    def create_context_menu(cls):
        menu = QMenu()
        prop = cls.get_object_properties()
        selected_items = cls.get_selected_items()
        menu_list = prop.context_menu_list
        if len(selected_items) == 1:
            menu_list = filter(lambda d: d["on_single_select"], menu_list)
        if len(selected_items) > 1:
            menu_list = filter(lambda d: d["on_multi_select"], menu_list)
        for menu_entry in menu_list:
            menu_entry["action"] = menu.addAction(menu_entry["display_name"])
            menu_entry["action"].triggered.connect(menu_entry["function"])
        return menu

    @classmethod
    def get_selected_objects(cls) -> list[SOMcreator.Object]:
        selected_items = cls.get_selected_items()
        return [cls.get_object_from_item(item) for item in selected_items]

    @classmethod
    def delete_object(cls, obj: SOMcreator.Object, recursive: bool = False):
        # TODO: Refactor NodeWindow so nodes delete automatically
        def delete_nodes(o: SOMcreator.Object):
            for aggregation in list(o.aggregations):
                node = som_gui.MainUi.window.graph_window.aggregation_dict().get(aggregation)
                node.delete(recursive)
            if recursive:
                for child in o.get_all_children():
                    delete_nodes(child)

        delete_nodes(obj)
        obj.delete(recursive)

    @classmethod
    def delete_selection(cls):
        objects = cls.get_selected_objects()
        from som_gui.windows.popups import msg_del_items
        delete_request, recursive_deletion = msg_del_items([o.name for o in objects], item_type=1)
        if not delete_request:
            return
        for o in objects:
            cls.delete_object(o, recursive_deletion)

    @classmethod
    def expand_selection(cls):
        tree = cls.get_object_tree()
        for index in tree.selectedIndexes():
            tree.expandRecursively(index)

    @classmethod
    def collapse_selection(cls):
        tree = cls.get_object_tree()
        for item in tree.selectedItems():
            tree.collapseItem(item)

    @classmethod
    def group_selection(cls):
        pass

    @classmethod
    def clear_context_menu_list(cls):
        prop = cls.get_object_properties()
        prop.context_menu_list = list()

    @classmethod
    def add_context_menu_entry(cls, name: str, function: Callable, single: bool, multi: bool) -> ContextMenuDict:
        d: ContextMenuDict = dict()
        d["display_name"] = name
        d["function"] = function
        d["on_multi_select"] = multi
        d["on_single_select"] = single
        prop = cls.get_object_properties()
        prop.context_menu_list.append(d)

    @classmethod
    def handle_attribute_issue(cls, result: int):
        if result == som_gui.module.objects.OK:
            return True
        # TODO: Popups erstellen
        if result == som_gui.module.objects.IDENT_ISSUE:
            logging.error(f"Identifier existiert bereits")
            return False
        if result == som_gui.module.objects.ABBREV_ISSUE:
            logging.error(f"Abkürzung existiert bereits")
            return False

    @classmethod
    def copy_object(cls, obj: SOMcreator.Object, data_dict: ObjectDataDict) -> tuple[int, SOMcreator.Object | None]:
        is_group = data_dict.get("is_group")
        if is_group:
            new_object = cp.copy(obj)
            new_object.ident_attrib = uuid.uuid4()
            return som_gui.module.objects.OK, new_object
        ident_value = data_dict["ident_value"]
        abbreviation = data_dict.get("abbreviation")
        pset = data_dict.get("ident_pset_name")
        attribute = data_dict.get("ident_attribute_name")

        if not cls.identifier_is_allowed(ident_value):
            return som_gui.module.objects.IDENT_ISSUE, None

        if not cls.abbreviation_is_allowed(abbreviation):
            logging.error(f"Abkürzung {abbreviation} existiert bereits!")
            return som_gui.module.objects.ABBREV_ISSUE, None
        new_object = cp.copy(obj)
        if pset and attribute:
            new_object.ident_attrib = cls.find_attribute(new_object, pset, attribute)
        new_object.ident_attrib.value = [ident_value]
        new_object.abbreviation = abbreviation
        return som_gui.module.objects.OK, new_object

    @classmethod
    def change_object_info(cls, obj: SOMcreator.Object, data_dict: ObjectDataDict) -> int:
        name = data_dict.get("name")
        ifc_mappings = data_dict.get("ifc_mappings")
        identifer = data_dict.get("ident_value")
        abbreviation = data_dict.get("abbreviation")
        pset_name = data_dict.get("ident_pset_name")
        attribute_name = data_dict.get("ident_attribute_name")
        is_group = data_dict.get("is_group")

        is_group = obj.is_concept if is_group is None else is_group
        if not is_group:
            if identifer is not None and not cls.identifier_is_allowed(identifer, obj.ident_value):
                return som_gui.module.objects.IDENT_ISSUE
            if abbreviation is not None and not cls.abbreviation_is_allowed(abbreviation, obj.abbreviation):
                return som_gui.module.objects.ABBREV_ISSUE
        obj.name = name if name else obj.name
        obj.ifc_mapping = ifc_mappings if ifc_mappings is not None else obj.ifc_mapping

        if is_group and not obj.is_concept:
            obj.ident_attrib = str(uuid.uuid4())
            return som_gui.module.objects.OK

        if pset_name and attribute_name:
            ident_attribute = cls.find_attribute(obj, pset_name, attribute_name)
            obj.ident_attrib = ident_attribute if ident_attribute is not None else obj.ident_attrib

        if identifer is not None:
            cls.set_ident_value(obj, identifer)
        obj.abbreviation = abbreviation if abbreviation is not None else obj.abbreviation
        return som_gui.module.objects.OK

    @classmethod
    def set_ident_value(cls, obj: SOMcreator.Object, value: str):
        if obj.is_concept:
            return
        obj.ident_attrib.value = [value]

    @classmethod
    def find_attribute(cls, obj: SOMcreator.Object, pset_name, attribute_name):
        pset = obj.get_property_set_by_name(pset_name)
        if pset is None:
            return None
        return pset.get_attribute_by_name(attribute_name)

    @classmethod
    def get_object_properties(cls) -> ObjectProperties:
        return som_gui.ObjectProperties

    @classmethod
    def get_active_object(cls) -> SOMcreator.Object:
        return som_gui.ObjectProperties.active_object

    @classmethod
    def get_existing_ident_values(cls) -> set[str]:
        proj = tool.Project.get()
        ident_values = set()
        for obj in proj.get_all_objects():
            if obj.ident_value:
                ident_values.add(obj.ident_value)
        return ident_values

    @classmethod
    def get_existing_abbriviations(cls) -> set[str]:
        proj = tool.Project.get()
        abbreviations = set()
        for obj in proj.get_all_objects():
            if obj.abbreviation:
                abbreviations.add(obj.abbreviation)
        return abbreviations

    @classmethod
    def identifier_is_allowed(cls, identifier, ignore=None):
        identifiers = cls.get_existing_ident_values()
        if ignore is not None:
            identifiers = list(filter(lambda i: i != ignore, identifiers))
        if identifier in identifiers:
            return False
        else:
            return True

    @classmethod
    def abbreviation_is_allowed(cls, abbreviation, ignore=None):
        abbreviations = cls.get_existing_abbriviations()
        if ignore is not None:
            abbreviations = list(filter(lambda a: a != ignore, abbreviations))
        if abbreviation in abbreviations:
            return False
        else:
            return True

    @classmethod
    def oi_create_widget(cls):
        prop: ObjectProperties = som_gui.ObjectProperties
        prop.object_info_widget_properties = som_gui.module.objects.prop.ObjectInfoWidgetProperties()
        prop.object_info_widget = som_gui.module.objects.ui.ObjectInfoWidget()
        return prop.object_info_widget

    @classmethod
    def oi_get_focus_object(cls):
        return cls.get_object_info_properties().focus_object

    @classmethod
    def oi_get_mode(cls):
        """
        1 = Info
        2 = Copy
        """
        return cls.get_object_info_properties().mode

    @classmethod
    def oi_get_values(cls) -> ObjectDataDict:
        widget = cls.get_object_properties().object_info_widget.widget
        d: ObjectDataDict = dict()

        d["is_group"] = widget.button_gruppe.isChecked()
        d["ident_value"] = widget.line_edit_attribute_value.text()
        d["abbreviation"] = widget.line_edit_abbreviation.text()
        d["ident_pset_name"] = widget.combo_box_pset.currentText()
        d["ident_attribute_name"] = widget.combo_box_attribute.currentText()
        d["name"] = widget.line_edit_name.text()
        d["ifc_mappings"] = cls.get_ifc_mappings()
        return d

    @classmethod
    def get_ifc_mappings(cls):
        widget = cls.get_object_properties().object_info_widget.widget
        values = list()
        for index in range(widget.vertical_layout_ifc.count()):
            item: QLineEdit = widget.vertical_layout_ifc.itemAt(index).widget()
            values.append(item.text())
        return values

    @classmethod
    def oi_set_values(cls, data_dict: ObjectDataDict):
        prop = cls.get_object_info_properties()
        if data_dict.get("name"):
            prop.name = data_dict.get("name")
        if data_dict.get("abbreviation"):
            prop.abbreviation = data_dict.get("abbreviation")
        if data_dict.get("is_group") is not None:
            prop.is_group = data_dict.get("is_group")
        if data_dict.get("ident_pset_name"):
            prop.pset_name = data_dict.get("ident_pset_name")
        if data_dict.get("ident_attribute_name"):
            prop.attribute_name = data_dict.get("ident_attribute_name")
        if data_dict.get("ident_value"):
            prop.ident_value = data_dict.get("ident_value")
        if data_dict.get("ifc_mappings"):
            prop.ifc_mappings = data_dict.get("ifc_mappings")

    @classmethod
    def oi_set_group_value(cls, value):
        prop = cls.get_object_info_properties()
        prop.is_group = value

    @classmethod
    def oi_set_ident_value_color(cls, color: str):
        widget = cls.get_object_properties().object_info_widget.widget
        widget.line_edit_attribute_value.setStyleSheet(f"color:{color}")

    @classmethod
    def oi_set_abbrev_value_color(cls, color: str):
        widget = cls.get_object_properties().object_info_widget.widget
        widget.line_edit_abbreviation.setStyleSheet(f"color:{color}")

    @classmethod
    def oi_set_abbreviation(cls, value):
        prop = cls.get_object_info_properties()
        prop.abbreviation = value

    @classmethod
    def oi_change_visibility_identifiers(cls, hide: bool):
        prop = cls.get_object_properties()
        layout = prop.object_info_widget.widget.layout_ident_attribute
        if hide:
            for index in range(layout.count()):
                layout.itemAt(index).widget().hide()
        else:
            for index in range(layout.count()):
                layout.itemAt(index).widget().show()

    @classmethod
    def oi_update_attribute_combobox(cls):
        prop: ObjectProperties = som_gui.ObjectProperties
        pset_name = prop.object_info_widget.widget.combo_box_pset.currentText()
        active_object = prop.object_info_widget_properties.focus_object

        property_set: SOMcreator.PropertySet = {p.name: p for p in active_object.property_sets}.get(pset_name)
        attribute_names = sorted([a.name for a in property_set.attributes])
        prop.object_info_widget.widget.combo_box_attribute.clear()
        prop.object_info_widget.widget.combo_box_attribute.addItems(attribute_names)

    @classmethod
    def create_ifc_completer(cls):
        return QCompleter(IFC_4_1)

    @classmethod
    def get_object_info_properties(cls):
        prop: ObjectProperties = som_gui.ObjectProperties
        return prop.object_info_widget_properties

    @classmethod
    def oi_fill_properties(cls, mode: int):
        prop: ObjectProperties = som_gui.ObjectProperties
        info_properties = prop.object_info_widget_properties
        info_properties.focus_object = prop.active_object
        info_properties.ident_value = info_properties.focus_object.ident_value
        info_properties.mode = mode

        info_properties.abbreviation = info_properties.focus_object.abbreviation
        info_properties.is_group = info_properties.focus_object.is_concept
        info_properties.name = info_properties.focus_object.name
        info_properties.ifc_mappings = list(info_properties.focus_object.ifc_mapping)
        if not info_properties.focus_object.is_concept:
            info_properties.pset_name = info_properties.focus_object.ident_attrib.property_set.name
            info_properties.attribute_name = info_properties.focus_object.ident_attrib.name

    @classmethod
    def oi_update_dialog(cls):
        prop: ObjectProperties = som_gui.ObjectProperties
        dialog = prop.object_info_widget
        info_prop = prop.object_info_widget_properties
        dialog.widget.line_edit_name.setText(info_prop.name)
        dialog.widget.line_edit_abbreviation.setText(info_prop.abbreviation)
        dialog.widget.button_gruppe.setChecked(info_prop.is_group)
        active_object = prop.active_object
        dialog.widget.combo_box_pset.clear()
        [dialog.widget.combo_box_pset.addItem(p.name) for p in active_object.property_sets]
        if not info_prop.is_group:
            dialog.widget.combo_box_pset.setCurrentText(info_prop.pset_name)
            dialog.widget.combo_box_attribute.setCurrentText(info_prop.attribute_name)
            dialog.widget.line_edit_attribute_value.setText(info_prop.ident_value)
        for mapping in info_prop.ifc_mappings:
            cls.add_ifc_mapping(mapping)

    @classmethod
    def add_ifc_mapping(cls, mapping):
        line_edit = QLineEdit()
        line_edit.setCompleter(cls.create_ifc_completer())
        line_edit.setText(mapping)
        prop: ObjectProperties = som_gui.ObjectProperties
        info_prop = prop.object_info_widget_properties
        info_prop.ifc_lines.append(line_edit)
        prop.object_info_widget.widget.vertical_layout_ifc.addWidget(line_edit)

    @classmethod
    def set_mouse_press(cls, is_pressed: bool):
        logging.debug(f"Set Mouse Press")
        prop: ObjectProperties = som_gui.ObjectProperties
        prop.mouse_is_pressed = is_pressed

    @classmethod
    def is_mouse_pressed(cls) -> bool:
        logging.debug(f"Mouse State Requested")

        prop: ObjectProperties = som_gui.ObjectProperties
        return prop.mouse_is_pressed

    @classmethod
    def drop_indication_pos_is_on_item(cls):
        logging.debug(f"Drop Indicator Requested")

        widget = cls.get_object_tree()
        if widget.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:
            return True
        else:
            return False

    @classmethod
    def get_item_from_pos(cls, pos: QPoint):
        logging.debug(f"Item from Pos Requested")

        widget = cls.get_object_tree()
        return widget.itemFromIndex(widget.indexAt(pos))

    @classmethod
    def get_selected_items(cls) -> list[QTreeWidgetItem]:
        logging.debug(f"selected Items Requested")
        widget = cls.get_object_tree()
        return widget.selectedItems()

    @classmethod
    def get_object_from_item(cls, item: QTreeWidgetItem) -> SOMcreator.Object:
        logging.debug(f"Object from Item Requested")
        return item.object

    @classmethod
    def fill_object_entry(cls, obj: SOMcreator.Object):
        logging.debug(f"Fill Object Entry")

        window: MainWindow = som_gui.MainUi.window
        window.ui.line_edit_object_name.setText(obj.name)
        window.ui.line_edit_abbreviation.setText(obj.abbreviation)

        ident_widgets = [window.ui.lineEdit_ident_pSet,
                         window.ui.lineEdit_ident_attribute,
                         window.ui.lineEdit_ident_value, ]
        if obj.is_concept:

            ident_values = ["", "", ""]
        else:
            ident_values = [obj.ident_attrib.property_set.name,
                            obj.ident_attrib.name,
                            obj.ident_value]

        for widget, value in zip(ident_widgets, ident_values):
            widget.setText(value)
            widget.setDisabled(obj.is_concept)

    @classmethod
    def set_active_object(cls, obj: SOMcreator.Object):
        logging.debug(f"Set Active Object")

        prop: ObjectProperties = som_gui.ObjectProperties
        prop.active_object = obj
        cls.fill_object_entry(obj)

    @classmethod
    def update_check_state(cls, item: QTreeWidgetItem):
        logging.debug(f"Update CheckState")

        obj: SOMcreator.Object = cls.get_object_from_item(item)
        obj.optional = True if item.checkState(3) == Qt.CheckState.Checked else False

    @classmethod
    def get_object_tree(cls) -> QTreeWidget:
        logging.debug(f"ObjectTree Requested")

        return som_gui.MainUi.ui.tree_object

    @classmethod
    def create_item(cls, obj: SOMcreator.Object):
        logging.debug(f"CreateItem")

        item = QTreeWidgetItem()
        item.object = obj  # item.setData(0,obj) leads to recursion bug so allocating directly
        item.setText(0, obj.name)
        return item

    @classmethod
    def update_item(cls, item: QTreeWidgetItem, obj: SOMcreator.Object):
        logging.debug(f"Update Item {obj}")

        item.setText(0, obj.name)
        item.setText(1, obj.ident_value)
        item.setText(2, obj.abbreviation)
        cs = Qt.CheckState.Checked if obj.optional else Qt.CheckState.Unchecked
        item.setCheckState(3, cs)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable)

    @classmethod
    def fill_object_tree(cls, objects: set[SOMcreator.Object], parent_item: QTreeWidgetItem) -> None:
        logging.debug(f"Fill Object Tree {parent_item}")
        old_objects_dict = {cls.get_object_from_item(parent_item.child(i)): i for i in range(parent_item.childCount())}
        old_objects = set(old_objects_dict.keys())
        new_objects = objects.difference(old_objects)
        delete_objects = old_objects.difference(objects)

        for obj in reversed(sorted(delete_objects, key=lambda o: old_objects_dict[o])):
            row_index = old_objects_dict[obj]
            parent_item.removeChild(parent_item.child(row_index))

        for new_object in sorted(new_objects, key=lambda o: o.name):
            item = cls.create_item(new_object)
            parent_item.addChild(item)

        for index in range(parent_item.childCount()):
            item = parent_item.child(index)
            obj: SOMcreator.Object = cls.get_object_from_item(item)
            cls.update_item(item, obj)
            cls.fill_object_tree(obj.children, item)
