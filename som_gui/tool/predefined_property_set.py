from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, Qt, QObject, Signal
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
)

import SOMcreator
import som_gui.core.tool
import som_gui.module.compare
import som_gui.module.predefined_property_set
from som_gui import tool
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.predefined_property_set import trigger

if TYPE_CHECKING:
    from som_gui.module.predefined_property_set.prop import (
        PredefinedPsetProperties,
        PredefinedPsetCompareProperties,
    )
    from som_gui.module.predefined_property_set import ui
    from PySide6.QtGui import QAction


class Signaller(QObject):
    property_requested = Signal(SOMcreator.SOMProperty)
    active_pset_changed = Signal(SOMcreator.SOMPropertySet)
    linked_pset_requested = Signal(SOMcreator.SOMClass)
    context_menu_requested = Signal()
    new_property_requested = Signal(SOMcreator.SOMPropertySet)


class PredefinedPropertySet(som_gui.core.tool.PredefinedPropertySet):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> PredefinedPsetProperties:
        return som_gui.PredefinedPsetProperties

    @classmethod
    def connect_signals(cls):
        cls.signaller.active_pset_changed.connect(trigger.set_active_property_set)
        cls.signaller.linked_pset_requested.connect(
            trigger.activate_linked_property_set
        )

    @classmethod
    def connect_window(cls, window: ui.PredefinedPropertySetWindow):
        pset_list = window.ui.list_view_pset
        pset_list.itemSelectionChanged.connect(
            lambda: cls.signaller.active_pset_changed.emit(
                cls.get_selected_property_set()
            )
        )

        pset_list.customContextMenuRequested.connect(
            trigger.pset_context_menu_requested
        )

        pset_list.itemChanged.connect(trigger.rename_property_set)

        class_table = window.ui.table_widgets_classes
        class_table.itemDoubleClicked.connect(
            lambda i: cls.signaller.linked_pset_requested.emit(
                tool.PropertySet.get_pset_from_item(i)
            )
        )
        class_table.customContextMenuRequested.connect(
            trigger.class_context_menu_requested
        )

        window.ui.button_pset.clicked.connect(cls.create_property_set)
        window.ui.button_property.clicked.connect(
            lambda: cls.signaller.new_property_requested.emit(
                cls.get_active_property_set()
            )
        )

        som_gui.module.predefined_property_set.trigger.connect_dialog(window)

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def get_window(cls) -> ui.PredefinedPropertySetWindow:
        return cls.get_properties().predefined_property_set_window

    @classmethod
    def set_window(cls, window):
        props = cls.get_properties()
        props.predefined_property_set_window = window

    @classmethod
    def create_window(cls) -> ui.PredefinedPropertySetWindow:
        window = som_gui.module.predefined_property_set.ui.PredefinedPropertySetWindow()
        cls.set_window(window)
        return cls.get_window()

    @classmethod
    def close_window(cls):
        window = cls.get_window()
        window.hide()

    @classmethod
    def get_property_table(cls):
        if not cls.get_window():
            return None
        return cls.get_window().ui.table_properties

    @classmethod
    def get_class_table_widget(cls) -> QTableWidget:
        return cls.get_window().ui.table_widgets_classes

    @classmethod
    def get_pset_list_widget(cls):
        return cls.get_window().ui.list_view_pset

    @classmethod
    def update_pset_widget(cls):
        list_widget = cls.get_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            item.setText(item.data(CLASS_REFERENCE).name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    @classmethod
    def update_class_widget(cls):
        table_widget = cls.get_class_table_widget()
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            property_set: SOMcreator.SOMPropertySet = (
                tool.PropertySet.get_property_set_from_item(item)
            )
            item.setText(f"{property_set.som_class.name}")
            table_widget.item(row, 1).setText(f"{property_set.som_class.ident_value}")

    @classmethod
    def get_selected_property_set(cls):
        props = cls.get_properties()
        selected_items = cls.get_window().ui.list_view_pset.selectedItems()
        if not selected_items:
            return None
        return selected_items[0].data(CLASS_REFERENCE)

    @classmethod
    def set_active_property_set(cls, property_set: SOMcreator.SOMPropertySet):
        props = cls.get_properties()
        props.active_predefined_pset = property_set

    @classmethod
    def get_active_property_set(cls) -> SOMcreator.SOMPropertySet:
        props = cls.get_properties()
        return props.active_predefined_pset

    @classmethod
    def is_edit_mode_active(cls):
        props = cls.get_properties()
        return props.is_renaming_predefined_pset

    @classmethod
    def remove_property_sets_from_list_widget(
        cls, property_sets: list[SOMcreator.SOMPropertySet], list_widget: QListWidget
    ):
        rows = {
            row
            for row in range(list_widget.count())
            if list_widget.item(row).data(CLASS_REFERENCE) in property_sets
        }
        for row in reversed(sorted(rows)):
            list_widget.takeItem(row)

    @classmethod
    def remove_property_sets_from_table_widget(
        cls, property_sets: list[SOMcreator.SOMPropertySet], table_widget: QTableWidget
    ):
        remove_rows = set()
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            if tool.PropertySet.get_property_set_from_item(item) in property_sets:
                remove_rows.add(row)
        for row in reversed(sorted(remove_rows)):
            table_widget.removeRow(row)

    @classmethod
    def add_property_sets_to_widget(
        cls, property_sets: list[SOMcreator.SOMPropertySet], list_widget: QListWidget
    ):
        list_widget.setSortingEnabled(False)

        for property_set in property_sets:
            item = QListWidgetItem(property_set.name)
            item.setData(CLASS_REFERENCE, property_set)
            list_widget.addItem(item)
        list_widget.setSortingEnabled(True)

    @classmethod
    def add_classes_to_table_widget(
        cls, property_sets: list[SOMcreator.SOMPropertySet], table_widget: QTableWidget
    ):
        for property_set in property_sets:
            row_count = table_widget.rowCount()
            table_widget.setRowCount(row_count + 1)
            som_class = property_set.som_class

            item_1 = QTableWidgetItem(som_class.name)
            item_2 = QTableWidgetItem(som_class.ident_value)

            item_1.setData(CLASS_REFERENCE, property_set)
            item_2.setData(CLASS_REFERENCE, property_set)

            table_widget.setItem(row_count, 0, item_1)
            table_widget.setItem(row_count, 1, item_2)

    @classmethod
    def get_existing_psets_in_list_widget(cls, pset_list: QListWidget):
        return {
            pset_list.item(row).data(CLASS_REFERENCE)
            for row in range(pset_list.count())
        }

    @classmethod
    def get_existing_psets_in_table_widget(cls, class_table: QTableWidget):
        psets = set()
        for row in range(class_table.rowCount()):
            item = class_table.item(row, 0)
            psets.add(tool.PropertySet.get_property_set_from_item(item))
        return psets

    @classmethod
    def delete_selected_property_set(cls):
        property_set = cls.get_active_property_set()
        property_set.delete(False, False)

    @classmethod
    def rename_selected_property_set(cls):
        pset = cls.get_active_property_set()
        list_widget = cls.get_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            if tool.PropertySet.get_property_set_from_item(item) == pset:
                list_widget.editItem(item)

    @classmethod
    def create_property_set(cls):
        existing_names = [p.name for p in cls.get_property_sets()]
        name = QCoreApplication.translate("PredefinedPset", "New PropertySet")
        tool.PropertySet.create_property_set(
            tool.Util.get_new_name(name, existing_names)
        )

    @classmethod
    def get_property_sets(cls) -> set[SOMcreator.SOMPropertySet]:
        """
        get all Predefined PropertySets
        """
        proj = tool.Project.get()
        return set(proj.get_predefined_psets(filter=False))

    @classmethod
    def get_selected_linked_psets(cls) -> set[SOMcreator.SOMPropertySet]:
        return {
            tool.PropertySet.get_property_set_from_item(item)
            for item in cls.get_class_table_widget().selectedItems()
        }

    @classmethod
    def delete_selected_classes(cls):
        property_sets = cls.get_selected_linked_psets()
        for property_set in property_sets:
            property_set.delete(override_ident_deletion=False)

    @classmethod
    def remove_selected_links(cls):
        property_sets = cls.get_selected_linked_psets()
        parent = cls.get_active_property_set()
        for property_set in property_sets:
            parent.remove_child(property_set)

    @classmethod
    def clear_class_table(cls):
        table = cls.get_class_table_widget()
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)

    @classmethod
    def get_class_from_item(cls, item):
        pset = tool.PropertySet.get_property_set_from_item(item)
        som_class = pset.som_class
        return som_class

    @classmethod
    def name_is_in_predefined_psets(cls, name: str):
        return name in [p.name for p in cls.get_property_sets()]

    @classmethod
    def get_pset_by_name(cls, name: str):
        return {p.name: p for p in cls.get_property_sets()}.get(name)


