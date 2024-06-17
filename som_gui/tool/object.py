from __future__ import annotations

import logging
import copy as cp
import uuid

import som_gui.core.tool
import som_gui.tool as tool
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem, QAbstractItemView, QLineEdit, QCompleter, QMenu
from PySide6.QtCore import Qt, QPoint
import som_gui
from typing import TYPE_CHECKING, TypedDict, Callable
from SOMcreator.Template import IFC_4_1
from som_gui.module.object.prop import PluginProperty
if TYPE_CHECKING:
    from som_gui.module.object.prop import ObjectProperties, ContextMenuDict
    from som_gui.module.main_window.ui import MainWindow
    from som_gui.module.object.ui import ObjectTreeWidget


class ObjectDataDict(TypedDict):
    name: str
    is_group: bool
    abbreviation: str
    ident_pset_name: str
    ident_attribute_name: str
    ident_value: str
    ifc_mappings: list[str]


class Object(som_gui.core.tool.Object):
    @classmethod
    def oi_add_plugin_entry(cls, key: str, layout_name: str, widget, index, init_value_getter, widget_value_getter,
                            widget_value_setter, test_function, value_setter):
        prop = PluginProperty(key, layout_name, widget, index, init_value_getter, widget_value_getter,
                              widget_value_setter, test_function, value_setter)

        cls.get_properties().object_info_plugin_list.append(prop)

    @classmethod
    def get_object_infos(cls) -> ObjectDataDict:
        d = dict()
        for key, func in cls.get_properties().object_add_infos_functions:
            d[key] = func()
        return d

    @classmethod
    def add_column_to_tree(cls, name, index, getter_func):
        tree = cls.get_object_tree()
        header = tree.headerItem()
        header_texts = [header.text(i) for i in range(header.columnCount())]
        header_texts.insert(index, tree.tr(name))
        tree.setColumnCount(tree.columnCount() + 1)
        [header.setText(i, t) for i, t in enumerate(header_texts)]
        cls.get_properties().column_List.insert(index, (name, getter_func))

    @classmethod
    def create_completer(cls, texts, lineedit: QLineEdit):
        completer = QCompleter(texts)
        lineedit.setCompleter(completer)

    @classmethod
    def get_all_objects(cls):
        return tool.Project.get().get_all_objects()

    @classmethod
    def get_item_from_object(cls, obj: SOMcreator.Object) -> QTreeWidgetItem:
        def iter_tree(item: QTreeWidgetItem):
            for child_index in range(item.childCount()):
                child = item.child(child_index)
                if cls.get_object_from_item(child) == obj:
                    return child
                result = iter_tree(child)
                if result is not None:
                    return result
            return None

        tree = cls.get_object_tree()
        return iter_tree(tree.invisibleRootItem())

    @classmethod
    def select_object(cls, obj: SOMcreator.Object) -> None:
        item = cls.get_item_from_object(obj)
        if item is None:
            return
        tree = cls.get_object_tree()
        for selected_item in tree.selectedItems():
            selected_item.setSelected(False)
        item.setSelected(True)
        cls.expand_to_item(item)

    @classmethod
    def expand_to_item(cls, item: QTreeWidgetItem):
        item.setExpanded(True)
        if item.parent() is not None:
            cls.expand_to_item(item.parent())

    @classmethod
    def autofit_tree(cls):
        if cls.get_properties().first_paint:
            cls.resize_tree()
            cls.get_properties().first_paint = False

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
    def create_context_menu(cls):
        menu = QMenu()
        prop = cls.get_properties()
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
        # def delete_nodes(o: SOMcreator.Object):
        #     for aggregation in list(o.aggregations):
        #         node = som_gui.MainUi.window.graph_window.aggregation_dict().get(aggregation)
        #         node.delete(recursive)
        #     if recursive:
        #         for child in o.get_all_children():
        #             delete_nodes(child)
        #
        # delete_nodes(obj)
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
        prop = cls.get_properties()
        prop.context_menu_list = list()

    @classmethod
    def add_context_menu_entry(cls, name: str, function: Callable, single: bool, multi: bool) -> ContextMenuDict:
        d: ContextMenuDict = dict()
        d["display_name"] = name
        d["function"] = function
        d["on_multi_select"] = multi
        d["on_single_select"] = single
        prop = cls.get_properties()
        prop.context_menu_list.append(d)
        return d

    @classmethod
    def handle_attribute_issue(cls, result: int):
        if result == som_gui.module.object.OK:
            return True
        app = tool.MainWindow.get_app()
        if result == som_gui.module.object.IDENT_ISSUE:
            text = "Identifier existiert bereits oder is nicht erlaubt!"
        elif result == som_gui.module.object.IDENT_ATTRIBUTE_ISSUE:
            text = u"Attribute Name is nicht erlaubt!"
        elif result == som_gui.module.object.IDENT_PSET_ISSUE:
            text = u"PropertySet Name is nicht erlaubt!"
        else:
            return False
        text = app.translate("MainWindow", text)
        logging.error(text)
        tool.Popups.create_warning_popup(text)
        return False

    @classmethod
    def copy_object(cls, obj: SOMcreator.Object, data_dict: ObjectDataDict) -> tuple[int, SOMcreator.Object | None]:
        is_group = data_dict.get("is_group")
        if is_group:
            new_object = cp.copy(obj)
            new_object.ident_attrib = uuid.uuid4()
            return som_gui.module.object.OK, new_object
        ident_value = data_dict["ident_value"]
        pset = data_dict.get("ident_pset_name")
        attribute = data_dict.get("ident_attribute_name")

        if not cls.is_identifier_allowed(ident_value):
            return som_gui.module.object.IDENT_ISSUE, None

        for plugin in cls.get_properties().object_info_plugin_list:  # Call Test Func
            result = plugin.value_test(data_dict[plugin.key], obj)
            if result != som_gui.module.object.OK:
                return result, None
        new_object = cp.copy(obj)
        if pset and attribute:
            new_object.ident_attrib = cls.find_attribute(new_object, pset, attribute)
        new_object.ident_attrib.value = [ident_value]
        for plugin in cls.get_properties().object_info_plugin_list:  # call Setter Func
            plugin.value_setter(new_object, data_dict[plugin.key])

        return som_gui.module.object.OK, new_object

    @classmethod
    def check_object_creation_imput(cls, data_dict) -> int:
        is_group = data_dict["is_group"]
        abbreviation = data_dict.get("abbreviation")
        ident_pset_name = data_dict.get("ident_pset_name")
        ident_attribute_name = data_dict.get("ident_attribute_name")
        ident_value = data_dict.get("ident_value")
        if is_group:
            return som_gui.module.object.OK
        else:
            if not cls.is_identifier_allowed(ident_value):
                return som_gui.module.object.IDENT_ISSUE
            elif not cls.is_abbreviation_allowed(abbreviation):
                return som_gui.module.object.ABBREV_ISSUE
            elif not ident_pset_name:
                return som_gui.module.object.IDENT_PSET_ISSUE
            elif not ident_attribute_name:
                return som_gui.module.object.IDENT_ATTRIBUTE_ISSUE
            else:
                return som_gui.module.object.OK

    @classmethod
    def create_object(cls, data_dict: ObjectDataDict, property_set: SOMcreator.PropertySet,
                      attribute: SOMcreator.Attribute):
        name = data_dict["name"]
        is_group = data_dict["is_group"]
        abbreviation = data_dict.get("abbreviation")
        ifc_mappings = data_dict.get("ifc_mappings")
        if is_group:
            ident = str(uuid.uuid4())
            obj = SOMcreator.Object(name, ident, uuid=ident, project=tool.Project.get())
        else:
            obj = SOMcreator.Object(name, attribute, project=tool.Project.get())
            obj.add_property_set(property_set)
        if ifc_mappings:
            obj.ifc_mapping = ifc_mappings
        if abbreviation:
            obj.abbreviation = abbreviation
        return obj

    @classmethod
    def change_object_info(cls, obj: SOMcreator.Object, data_dict: ObjectDataDict) -> int:
        name = data_dict.get("name")
        ifc_mappings = data_dict.get("ifc_mappings")
        identifer = data_dict.get("ident_value")
        pset_name = data_dict.get("ident_pset_name")
        attribute_name = data_dict.get("ident_attribute_name")
        is_group = data_dict.get("is_group")

        is_group = obj.is_concept if is_group is None else is_group
        if not is_group:
            if identifer is not None and not cls.is_identifier_allowed(identifer, obj.ident_value):
                return som_gui.module.object.IDENT_ISSUE

        for plugin in cls.get_properties().object_info_plugin_list:  # Call Test Func
            result = plugin.value_test(data_dict[plugin.key], obj)
            if result != som_gui.module.object.OK:
                return result

        obj.name = name if name else obj.name
        obj.ifc_mapping = ifc_mappings if ifc_mappings is not None else obj.ifc_mapping

        if is_group and not obj.is_concept:
            obj.ident_attrib = str(uuid.uuid4())
            return som_gui.module.object.OK

        if pset_name and attribute_name:
            ident_attribute = cls.find_attribute(obj, pset_name, attribute_name)
            obj.ident_attrib = ident_attribute if ident_attribute is not None else obj.ident_attrib

        if identifer is not None:
            cls.set_ident_value(obj, identifer)
        for plugin in cls.get_properties().object_info_plugin_list:  # call Setter Func
            plugin.value_setter(obj, data_dict[plugin.key])

        return som_gui.module.object.OK

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
    def get_properties(cls) -> ObjectProperties:
        return som_gui.ObjectProperties

    @classmethod
    def get_active_object(cls) -> SOMcreator.Object | None:
        if not hasattr(cls.get_properties(), "active_object"):
            return None
        return cls.get_properties().active_object

    @classmethod
    def get_existing_ident_values(cls) -> set[str]:
        proj = tool.Project.get()
        ident_values = set()
        for obj in proj.get_all_objects():
            if obj.ident_value:
                ident_values.add(obj.ident_value)
        return ident_values



    @classmethod
    def is_identifier_allowed(cls, identifier, ignore=None):
        identifiers = cls.get_existing_ident_values()
        if ignore is not None:
            identifiers = list(filter(lambda i: i != ignore, identifiers))
        if identifier in identifiers or not identifier:
            return False
        else:
            return True



    @classmethod
    def oi_create_dialog(cls):
        prop = cls.get_properties()
        prop.object_info_widget_properties = som_gui.module.object.prop.ObjectInfoWidgetProperties()
        dialog = som_gui.module.object.ui.ObjectInfoWidget()
        for plugin in prop.object_info_plugin_list:
            getattr(dialog.widget, plugin.layout_name).insertWidget(plugin.index, plugin.widget)
            setattr(prop.object_info_widget_properties, plugin.key, plugin.init_value_getter)
        prop.object_info_widget = dialog
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
        widget = cls.get_properties().object_info_widget.widget
        d: ObjectDataDict = dict()

        d["is_group"] = widget.button_gruppe.isChecked()
        d["ident_value"] = widget.line_edit_attribute_value.text()
        d["ident_pset_name"] = widget.combo_box_pset.currentText()
        d["ident_attribute_name"] = widget.combo_box_attribute.currentText()
        d["name"] = widget.line_edit_name.text()
        d["ifc_mappings"] = cls.get_ifc_mappings()
        for plugin in cls.get_properties().object_info_plugin_list:
            d[plugin.key] = plugin.widget_value_getter()
        return d

    @classmethod
    def get_ifc_mappings(cls):
        widget = cls.get_properties().object_info_widget.widget
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
    def oi_set_ident_value_color(cls, color: str):
        widget = cls.get_properties().object_info_widget.widget
        widget.line_edit_attribute_value.setStyleSheet(f"color:{color}")



    @classmethod
    def oi_set_abbreviation(cls, value):
        prop = cls.get_object_info_properties()
        prop.abbreviation = value

    @classmethod
    def oi_change_visibility_identifiers(cls, hide: bool):
        prop = cls.get_properties()
        layout = prop.object_info_widget.widget.layout_ident_attribute
        if hide:
            for index in range(layout.count()):
                layout.itemAt(index).widget().hide()
        else:
            for index in range(layout.count()):
                layout.itemAt(index).widget().show()

    @classmethod
    def oi_update_attribute_combobox(cls):
        prop: ObjectProperties = cls.get_properties()
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
        return cls.get_properties().object_info_widget_properties

    @classmethod
    def oi_fill_properties(cls, mode: int):
        prop: ObjectProperties = cls.get_properties()
        info_properties = prop.object_info_widget_properties
        obj = prop.active_object
        info_properties.focus_object = prop.active_object
        info_properties.ident_value = obj.ident_value
        info_properties.mode = mode

        for plugin in prop.object_info_plugin_list:
            info_properties.plugin_infos[plugin.key] = plugin.init_value_getter(obj)
        info_properties.is_group = obj.is_concept
        info_properties.name = obj.name
        info_properties.ifc_mappings = list(obj.ifc_mapping)
        if not obj.is_concept:
            info_properties.pset_name = obj.ident_attrib.property_set.name
            info_properties.attribute_name = obj.ident_attrib.name

    @classmethod
    def oi_update_dialog(cls):
        prop: ObjectProperties = cls.get_properties()
        dialog = prop.object_info_widget
        info_prop = prop.object_info_widget_properties
        dialog.widget.line_edit_name.setText(info_prop.name)
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

        for plugin in prop.object_info_plugin_list:
            plugin.widget_value_setter(info_prop.plugin_infos.get(plugin.key))


    @classmethod
    def add_ifc_mapping(cls, mapping):
        line_edit = QLineEdit()
        line_edit.setCompleter(cls.create_ifc_completer())
        line_edit.setText(mapping)
        prop: ObjectProperties = cls.get_properties()
        info_prop = prop.object_info_widget_properties
        info_prop.ifc_lines.append(line_edit)
        prop.object_info_widget.widget.vertical_layout_ifc.addWidget(line_edit)

    @classmethod
    def drop_indication_pos_is_on_item(cls):

        widget = cls.get_object_tree()
        if widget.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:
            return True
        else:
            return False

    @classmethod
    def get_item_from_pos(cls, pos: QPoint):

        widget = cls.get_object_tree()
        return widget.itemFromIndex(widget.indexAt(pos))

    @classmethod
    def get_selected_items(cls) -> list[QTreeWidgetItem]:
        widget = cls.get_object_tree()
        return widget.selectedItems()

    @classmethod
    def get_object_from_item(cls, item: QTreeWidgetItem) -> SOMcreator.Object:
        return item.object

    @classmethod
    def fill_object_property_set_line_edit(cls, line_edit: QLineEdit, obj: SOMcreator.Object, ):
        if obj.is_concept:
            line_edit.setText("")
            line_edit.setEnabled(False)
            return
        else:
            line_edit.setEnabled(True)

        if not obj.ident_attrib:
            line_edit.setText("")
            return
        if not obj.ident_attrib.property_set:
            line_edit.setText("")
            return
        line_edit.setText(obj.ident_attrib.property_set.name)

    @classmethod
    def fill_object_attribute_line_edit(cls, line_edit: QLineEdit, obj: SOMcreator.Object):
        if obj.is_concept:
            line_edit.setText("")
            line_edit.setEnabled(False)
            return
        else:
            line_edit.setEnabled(True)

        if not obj.ident_attrib:
            line_edit.setText("")
            return
        line_edit.setText(obj.ident_attrib.name)

    @classmethod
    def add_object_activate_function(cls, func: Callable):
        cls.get_properties().object_activate_functions.append(func)

    @classmethod
    def add_objects_infos_add_function(cls, key: str, getter_function: Callable):
        cls.get_properties().object_add_infos_functions.append((key, getter_function))

    @classmethod
    def fill_object_entry(cls, obj: SOMcreator.Object):
        for func in cls.get_properties().object_activate_functions:
            func(obj)

    @classmethod
    def set_active_object(cls, obj: SOMcreator.Object):
        prop: ObjectProperties = cls.get_properties()
        prop.active_object = obj
        cls.fill_object_entry(obj)

    @classmethod
    def update_check_state(cls, item: QTreeWidgetItem):
        obj: SOMcreator.Object = cls.get_object_from_item(item)
        obj.optional = True if item.checkState(3) == Qt.CheckState.Checked else False

    @classmethod
    def get_object_tree(cls) -> ObjectTreeWidget:
        return tool.MainWindow.get_object_tree_widget()

    @classmethod
    def create_item(cls, obj: SOMcreator.Object):
        item = QTreeWidgetItem()
        item.object = obj  # item.setData(0,obj) leads to recursion bug so allocating directly
        item.setText(0, obj.name)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable)
        item.setCheckState(3, Qt.CheckState.Unchecked)
        return item

    @classmethod
    def update_item(cls, item: QTreeWidgetItem, obj: SOMcreator.Object):
        values = [f(obj) for n, f in cls.get_properties().column_List]

        for column, value in enumerate(values):
            if isinstance(value, bool):
                cs = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
                if item.checkState(column) != cs:
                    item.setCheckState(column, cs)

            elif item.text(column) != value:
                item.setText(column, value)

    @classmethod
    def fill_object_tree(cls, objects: set[SOMcreator.Object], parent_item: QTreeWidgetItem) -> None:
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
            cls.fill_object_tree(set(obj.children), item)

    @classmethod
    def clear_object_input(cls, ui):
        obj_line_edit_list = [
            ui.line_edit_object_name,
            ui.lineEdit_ident_value,
            ui.lineEdit_ident_attribute,
            ui.lineEdit_ident_pSet,
            ui.line_edit_abbreviation,
        ]
        for el in obj_line_edit_list:
            el.clear()
