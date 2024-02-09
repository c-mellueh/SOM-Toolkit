from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import Attribute


def add_basic_attribute_data(attribute_tool: Type[Attribute]):
    attribute_tool.add_attribute_data_value("name", attribute_tool.get_attribute_name,
                                            attribute_tool.set_attribute_name)
    attribute_tool.add_attribute_data_value("data_type", attribute_tool.get_attribute_data_type,
                                            attribute_tool.set_attribute_data_type)
    attribute_tool.add_attribute_data_value("value_type", attribute_tool.get_attribute_value_type,
                                            attribute_tool.set_attribute_value_type)
    attribute_tool.add_attribute_data_value("values", attribute_tool.get_attribute_values,
                                            attribute_tool.set_attribute_values)
    attribute_tool.add_attribute_data_value("description", attribute_tool.get_attribute_description,
                                            attribute_tool.set_attribute_description)
    attribute_tool.add_attribute_data_value("optional", attribute_tool.is_attribute_optional,
                                            attribute_tool.set_attribute_optional)
