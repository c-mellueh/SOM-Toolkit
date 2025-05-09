from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from som_gui.module.class_info.prop import PluginProperty
from som_gui.module.class_.prop import ClassDataDict
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QLineEdit, QCompleter, QLayout
from PySide6.QtCore import QCoreApplication, Qt
import logging

if TYPE_CHECKING:
    from som_gui.module.class_info.prop import ClassInfoProperties
    from som_gui.module.ifc_schema.ui import MappingWidget
import som_gui.core.tool
from som_gui import tool
import SOMcreator
from som_gui.module.class_info.ui import (
    ClassInfoDialog,
    Ui_ClassInfo,
)
from SOMcreator.templates import IFC_4_1
from som_gui.module.class_info import trigger
import som_gui.module.class_tree.constants
from som_gui.module.ifc_schema.constants import PREDEFINED_SPLITTER


class ClassInfo(som_gui.core.tool.ClassInfo):
    @classmethod
    def get_properties(cls) -> ClassInfoProperties:
        return som_gui.ClassInfoProperties

    @classmethod
    def get_dialog(cls) -> ClassInfoDialog | None:
        return cls.get_properties().dialog

    @classmethod
    def get_ui(cls) -> Ui_ClassInfo | None:
        if cls.get_dialog() is None:
            return None
        return cls.get_dialog().ui

    @classmethod
    def remove_plugin_entry(cls, key: str):
        for plugin in reversed(cls.get_properties().class_info_plugin_list):
            if plugin.key == key:
                cls.get_properties().class_info_plugin_list.remove(plugin)
                break

    @classmethod
    def add_plugin_entry(
        cls,
        key: str,
        layout_name: str,
        widget_creator: Callable,
        index: int,
        init_value_getter: Callable,
        widget_value_getter: Callable,
        widget_value_setter: Callable,
        test_function: Callable,
        value_setter: Callable,
    ) -> int:
        """
        Create entry of QWidget that will be added to Class Info Dialog
        layout_name: name of layout in which QWidget will be placed
        widget: Widget that will be placed
        index: index of position in layout where widget will be placed
        init_value_getter: function that gets the initial value that will be displayed in the widget
        widget_value_setter: function that will set a given value in the widget
        test_function: function that get's called to check if value written in widget is valid for class
        value_setter: function thats sets value of class after ClassInfoWidget is accepted
        return: index of plugin in list
        """
        prop = PluginProperty(
            key,
            layout_name,
            widget_creator,
            index,
            init_value_getter,
            widget_value_getter,
            widget_value_setter,
            test_function,
            value_setter,
        )

        cls.get_properties().class_info_plugin_list.append(prop)
        return len(cls.get_properties().class_info_plugin_list) - 1

    @classmethod
    def get_class_infos(cls) -> ClassDataDict:
        d = dict()
        for key, func in cls.get_properties().class_add_infos_functions:
            d[key] = func()
        return d

    @classmethod
    def update_property_combobox(
        cls, predefined_psets: list[SOMcreator.SOMPropertySet]
    ):
        ui = cls.get_ui()
        pset_name = ui.combo_box_pset.currentText()
        mode = cls.get_mode()
        search_psets = predefined_psets
        if mode != 0:
            search_psets += list(cls.get_active_class().get_property_sets())
        property_set = {p.name: p for p in search_psets}.get(pset_name)
        if not property_set:
            return
        pr_names = [pr.name for pr in property_set.get_properties(filter=False)]
        ui.combo_box_property.clear()
        ui.combo_box_property.addItems(pr_names)
        tool.Util.create_completer(pr_names, ui.combo_box_property)

    @classmethod
    def create_dialog(cls, title, ifc_versions: list[str]) -> ClassInfoDialog:
        prop = cls.get_properties()
        prop.dialog = ClassInfoDialog()
        for plugin in prop.class_info_plugin_list:
            layout: QLayout = getattr(cls.get_ui(), plugin.layout_name)
            layout.insertWidget(plugin.index, plugin.widget(prop.dialog))
            setattr(prop, plugin.key, plugin.init_value_getter)
        dl = cls.get_dialog()
        dl.setWindowTitle(title)
        return dl

    @classmethod
    def reset(cls):
        cls.get_properties().dialog = None
        cls.get_properties().ifc_line_edits = []
        cls.set_active_class(None)
        cls.get_properties().ifc_mappings = []

    @classmethod
    def connect_dialog(
        cls,
        dialog: ClassInfoDialog,
        predefined_psets: list[SOMcreator.SOMPropertySet],
    ):
        dialog.ui.combo_box_pset.currentTextChanged.connect(
            lambda: cls.update_property_combobox(predefined_psets)
        )

    @classmethod
    def get_active_class(cls) -> SOMcreator.SOMClass:
        return cls.get_properties().active_class

    @classmethod
    def set_active_class(cls, value: SOMcreator.SOMClass):
        cls.get_properties().active_class = value

    @classmethod
    def get_mode(cls) -> int:
        """
        0 = Create
        1 = Info
        2 = Copy
        """
        return cls.get_properties().mode

    @classmethod
    def generate_datadict(cls) -> ClassDataDict:
        ui = cls.get_ui()
        if ui is None:
            return {}
        d: ClassDataDict = dict()
        d["is_group"] = ui.button_gruppe.isChecked()
        d["ident_value"] = ui.line_edit_property_value.text()
        d["ident_pset_name"] = ui.combo_box_pset.currentText()
        d["ident_property_name"] = ui.combo_box_property.currentText()
        d["name"] = ui.line_edit_name.text()
        d["ifc_mappings"] = cls.get_ifc_mappings()
        d["description"] = ui.text_edit_description.toPlainText()
        for plugin in cls.get_properties().class_info_plugin_list:
            d[plugin.key] = plugin.widget_value_getter()
        return d

    @classmethod
    def get_ifc_mappings(cls):
        ui = cls.get_ui()
        version_dict = dict()
        for widget_row in range(ui.toolBox.count()):
            widget: MappingWidget = ui.toolBox.widget(widget_row)
            tv = widget.ui.table_view
            version = widget.version
            model: QStandardItemModel = tv.model()
            values = list()
            for row in range(model.rowCount()):
                entity_index = model.index(row, 0)
                predefined_index = model.index(row, 1)
                if entity_index.isValid():
                    text = entity_index.data(Qt.ItemDataRole.DisplayRole)
                    predef_text = predefined_index.data(Qt.ItemDataRole.DisplayRole)
                    if predef_text:
                        text = f"{text}{PREDEFINED_SPLITTER}{predef_text}"
                    values.append(text)
            version_dict[version] = values
        return version_dict

    @classmethod
    def oi_set_values(cls, data_dict: ClassDataDict):
        prop = cls.get_properties()
        if data_dict.get("name"):
            prop.class_name = data_dict.get("name")

        if data_dict.get("is_group") is not None:
            prop.is_group = data_dict.get("is_group")
        if data_dict.get("ident_pset_name"):
            prop.pset_name = data_dict.get("ident_pset_name")
        if data_dict.get("ident_property_name"):
            prop.ident_property_name = data_dict.get("ident_property_name")
        if data_dict.get("ident_value"):
            prop.ident_value = data_dict.get("ident_value")
        if data_dict.get("ifc_mappings"):
            prop.ifc_mappings = data_dict.get("ifc_mappings")

        for plugin_values in cls.get_properties().class_info_plugin_list:
            setattr(prop, plugin_values.key, data_dict.get(plugin_values.key))

    @classmethod
    def oi_set_ident_value_color(cls, color: str):
        cls.get_ui().line_edit_property_value.setStyleSheet(
            f"QLineEdit {{color:{color};}}"
        )

    @classmethod
    def oi_change_visibility_identifiers(cls, hide: bool):
        prop = cls.get_properties()
        layout = cls.get_ui().layout_ident_property
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
        active_class = cls.get_active_class()
        prop.ident_value = active_class.ident_value if active_class else None
        prop.mode = mode

        for plugin in prop.class_info_plugin_list:
            prop.plugin_infos[plugin.key] = plugin.init_value_getter(active_class)
        prop.is_group = active_class.is_concept if active_class else False
        prop.class_name = active_class.name if active_class else ""
        prop.ifc_mappings = (
            list(active_class.ifc_mapping)
            if active_class
            else ["IfcBuildingElementProxy"]
        )
        if active_class and not active_class.is_concept:
            prop.pset_name = active_class.identifier_property.property_set.name
            prop.ident_property_name = active_class.identifier_property.name

        if active_class:
            prop.description = active_class.description

    @classmethod
    def update_dialog(cls, dialog: ClassInfoDialog):
        prop = cls.get_properties()

        # set Name
        dialog.ui.line_edit_name.setText(prop.class_name)
        # set IsGroup
        dialog.ui.button_gruppe.setChecked(prop.is_group)

        for plugin in prop.class_info_plugin_list:
            plugin.widget_value_setter(prop.plugin_infos.get(plugin.key))

        mode = cls.get_mode()
        dialog.ui.text_edit_description.setPlainText(prop.description or "")
        active_class = cls.get_active_class()
        if mode != 0:
            dialog.ui.combo_box_pset.clear()
            [
                dialog.ui.combo_box_pset.addItem(p.name)
                for p in active_class.get_property_sets(filter=False)
            ]
        if not prop.is_group:
            dialog.ui.combo_box_pset.setCurrentText(prop.pset_name)
            dialog.ui.combo_box_property.setCurrentText(prop.ident_property_name)
            dialog.ui.line_edit_property_value.setText(prop.ident_value)

    @classmethod
    def add_classes_infos_add_function(cls, key: str, getter_function: Callable):
        cls.get_properties().class_add_infos_functions.append((key, getter_function))

    @classmethod
    def trigger_class_info_widget(
        cls, mode: int, som_class: SOMcreator.SOMClass = None
    ):
        trigger.create_class_info_widget(mode, som_class)

    @classmethod
    def are_plugin_requirements_met(
        cls, som_class: SOMcreator.SOMClass, data_dict: ClassDataDict
    ):
        """
        set som_class to None if no som_class exists (creation of new class) this will skip ignore
        """
        for plugin in cls.get_properties().class_info_plugin_list:  # Call Test Func
            result = plugin.value_test(data_dict[plugin.key], som_class)
            if result != som_gui.module.class_tree.constants.OK:
                return result
        return som_gui.module.class_tree.constants.OK

    @classmethod
    def is_ident_pset_valid(cls, data_dict: ClassDataDict):
        is_group = data_dict["is_group"]
        if is_group:
            return True
        value = data_dict["ident_pset_name"]
        if not value:
            text = QCoreApplication.translate(
                "Class", "Name of PropertySet is not allowed"
            )
            logging.error(text)
            tool.Popups.create_warning_popup(text)
            return False
        return True

    @classmethod
    def is_ident_property_valid(cls, data_dict: ClassDataDict):
        is_group = data_dict["is_group"]
        if is_group:
            return True
        value = data_dict["ident_property_name"]
        if not value:
            text = QCoreApplication.translate(
                "Class", "Name of Property is not allowed"
            )
            logging.error(text)
            return False
        return True

    @classmethod
    def is_identifier_unique(cls, data_dict: ClassDataDict):
        is_group = data_dict["is_group"]
        if is_group:
            return True
        value = data_dict["ident_value"]
        if not cls.is_identifier_allowed(value):
            text = QCoreApplication.translate(
                "Class", "Identifier exists allready or is not allowed"
            )
            logging.error(text)
            return False
        return True

    @classmethod
    def add_plugin_infos_to_class(
        cls, som_class: SOMcreator.SOMClass, data_dict: ClassDataDict
    ):
        for plugin in cls.get_properties().class_info_plugin_list:  # call Setter Func
            plugin.value_setter(som_class, data_dict[plugin.key])

    @classmethod
    def get_ifc_lineedits(cls):
        return cls.get_properties().ifc_line_edits

    @classmethod
    def append_ifc_lineedit(cls, line_edit: QLineEdit):
        cls.get_properties().ifc_line_edits.append(line_edit)
        cls.get_ui().vertical_layout_ifc.addWidget(line_edit)
