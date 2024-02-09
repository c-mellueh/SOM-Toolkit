from __future__ import annotations
import som_gui.core.tool
import som_gui.module.predefined_property_set
import SOMcreator
from som_gui.module.project.constants import CLASS_REFERENCE
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from som_gui import tool

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.predefined_property_set.prop import PredefinedPsetProperties
    from som_gui.module.predefined_property_set import ui


class PredefinedPropertySet(som_gui.core.tool.PredefinedPropertySet):

    @classmethod
    def get_properties(cls) -> PredefinedPsetProperties:
        return som_gui.PredefinedPsetProperties

    @classmethod
    def get_window(cls) -> ui.PredefinedPropertySetWindow:
        return cls.get_properties().predefined_property_set_window

    @classmethod
    def connect_window_triggers(cls, window):
        som_gui.module.predefined_property_set.trigger.connect_dialog(window)

    @classmethod
    def set_predefined_pset_window(cls, window):
        props = cls.get_properties()
        props.predefined_property_set_window = window

    @classmethod
    def create_predefined_pset_window(cls) -> ui.PredefinedPropertySetWindow:
        window = som_gui.module.predefined_property_set.ui.PredefinedPropertySetWindow()
        cls.set_predefined_pset_window(window)
        return cls.get_window()

    @classmethod
    def get_predefined_pset_inheritance_list(cls):
        return cls.get_window().widget.list_view_existance

    @classmethod
    def get_predefine_pset_list_widget(cls):
        return cls.get_window().widget.list_view_pset

    @classmethod
    def update_predefined_pset_list(cls):
        list_widget = cls.get_predefine_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            item.setText(item.data(CLASS_REFERENCE).name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    @classmethod
    def update_predefined_pset_inheritance_list(cls):
        list_widget = cls.get_predefined_pset_inheritance_list()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            property_set: SOMcreator.PropertySet = item.data(CLASS_REFERENCE)
            item.setText(f"{property_set.object.name}")

    @classmethod
    def close_predefined_pset_window(cls):
        window = cls.get_window()
        window.hide()

    @classmethod
    def get_selected_predef_property_set(cls):
        props = cls.get_properties()
        return props.predefined_property_set_window.widget.list_view_pset.selectedItems()[0].data(CLASS_REFERENCE)

    @classmethod
    def set_predef_property_set(cls, property_set: SOMcreator.PropertySet):
        props = cls.get_properties()
        props.active_predefined_pset = property_set

    @classmethod
    def get_active_predefined_pset(cls) -> SOMcreator.PropertySet:
        props = cls.get_properties()
        return props.active_predefined_pset

    @classmethod
    def predefined_pset_list_is_editing(cls):
        props = cls.get_properties()
        return props.is_renaming_predefined_pset

    @classmethod
    def remove_property_sets_from_list(cls, property_sets: list[SOMcreator.PropertySet], list_widget: QListWidget):
        rows = {row for row in range(list_widget.count()) if
                list_widget.item(row).data(CLASS_REFERENCE) in property_sets}
        for row in reversed(sorted(rows)):
            list_widget.takeItem(row)

    @classmethod
    def add_property_sets_to_list(cls, property_sets: list[SOMcreator.PropertySet], list_widget: QListWidget):
        list_widget.setSortingEnabled(False)

        for property_set in property_sets:
            item = QListWidgetItem(property_set.name)
            item.setData(CLASS_REFERENCE, property_set)
            list_widget.addItem(item)
        list_widget.setSortingEnabled(True)

    @classmethod
    def add_property_sets_to_inheritance_list(cls, property_sets: list[SOMcreator.PropertySet],
                                              list_widget: QListWidget):
        list_widget.setSortingEnabled(False)
        for property_set in property_sets:
            item = QListWidgetItem(property_set.object.name)
            item.setData(CLASS_REFERENCE, property_set)
            list_widget.addItem(item)
        list_widget.setSortingEnabled(True)

    @classmethod
    def get_existing_psets_in_list(cls, pset_list: QListWidget):
        return {pset_list.item(row).data(CLASS_REFERENCE) for row in range(pset_list.count())}

    @classmethod
    def delete_predefined_pset(cls):
        property_set = cls.get_active_predefined_pset()
        property_set.delete(False, False)

    @classmethod
    def rename_predefined_pset(cls):
        pset = cls.get_active_predefined_pset()
        list_widget = cls.get_predefine_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            if tool.PropertySet.get_property_set_from_item(item) == pset:
                list_widget.editItem(item)

    @classmethod
    def add_predefined_pset(cls):
        existing_names = [p.name for p in cls.get_predefined_psets()]
        tool.PropertySet.create_property_set(
            tool.ObjectFilter.get_new_use_case_name("Neues PropertySet", existing_names))

    @classmethod
    def get_predefined_psets(cls) -> set[SOMcreator.PropertySet]:
        proj = tool.Project.get()
        return proj.get_predefined_psets()
