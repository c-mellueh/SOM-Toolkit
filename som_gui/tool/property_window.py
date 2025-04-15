from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import logging

import som_gui.core.tool
import som_gui

from PySide6.QtCore import Slot, Signal, QObject, QCoreApplication, Qt
from PySide6.QtWidgets import QLayout, QCompleter, QComboBox
import SOMcreator
from som_gui.module.property_window import ui, trigger
from som_gui.module.property_window.prop import PropertyWindowProperties, PluginProperty
from SOMcreator.constants.value_constants import DATA_TYPES, VALUE_TYPES
from SOMcreator.constants import value_constants

if TYPE_CHECKING:
    from som_gui.module.property_window.qt.ui_Window import Ui_PropertyWindow
test_index = None


class Signaller(QObject):
    name_changed = Signal(SOMcreator.SOMProperty)
    datatype_changed = Signal(SOMcreator.SOMProperty)
    valuetype_changed = Signal(SOMcreator.SOMProperty)
    unit_changed = Signal(SOMcreator.SOMProperty)
    description_changed = Signal(SOMcreator.SOMProperty)
    values_changed = Signal(SOMcreator.SOMClass)


class PropertyWindow(som_gui.core.tool.PropertyWindow):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> PropertyWindowProperties:
        return som_gui.PropertyWindowProperties

    @classmethod
    def property_info_requested(cls, som_property: SOMcreator.SOMProperty):
        trigger.property_info_requested(som_property)

    @classmethod
    def add_plugin_entry(
        cls,
        key: str,
        layout_name: str,
        widget_creator: Callable,
        index: int,
        value_getter: Callable,
        value_setter: Callable,
        widget_value_setter: Callable,
        test_function: Callable,
    ) -> int:
        """
        Create entry of QWidget that will be added to Class Info Dialog
        layout_name: name of layout in which QWidget will be placed
        widget_creator: Widget that will be placed
        index: index of position in layout where widget will be placed
        value_getter: function that gets the value that will be displayed in the widget
        value_setter: function that will update the value in the property if the value changes
        widget_value_setter: function that sets value in the widget
        test_function: function that get's called to check if value written in widget is valid for class
        return: index of plugin in list
        """
        prop = PluginProperty(
            key,
            layout_name,
            widget_creator,
            index,
            value_getter,
            value_setter,
            widget_value_setter,
            test_function,
        )

        cls.get_properties().plugin_widget_list.append(prop)
        return len(cls.get_properties().plugin_widget_list) - 1

    @classmethod
    def remove_plugin_entry(cls, key: str):
        for plugin in reversed(cls.get_properties().plugin_widget_list):
            if plugin.key == key:
                cls.get_properties().plugin_widget_list.remove(plugin)
                break

    @classmethod
    def remove_window(cls, window: ui.PropertyWindow):
        cls.get_properties().windows.pop(window.som_property)

    @classmethod
    def create_window(cls, som_property: SOMcreator.SOMProperty) -> ui.PropertyWindow:
        prop = cls.get_properties()
        prop.windows[som_property] = ui.PropertyWindow(som_property)
        for plugin in prop.plugin_widget_list:
            layout: QLayout = getattr(cls.get_ui(), plugin.layout_name)
            layout.insertWidget(plugin.index, plugin.widget())
            setattr(prop, plugin.key, plugin.value_getter)
        title = cls.create_window_title(som_property)
        cls.get_window(som_property).setWindowTitle(title)  # TODO: Update Name Getter
        return cls.get_window(som_property)

    @classmethod
    def get_window(
        cls, som_property: SOMcreator.SOMProperty
    ) -> ui.PropertyWindow | None:
        return cls.get_properties().windows.get(som_property)

    @classmethod
    def get_windows(cls) -> set[ui.PropertyWindow]:
        return set(cls.get_properties().windows.values())

    @classmethod
    def get_ui(cls, som_property: SOMcreator.SOMProperty):
        window = cls.get_window(som_property)
        return window.ui if window else None

    @classmethod
    def create_window_title(cls, som_property: SOMcreator.SOMProperty):
        SEPERATOR = " : "
        text = som_property.name
        pset = som_property.property_set
        if not pset:
            return text
        text = pset.name + SEPERATOR + text
        som_class = pset.som_class
        if not som_class:
            return text
        return som_class.name + SEPERATOR + text

    @classmethod
    def get_property_from_window(cls, window: ui.PropertyWindow):
        return window.som_property

    @classmethod
    def rename_property(cls, som_property: SOMcreator.SOMProperty, value: str):
        som_property.name = value
        cls.signaller.name_changed.emit(som_property)

    @classmethod
    def set_datatype(cls, som_property: SOMcreator.SOMProperty, value: str):
        som_property.data_type = value
        cls.signaller.datatype_changed.emit(som_property)

    @classmethod
    def set_valuetype(cls, som_property: SOMcreator.SOMProperty, value: str):
        som_property.value_type = value
        cls.signaller.valuetype_changed.emit(som_property)

    @classmethod
    def set_unit(cls, som_property: SOMcreator.SOMProperty, value: str):
        som_property.unit = value
        cls.signaller.unit_changed.emit(som_property)

    @classmethod
    def set_description(cls, som_property: SOMcreator.SOMProperty, value: str):
        som_property.description = value
        cls.signaller.description_changed.emit(som_property)

    @classmethod
    def set_value_inherit_state(cls, som_property: SOMcreator.SOMProperty, value: bool):
        som_property.child_inherits_values = value

    @classmethod
    def get_datatype_combobox(cls, widget_ui: Ui_PropertyWindow) -> QComboBox:
        return widget_ui.combo_data_type

    @classmethod
    def get_valuetype_combobox(cls, widget_ui: Ui_PropertyWindow) -> QComboBox:
        return widget_ui.combo_value_type

    @classmethod
    def get_unit_combobox(cls, widget_ui: Ui_PropertyWindow):
        return widget_ui.combo_unit

    @classmethod
    def get_description_textedit(cls, widget_ui: Ui_PropertyWindow):
        return widget_ui.description

    @classmethod
    def set_comboboxes_enabled(cls, enabled_state: bool, window: ui.PropertyWindow):
        window.ui.combo_value_type.setEnabled(enabled_state)
        window.ui.combo_data_type.setEnabled(enabled_state)
        window.ui.combo_unit.setEnabled(enabled_state)
        if enabled_state:
            t1 = QCoreApplication.translate(
                "PropertyWindow",
                "Property was inherited -> Type change not possible",
            )
            t2 = QCoreApplication.translate(
                "PropertyWindow",
                "Property was inherited -> DataType change not possible",
            )
            t3 = QCoreApplication.translate(
                "PropertyWindow",
                "Property was inherited -> Unit change not possible",
            )
        else:
            t1 = t2 = t3 = ""
        window.ui.combo_value_type.setToolTip(t1)
        window.ui.combo_data_type.setToolTip(t2)
        window.ui.combo_unit.setToolTip(t3)

    @classmethod
    def prefill_comboboxes(cls, window: ui.PropertyWindow):
        window.ui.combo_value_type.clear()
        window.ui.combo_value_type.addItems(cls.get_allowed_value_types())
        window.ui.combo_data_type.clear()
        window.ui.combo_data_type.addItems(cls.get_allowed_data_types())
        window.ui.combo_value_type.setCurrentText(value_constants.LIST)
        window.ui.combo_data_type.setCurrentText(value_constants.LABEL)

    @classmethod
    def get_allowed_value_types(cls):
        return VALUE_TYPES

    @classmethod
    def get_allowed_data_types(cls):
        return DATA_TYPES

    @classmethod
    def update_unit_completer(cls, window: ui.PropertyWindow):
        cb = window.ui.combo_unit
        cb.setCompleter(QCompleter([cb.itemText(i) for i in range(cb.count())]))

    @classmethod
    def connect_value_view(cls, window: ui.PropertyWindow):
        som_property = cls.get_property_from_window(window)
        table_view = window.ui.table_view_value
        table_view.som_property = som_property
        model = ui.ValueModel(som_property)
        sort_model = ui.SortModel(som_property)
        sort_model.setSourceModel(model)
        table_view.setModel(sort_model)
        table_view.customContextMenuRequested.connect(
            lambda pos: trigger.value_context_menu_request(pos, table_view)
        )

    @classmethod
    def add_context_menu_builder(cls, context_menu_builder: Callable):
        """
        :param context_menu_builder: Function which gets called on context menu creation.
        should return tuple[name, function] of context should be shown or None if not shown.
        The function gets passed the current table as a variable
        :return:
        """
        cls.get_properties().context_menu_builders.append(context_menu_builder)

    @classmethod
    def get_selected_values(cls, table_view: ui.ValueView):
        model = table_view.model()
        av = table_view.som_property.all_values
        selected_indexes = [model.mapToSource(i) for i in table_view.selectedIndexes()]
        return [av[i.row()] for i in selected_indexes]

    @classmethod
    def remove_builder(cls, table_view: ui.ValueView):
        values = cls.get_selected_values(table_view)
        if not values:
            return None
        name = QCoreApplication.translate("PropertySetWindow", "Remove")
        action = lambda: cls.remove_selected_values(table_view)
        return name, action

    @classmethod
    def ignore_builder(cls, table_view: ui.ValueView):
        som_property = table_view.som_property
        values = cls.get_selected_values(table_view)
        are_values_ignored = [
            som_property.is_value_ignored(v)
            for v in values
            if som_property.is_value_inherited(v)
        ]
        if all(are_values_ignored):
            return
        name = QCoreApplication.translate("PropertySetWindow", "Ignore")
        action = lambda: cls.set_selecteded_values_ignored(table_view, True)
        return name, action

    @classmethod
    def unignore_builder(cls, table_view: ui.ValueView):
        som_property = table_view.som_property
        values = cls.get_selected_values(table_view)
        are_values_ignored = [
            som_property.is_value_ignored(v)
            for v in values
            if som_property.is_value_inherited(v)
        ]
        if not any(are_values_ignored):
            return
        name = QCoreApplication.translate("PropertySetWindow", "Unignore")
        action = lambda: cls.set_selecteded_values_ignored(table_view, False)
        return name, action

    @classmethod
    def set_selecteded_values_ignored(cls, table_view: ui.ValueView, state: bool):
        som_property = table_view.som_property
        av = som_property.all_values
        for index in table_view.selectedIndexes():
            index = table_view.model().mapToSource(index)
            value = av[index.row()]
            if state:
                som_property.ignore_parent_value(value)
            else:
                som_property.unignore_parent_value(value)
        table_view.model().sourceModel().update_values()

    @classmethod
    def remove_selected_values(cls, table_view: ui.ValueView):
        som_property = table_view.som_property
        av = som_property.all_values
        model = table_view.model().sourceModel()
        for index in reversed(
            sorted(table_view.selectedIndexes(), key=lambda i: i.row())
        ):
            index = table_view.model().mapToSource(index)
            value = av[index.row()]
            if som_property.is_value_inherited(value):
                som_property.ignore_parent_value(value)
                model.dataChanged.emit(index, index, Qt.ItemDataRole.EditRole)
            else:
                table_view.model().sourceModel().removeRow(index.row())
                cls.signaller.values_changed.emit(som_property)

    @classmethod
    def get_context_menu_builders(cls) -> list:
        """
        Functions that are getting called if context menu is requested. Return tuple with name and function or None # Each builder gets passed the current table
        """
        return cls.get_properties().context_menu_builders

    @classmethod
    def add_value(cls, table_view: ui.ValueView, value=""):
        model = table_view.model().sourceModel()
        model.append_row()
        model.setData(
            model.createIndex(model.rowCount() - 1, 0, None),
            value,
            Qt.ItemDataRole.EditRole,
        )
        cls.signaller.values_changed.emit(table_view.som_property)
