from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
import SOMcreator
import ifcopenshell
from datetime import datetime
from PySide6.QtCore import QCoreApplication

GROUP = "Gruppe"
ELEMENT = "Element"

rev_datatype_dict = {
    str:   "IfcText/IfcLabel",
    bool:  "IfcBoolean",
    int:   "IfcInteger",
    float: "IfcReal"
}


def check_file(file: ifcopenshell.file, modelcheck: Type[tool.Modelcheck],
               modelcheck_window: Type[tool.ModelcheckWindow]):
    modelcheck.connect_to_data_base(modelcheck.get_database_path())
    modelcheck.remove_existing_issues(datetime.today())

    modelcheck.build_data_dict(modelcheck_window.get_item_checkstate_dict())

    modelcheck.set_object_checked_count(0)
    modelcheck.set_object_count(modelcheck.get_element_count())
    modelcheck.set_progress(0)

    entities = file.by_type("IfcElement")
    modelcheck.set_object_count(len(entities))
    check_entities(entities, modelcheck)

    for plugin_func in modelcheck.get_file_check_plugins():
        plugin_func(file)

    modelcheck.disconnect_from_data_base()

    modelcheck.set_status(QCoreApplication.translate("Modelcheck", "Modelcheck Done!"))
    modelcheck.set_progress(100)


def check_entities(entities: list[ifcopenshell.entity_instance], modelcheck: Type[tool.Modelcheck]):
    modelcheck.set_status(f'{len(entities)} {QCoreApplication.translate("Modelcheck", "Entities will be checked.")}')
    for entity in entities:
        modelcheck.increment_checked_items()
        if modelcheck.is_aborted():
            return
        check_element(entity, modelcheck)


def check_element(element: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck]):
    modelcheck.set_active_element_type(ELEMENT)
    modelcheck.set_active_element(element)

    data_dict = modelcheck.get_data_dict()
    main_pset_name, main_attribute_name = modelcheck.get_main_pset_name(), modelcheck.get_main_attribute_name()
    main_attribute_value = modelcheck.get_ident_value(element)
    main_attribute_value = "" if main_attribute_value is None else main_attribute_value
    modelcheck.db_create_entity(element, main_attribute_value)

    if not modelcheck.is_pset_existing(element, main_pset_name):
        modelcheck.ident_pset_issue(element.GlobalId, main_pset_name)
        return

    elif not modelcheck.is_attribute_existing(element, main_pset_name, main_attribute_name):
        modelcheck.ident_issue(element.GlobalId, main_pset_name, main_attribute_name)
        return

    obj_rep: SOMcreator.Object = modelcheck.get_ident_dict().get(main_attribute_value)

    if obj_rep is None:
        modelcheck.ident_unknown(element.GlobalId, main_pset_name, main_attribute_name,
                                 main_attribute_value)
        return

    if obj_rep not in data_dict:  # Object Type shouldn't be tested
        return

    for plugin_func in modelcheck.get_entity_check_plugins():
        plugin_func(element)

    modelcheck.check_for_attributes(element, obj_rep)
