from __future__ import annotations
import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui.tool import Object, Project
from PySide6.QtWidgets import QTableWidgetItem, QCompleter
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE
from SOMcreator.constants.json_constants import INHERITED_TEXT
from som_gui.icons import get_link_icon
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.property_set.prop import PropertySetProperties
from som_gui.module.property_set import ui


class PropertySet(som_gui.core.tool.PropertySet):
    @classmethod
    def get_pset_from_item(cls, item: QTableWidgetItem):
        return item.data(CLASS_REFERENCE)

    @classmethod
    def get_existing_psets_in_table(cls):
        table = cls.get_table()
        psets = set()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            psets.add(cls.get_pset_from_item(item))
        return psets

    @classmethod
    def clear_table(cls):
        table = cls.get_table()
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)

    @classmethod
    def get_property_sets(cls) -> set[SOMcreator.PropertySet]:
        active_object = Object.get_active_object()
        if active_object is None:
            return set()
        return set(active_object.property_sets)

    @classmethod
    def get_table(cls):
        return som_gui.MainUi.ui.table_pset

    @classmethod
    def get_row_from_pset(cls, property_set: SOMcreator.PropertySet):
        table = cls.get_table()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_pset_from_item(item) == property_set:
                return row

    @classmethod
    def remove_property_sets_from_table(cls, property_sets: set[SOMcreator.PropertySet]):
        d = {cls.get_row_from_pset(p): p for p in property_sets}
        table = cls.get_table()
        for row in reversed(d.keys()):
            table.removeRow(row)

    @classmethod
    def add_property_sets_to_table(cls, property_sets: set[SOMcreator.PropertySet]):
        table = cls.get_table()
        for property_set in property_sets:
            items = [QTableWidgetItem() for _ in range(3)]
            row = table.rowCount()
            table.setRowCount(row + 1)
            [item.setData(CLASS_REFERENCE, property_set) for item in items]
            [table.setItem(row, col, item) for col, item in enumerate(items)]
            check_state = Qt.CheckState.Checked if property_set.optional else Qt.CheckState.Unchecked
            items[0].setText(f"{property_set.name}")
            if property_set.is_child:
                text = property_set.parent.name if property_set.parent.object is not None else INHERITED_TEXT
                items[1].setText(text)
                items[0].setIcon(get_link_icon())
            items[2].setCheckState(check_state)

    @classmethod
    def get_predefined_psets(cls) -> set[SOMcreator.PropertySet]:
        proj = Project.get()
        return proj.get_predefined_psets()

    @classmethod
    def get_selecte_property_set(cls) -> SOMcreator.PropertySet:
        table = cls.get_table()
        items = table.selectedItems()
        if not items:
            return
        item = items[0]
        return cls.get_pset_from_item(item)

    @classmethod
    def update_completer(cls):
        psets = [pset.name for pset in cls.get_predefined_psets()]
        completer = QCompleter(psets)
        som_gui.MainUi.ui.lineEdit_ident_pSet.setCompleter(completer)
        som_gui.MainUi.ui.lineEdit_pSet_name.setCompleter(completer)

    @classmethod
    def set_enabled(cls, enabled: bool):
        layout = som_gui.MainUi.ui.box_layout_pset
        layout.setEnabled(enabled)

    @classmethod
    def get_pset_properties(cls) -> PropertySetProperties:
        return som_gui.PropertySetProperties

    @classmethod
    def set_active_pset(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_pset_properties()
        prop.active_pset = property_set
        obj = Object.get_active_object()

        from som_gui.windows import propertyset_window
        propertyset_window.fill_attribute_table(obj, som_gui.MainUi.ui.table_attribute, property_set)

    @classmethod
    def open_pset_window(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_pset_properties()
        widget = ui.PropertySetWindow()
        prop.property_set_windows.append(widget)
        widget.show()
