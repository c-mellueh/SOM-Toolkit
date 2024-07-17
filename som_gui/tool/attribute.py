from __future__ import annotations

import logging

import SOMcreator
import som_gui.core.tool
from typing import Callable, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from som_gui.module.attribute.prop import AttributeProperties


class Attribute(som_gui.core.tool.Attribute):
    @classmethod
    def set_inherit_state(cls, state: bool, attribute: SOMcreator.Attribute):
        attribute.child_inherits_values = state

    @classmethod
    def get_inherit_state(cls, attribute: SOMcreator.Attribute):
        return attribute.child_inherits_values

    @classmethod
    def delete(cls, attributes: set[SOMcreator.Attribute], with_subattributes=False):
        for attribute in attributes:
            attribute.delete(with_subattributes)

    @classmethod
    def add_attribute_data_value(cls, name: str, getter: Callable, setter: Callable):
        prop = cls.get_attribute_properties()
        prop.attribute_data_dict[name] = {"getter": getter,
                                          "setter": setter}

    @classmethod
    def get_attribute_data(cls, attribute: SOMcreator.Attribute) -> dict[str, Any]:
        prop = cls.get_attribute_properties()
        d = dict()
        for name, data_dict in prop.attribute_data_dict.items():
            value = data_dict["getter"](attribute)
            d[name] = value
        return d

    @classmethod
    def set_attribute_data(cls, attribute: SOMcreator, data_dict: dict[str, str | list]):
        prop = cls.get_attribute_properties()
        for name, value in data_dict.items():
            d = prop.attribute_data_dict.get(name)
            if not d:
                logging.warning(f"data {name} not found")
                continue
            d["setter"](value, attribute)

    @classmethod
    def get_attribute_name(cls, attribute: SOMcreator.Attribute):
        return attribute.name

    @classmethod
    def set_attribute_name(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.name = value

    @classmethod
    def get_attribute_data_type(cls, attribute: SOMcreator.Attribute):
        return attribute.data_type

    @classmethod
    def set_attribute_data_type(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.data_type = value

    @classmethod
    def get_attribute_value_type(cls, attribute: SOMcreator.Attribute):
        return attribute.value_type

    @classmethod
    def set_attribute_value_type(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.value_type = value

    @classmethod
    def get_attribute_values(cls, attribute: SOMcreator.Attribute):
        return attribute.value

    @classmethod
    def set_attribute_values(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.value = value

    @classmethod
    def get_attribute_description(cls, attribute: SOMcreator.Attribute):
        return attribute.description

    @classmethod
    def set_attribute_description(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.description = value

    @classmethod
    def is_attribute_optional(cls, attribute: SOMcreator.Attribute):
        return attribute.optional

    @classmethod
    def set_attribute_optional(cls, optional: bool, attribute: SOMcreator.Attribute):
        attribute.optional = optional

    @classmethod
    def get_attribute_properties(cls) -> AttributeProperties:
        return som_gui.AttributeProperties

    @classmethod
    def create_attribute(cls, property_set: SOMcreator.PropertySet, attribute_data: dict[str, str | list | bool]):
        name = attribute_data["name"]
        if not name:
            return
        values = attribute_data["values"]
        value_type = attribute_data["value_type"]
        inherit = attribute_data["inherit_value"]
        attribute = SOMcreator.Attribute(property_set, name, values, value_type, child_inherits_values=inherit)
        cls.set_attribute_data(attribute, attribute_data)
        return attribute
