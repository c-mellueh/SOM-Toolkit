
from __future__ import annotations
from typing import TYPE_CHECKING,Callable
import logging

import som_gui.core.tool
import som_gui

from PySide6.QtCore import Slot,Signal,QObject,QCoreApplication,Qt
from PySide6.QtWidgets import QLayout
import SOMcreator
from som_gui.module.property_window import ui,trigger
from som_gui.module.property_window.prop import PropertyWindowProperties,PluginProperty

class Signaller(QObject):
    name_changed = Signal(SOMcreator.SOMProperty)

class PropertyWindow(som_gui.core.tool.PropertyWindow):
    signaller = Signaller()
    
    @classmethod
    def get_properties(cls) -> PropertyWindowProperties:
        return som_gui.PropertyWindowProperties

    @classmethod
    def property_info_requested(cls,som_property:SOMcreator.SOMProperty):
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
    def create_window(cls, som_property:SOMcreator.SOMProperty) -> ui.PropertyWindow:
        prop = cls.get_properties()
        prop.windows[som_property] =  ui.PropertyWindow(som_property)
        for plugin in prop.plugin_widget_list:
            layout: QLayout = getattr(cls.get_ui(), plugin.layout_name)
            layout.insertWidget(plugin.index, plugin.widget())
            setattr(prop, plugin.key, plugin.value_getter)
        title = cls.create_window_title(som_property)
        cls.get_window(som_property).setWindowTitle(title) #TODO: Update Name Getter
        return cls.get_window(som_property)
    
    @classmethod
    def get_window(cls,som_property:SOMcreator.SOMProperty) ->ui.PropertyWindow|None:
        return cls.get_properties().windows.get(som_property) 
    @classmethod
    def get_ui(cls,som_property:SOMcreator.SOMProperty):
        window = cls.get_window(som_property)
        return window.ui if window else None

    @classmethod
    def create_window_title(cls,som_property:SOMcreator.SOMProperty):
            SEPERATOR = " : "
            text = som_property.name
            pset = som_property.property_set
            if not pset:
                return text
            text = pset.name+SEPERATOR+text
            som_class = pset.som_class
            if not som_class:
                return text
            return som_class.name+SEPERATOR+text
    
    @classmethod
    def get_property_from_window(cls,window:ui.PropertyWindow):
        return window.som_property
    
    @classmethod
    def rename_property(cls,som_property:SOMcreator.SOMProperty,value:str):
        som_property.name = value
        cls.signaller.name_changed.emit(som_property)
    
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