class PredefinedPropertySetCompare(som_gui.core.tool.PredefinedPropertySetCompare):

    @classmethod
    def get_properties(cls) -> PredefinedPsetCompareProperties:
        return som_gui.PredefinedPsetCompareProperties

    @classmethod
    def reset(cls):
        cls.get_properties().widget = None
        cls.get_properties().predefined_psets = None
        cls.get_properties().pset_lists = list()
        cls.get_properties().value_dict = dict()

    @classmethod
    def create_pset_list(
        cls,
        psets0: list[SOMcreator.SOMPropertySet],
        psets1: list[SOMcreator.SOMPropertySet],
    ):
        uuid_dict = tool.PropertyCompare.generate_uuid_dict(psets1)
        name_dict = tool.PropertyCompare.generate_name_dict(psets1)
        pset_list = list()
        missing = list(psets1)
        for pset in psets0:
            logging.debug(f"Search for Pset {pset}")
            match = tool.PropertyCompare.find_matching_entity(
                pset, uuid_dict, name_dict
            )
            if match:
                if match not in missing:
                    logging.debug(
                        f"Pset found: {match} Match not in missing -> append empty"
                    )
                    pset_list.append((pset, None))
                else:
                    logging.debug(
                        f"Pset found: {match} Match is in missing -> append Entry"
                    )
                    pset_list.append((pset, match))
                    missing.remove(match)
            else:
                logging.debug(f"Pset NOT found: {match}")
                pset_list.append((pset, None))
        for pset in missing:
            pset_list.append((None, pset))

        cls.set_pset_lists(pset_list)
        return pset_list

    @classmethod
    def create_tree_selection_trigger(cls, widget: ui.CompareWidget):
        widget.ui.tree_widget_propertysets.itemSelectionChanged.connect(
            lambda: som_gui.module.property_.trigger.pset_tree_selection_changed(widget)
        )

    @classmethod
    def create_widget(cls):
        from som_gui.module.predefined_property_set import ui

        if cls.get_properties().widget is None:
            cls.get_properties().widget = ui.CompareWidget()
        return cls.get_properties().widget

    @classmethod
    def set_predefined_psets(cls, psets0, psets1):
        cls.get_properties().predefined_psets = (psets0, psets1)

    @classmethod
    def set_pset_lists(
        cls,
        pset_lists: list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]],
    ) -> None:
        cls.get_properties().pset_lists = pset_lists

    @classmethod
    def get_pset_lists(
        cls,
    ) -> list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]]:
        return cls.get_properties().pset_lists
