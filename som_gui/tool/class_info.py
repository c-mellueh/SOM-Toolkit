from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from som_gui.module.class_info.prop import PluginProperty, ClasstDataDict
from PySide6.QtWidgets import QWidget, QLineEdit, QCompleter

if TYPE_CHECKING:
    from som_gui.module.class_info.prop import ClassInfoProperties
import som_gui.core.tool
from som_gui import tool
import SOMcreator
from som_gui.module.class_info.ui import ClassInfoWidget
from SOMcreator.templates import IFC_4_1
from som_gui.module.class_info import trigger


class ClassInfo(som_gui.core.tool):
    @classmethod
    def get_properties(cls) -> ClassInfoProperties:
        return som_gui.ClassInfoProperties

    @classmethod
    def add_plugin_entry(
        cls,
        key: str,
        layout_name: str,
        widget: QWidget,
        index: int,
        init_value_getter: Callable,
        widget_value_getter: Callable,
        widget_value_setter: Callable,
        test_function: Callable,
        value_setter: Callable,
    ):
        """
        Create entry of QWidget that will be added to Class Info Dialog
        layout_name: name of layout in which QWidget will be placed
        widget: Widget that will be placed
        index: index of position in layout where widget will be placed
        init_value_getter: function that gets the initial value that will be displayed in the widget
        widget_value_setter: function that will set a given value in the widget
        test_function: function that get's called to check if value written in widget is valid for object
        value_setter: function thats sets value of class after ClassInfoWidget is accepted
        """
        prop = PluginProperty(
            key,
            layout_name,
            widget,
            index,
            init_value_getter,
            widget_value_getter,
            widget_value_setter,
            test_function,
            value_setter,
        )

        cls.get_properties().class_info_plugin_list.append(prop)

    @classmethod
    def get_class_infos(cls) -> ClasstDataDict:
        d = dict()
        for key, func in cls.get_properties().class_add_infos_functions:
            d[key] = func()
        return d

    @classmethod
    def oi_update_attribute_combobox(
        cls, predefined_psets: list[SOMcreator.SOMPropertySet]
    ):
        prop = cls.get_properties()
        widget = prop.widget.widget
        pset_name = widget.combo_box_pset.currentText()
        mode = cls.oi_get_mode()

        if mode == 0:
            property_set = {p.name: p for p in predefined_psets}.get(pset_name)
            if property_set:
                property_names = [
                    pr.name for pr in property_set.get_properties(filter=False)
                ]
                tool.Util.create_completer(property_names, widget.combo_box_attribute)
        else:
            active_object = cls.oi_get_focus_class()
            property_set: SOMcreator.SOMPropertySet = {
                p.name: p for p in active_object.get_property_sets(filter=False)
            }.get(pset_name)
            attribute_names = sorted(
                [a.name for a in property_set.get_properties(filter=False)]
            )
            widget.combo_box_attribute.clear()
            widget.combo_box_attribute.addItems(attribute_names)

    @classmethod
    def oi_create_dialog(cls, title) -> ClassInfoWidget:
        prop = cls.get_properties()
        prop.object_info_widget_properties = (
            som_gui.module.class_.prop.ObjectInfoWidgetProperties()
        )
        dialog = som_gui.module.class_.ui.ClassInfoWidget()
        for plugin in prop.class_info_plugin_list:
            getattr(dialog.widget, plugin.layout_name).insertWidget(
                plugin.index, plugin.widget
            )
            setattr(
                prop.object_info_widget_properties, plugin.key, plugin.init_value_getter
            )
        prop.widget = dialog
        prop.widget.setWindowTitle(title)
        return prop.widget

    @classmethod
    def oi_connect_dialog(
        cls,
        dialog: ClassInfoWidget,
        predefined_psets: dict[str, SOMcreator.SOMPropertySet],
    ):
        dialog.widget.button_add_ifc.pressed.connect(lambda: cls.add_ifc_mapping(""))
        dialog.widget.combo_box_pset.currentTextChanged.connect(
            lambda: cls.oi_update_attribute_combobox(predefined_psets)
        )

    @classmethod
    def oi_get_focus_class(cls):
        return cls.get_object_info_properties().focus_object

    @classmethod
    def oi_get_mode(cls):
        """
        0 = Create
        1 = Info
        2 = Copy
        """
        return cls.get_object_info_properties().mode

    @classmethod
    def oi_get_values(cls) -> ClasstDataDict:
        widget = cls.get_properties().widget.widget
        d: ClasstDataDict = dict()

        d["is_group"] = widget.button_gruppe.isChecked()
        d["ident_value"] = widget.line_edit_attribute_value.text()
        d["ident_pset_name"] = widget.combo_box_pset.currentText()
        d["ident_property_name"] = widget.combo_box_attribute.currentText()
        d["name"] = widget.line_edit_name.text()
        d["ifc_mappings"] = cls.get_ifc_mappings()
        for plugin in cls.get_properties().class_info_plugin_list:
            d[plugin.key] = plugin.widget_value_getter()
        return d

    @classmethod
    def get_ifc_mappings(cls):
        widget = cls.get_properties().widget.widget
        values = list()
        for index in range(widget.vertical_layout_ifc.count()):
            item: QLineEdit = widget.vertical_layout_ifc.itemAt(index).widget()
            values.append(item.text())
        return values

    @classmethod
    def oi_set_values(cls, data_dict: ClasstDataDict):
        prop = cls.get_object_info_properties()
        if data_dict.get("name"):
            prop.name = data_dict.get("name")

        if data_dict.get("is_group") is not None:
            prop.is_group = data_dict.get("is_group")
        if data_dict.get("ident_pset_name"):
            prop.pset_name = data_dict.get("ident_pset_name")
        if data_dict.get("ident_property_name"):
            prop.attribute_name = data_dict.get("ident_property_name")
        if data_dict.get("ident_value"):
            prop.ident_value = data_dict.get("ident_value")
        if data_dict.get("ifc_mappings"):
            prop.ifc_mappings = data_dict.get("ifc_mappings")

        for plugin_values in cls.get_properties().class_info_plugin_list:
            setattr(prop, plugin_values.key, data_dict.get(plugin_values.key))

    @classmethod
    def oi_set_ident_value_color(cls, color: str):
        widget = cls.get_properties().widget.widget
        widget.line_edit_attribute_value.setStyleSheet(f"QLineEdit {{color:{color};}}")

    @classmethod
    def oi_change_visibility_identifiers(cls, hide: bool):
        prop = cls.get_properties()
        layout = prop.widget.widget.layout_ident_property
        if hide:
            for index in range(layout.count()):
                layout.itemAt(index).widget().hide()
        else:
            for index in range(layout.count()):
                layout.itemAt(index).widget().show()

    @classmethod
    def create_ifc_completer(cls):
        return QCompleter(IFC_4_1)

    @classmethod
    def oi_fill_properties(cls, mode: int):
        prop = cls.get_properties()
        info_properties = prop.object_info_widget_properties
        obj = prop.active_class
        info_properties.focus_object = obj
        info_properties.ident_value = obj.ident_value if obj else None
        info_properties.mode = mode

        for plugin in prop.class_info_plugin_list:
            info_properties.plugin_infos[plugin.key] = plugin.init_value_getter(obj)
        info_properties.is_group = obj.is_concept if obj else False
        info_properties.name = obj.name if obj else ""
        info_properties.ifc_mappings = (
            list(obj.ifc_mapping) if obj else ["IfcBuildingElementProxy"]
        )
        if obj and not obj.is_concept:
            info_properties.pset_name = obj.identifier_property.property_set.name
            info_properties.attribute_name = obj.identifier_property.name

    @classmethod
    def oi_update_dialog(cls, dialog: ClassInfoWidget):
        prop = cls.get_properties()
        info_prop = prop.object_info_widget_properties

        # set Name
        dialog.widget.line_edit_name.setText(info_prop.name)
        # set IsGroup
        dialog.widget.button_gruppe.setChecked(info_prop.is_group)

        for plugin in prop.class_info_plugin_list:
            plugin.widget_value_setter(info_prop.plugin_infos.get(plugin.key))

        for mapping in info_prop.ifc_mappings:
            cls.add_ifc_mapping(mapping)

        mode = cls.oi_get_mode()

        active_object = prop.active_class
        if mode != 0:
            dialog.widget.combo_box_pset.clear()
            [
                dialog.widget.combo_box_pset.addItem(p.name)
                for p in active_object.get_property_sets(filter=False)
            ]
        if not info_prop.is_group:
            dialog.widget.combo_box_pset.setCurrentText(info_prop.pset_name)
            dialog.widget.combo_box_attribute.setCurrentText(info_prop.attribute_name)
            dialog.widget.line_edit_attribute_value.setText(info_prop.ident_value)

    @classmethod
    def add_ifc_mapping(cls, mapping):
        line_edit = QLineEdit()
        line_edit.setCompleter(cls.create_ifc_completer())
        line_edit.setText(mapping)
        prop = cls.get_properties()
        info_prop = prop.object_info_widget_properties
        info_prop.ifc_lines.append(line_edit)
        prop.widget.widget.vertical_layout_ifc.addWidget(line_edit)

    @classmethod
    def add_objects_infos_add_function(cls, key: str, getter_function: Callable):
        cls.get_properties().class_add_infos_functions.append((key, getter_function))

    @classmethod
    def trigger_class_info_widget(mode: int):
        trigger.create_object_info_widget(mode)
