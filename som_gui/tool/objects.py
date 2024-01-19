from __future__ import annotations

import logging

import som_gui.core.tool
import som_gui.tool as tool
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget, QAbstractItemView, QLineEdit, QCompleter
from PySide6.QtCore import Qt, QPoint
import som_gui
from typing import TYPE_CHECKING
from SOMcreator.Template import IFC_4_1

if TYPE_CHECKING:
    from som_gui.module.objects.prop import ObjectProperties
    from som_gui.main_window import MainWindow


class Objects(som_gui.core.tool.Object):
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
    def oi_get_values(cls):
        widget = cls.get_object_properties().object_info_widget.widget

        group = widget.button_gruppe.isChecked()
        ident_value = widget.line_edit_attribute_value.text()
        abbreviation = widget.line_edit_abbreviation.text()
        pset = widget.combo_box_pset.currentText()
        attribute = widget.combo_box_attribute.currentText()
        name = widget.line_edit_name.text()
        ifc_mappings = cls.get_ifc_mappings()
        return name, abbreviation, group, pset, attribute, ident_value, ifc_mappings

    @classmethod
    def get_ifc_mappings(cls):
        widget = cls.get_object_properties().object_info_widget.widget
        values = list()
        for index in range(widget.vertical_layout_ifc.count()):
            item: QLineEdit = widget.vertical_layout_ifc.itemAt(index).widget()
            values.append(item.text())
        return values

    @classmethod
    def oi_set_values(cls, name, abbreviation, group, pset, attribute, ident_value, ifc_mappings):
        prop = cls.get_object_info_properties()
        prop.name = name
        prop.abbreviation = abbreviation
        prop.is_group = group
        prop.pset_name = pset
        prop.attribute_name = attribute
        prop.ident_value = ident_value
        prop.ifc_mappings = ifc_mappings

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
        active_object = prop.active_object

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
    def oi_fill_properties(cls):
        prop: ObjectProperties = som_gui.ObjectProperties
        info_properties = prop.object_info_widget_properties
        active_object = prop.active_object
        info_properties.ident_value = active_object.ident_value
        info_properties.abbreviation = active_object.abbreviation
        info_properties.is_group = active_object.is_concept
        info_properties.name = active_object.name
        info_properties.ifc_mappings = list(active_object.ifc_mapping)
        if active_object.ident_attrib:
            info_properties.pset_name = active_object.ident_attrib.property_set.name
            info_properties.attribute_name = active_object.ident_attrib.name

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
