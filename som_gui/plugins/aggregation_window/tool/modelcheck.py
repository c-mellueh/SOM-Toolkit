import som_gui.plugins.aggregation_window.core.tool
from som_gui.plugins.aggregation_window.module.modelcheck.prop import AggregationModelcheckProperties
from ifcopenshell import entity_instance
import ifcopenshell

import SOMcreator
from SOMcreator.constants import value_constants
from som_gui import tool
from ifcopenshell.util import element as ifc_el
from som_gui.module.modelcheck.constants import *
from PySide6.QtCore import QCoreApplication
ABBREV_ISSUE = 2


class Modelcheck(som_gui.plugins.aggregation_window.core.tool.Modelcheck):
    @classmethod
    def get_all_groups(cls, file: ifcopenshell.file):
        return file.by_type("IfcGroup")

    @classmethod
    def get_properties(cls) -> AggregationModelcheckProperties:
        return som_gui.AggregationModelcheckProperties

    @classmethod
    def get_parent_entity(cls, entity: ifcopenshell.entity_instance) -> ifcopenshell.entity_instance | None:
        return cls.get_properties().group_parent_dict.get(entity)

    @classmethod
    def subelements_have_doubling_identifier(cls, entity: ifcopenshell):
        """Checks if there are multiple classes of subelements in a Group that have the same Matchkey"""
        sub_idents = [tool.Modelcheck.get_ident_value(sub_group) for sub_group in cls.get_sub_entities(entity)]
        return len(set(sub_idents)) != len(sub_idents)

    @classmethod
    def get_sub_entities(cls, entity: ifcopenshell.entity_instance) -> set[ifcopenshell.entity_instance]:
        group_dict = cls.get_properties().group_dict
        return group_dict.get(entity) if entity in group_dict else set()

    @classmethod
    def build_group_structure(cls, ifc: ifcopenshell.file):
        cls.get_properties().group_dict = dict()
        cls.get_properties().group_parent_dict = dict()

        for entity in cls.get_root_groups(ifc):
            cls.iterate_group_structure(entity)
            cls.set_parent_entity(entity, None)

    @classmethod
    def get_root_groups(cls, ifc: ifcopenshell.file) -> list[ifcopenshell.entity_instance]:
        return [group for group in ifc.by_type("IfcGroup") if cls.is_root_group(group)]

    @classmethod
    def iterate_group_structure(cls, entity: entity_instance):
        relationships = getattr(entity, "IsGroupedBy", [])
        for relationship in relationships:
            sub_entities: set[ifcopenshell.entity_instance] = set(se for se in relationship.RelatedObjects)
            cls.set_sub_entities(entity, sub_entities)
            for sub_entity in sub_entities:  # IfcGroup or IfcElement
                cls.set_parent_entity(sub_entity, entity)
                if sub_entity.is_a("IfcGroup"):
                    cls.iterate_group_structure(sub_entity)

    @classmethod
    def is_root_group(cls, group: entity_instance) -> bool:
        parent_assignment = []
        for assignement in group.HasAssignments:
            if not assignement.is_a("IfcRelAssignsToGroup"):
                continue
            parent_assignment.append(assignement)

        if not parent_assignment:
            return True
        return False

    @classmethod
    def set_sub_entities(cls, entity: ifcopenshell.entity_instance, sub_entities: set[ifcopenshell.entity_instance]):
        cls.get_properties().group_dict[entity] = sub_entities

    @classmethod
    def set_parent_entity(cls, entity: ifcopenshell.entity_instance,
                          parent_entity: ifcopenshell.entity_instance | None):
        cls.get_properties().group_parent_dict[entity] = parent_entity

    @classmethod
    def get_object_representation(cls, entity: ifcopenshell.entity_instance) -> SOMcreator.Object | None:
        return tool.Modelcheck.get_object_representation(entity)

    @classmethod
    def is_parent_allowed(cls, entity: ifcopenshell.entity_instance, parent_entity: ifcopenshell.entity_instance):
        object_rep = cls.get_object_representation(entity)
        parent_object_rep = cls.get_object_representation(parent_entity)
        allowed_parents = cls.get_allowed_parents(object_rep)
        return bool(parent_object_rep.aggregations.intersection(allowed_parents))

    @classmethod
    def get_allowed_parents(cls, obj: SOMcreator.Object):
        def _loop_parent(el: SOMcreator.Aggregation) -> SOMcreator.Aggregation:
            if el.parent_connection != value_constants.INHERITANCE:
                return el.parent
            else:
                return _loop_parent(el.parent)

        return set(_loop_parent(aggreg) for aggreg in obj.aggregations)

    @classmethod
    def get_group_count(cls) -> int:
        return len(cls.get_properties().group_parent_dict)

    @classmethod
    def parent_issue(cls, element: entity_instance, parent_element: entity_instance):
        main_pset_name = tool.Modelcheck.get_main_pset_name()
        main_attribute_name = tool.Modelcheck.get_main_attribute_name()
        element_type = tool.Modelcheck.get_active_element_type()
        ident_value = ifc_el.get_pset(parent_element, main_pset_name, main_attribute_name)

        description = QCoreApplication.translate("Aggregation", "{}: Parent '{}' is not allowed").format(element_type,
                                                                                                         ident_value)
        issue_nr = PARENT_ISSUE
        tool.Modelcheck.add_issues(element.GlobalId, description, issue_nr, None)

    @classmethod
    def empty_group_issue(cls, element):
        description = QCoreApplication.translate("Aggregation", "Group doesn't contain subelements")
        issue_nr = EMPTY_GROUP_ISSUE
        tool.Modelcheck.add_issues(element.GlobalId, description, issue_nr, None)

    @classmethod
    def repetetive_group_issue(cls, element):
        description = QCoreApplication.translate("Aggregation",
                                                 "Group contains multiple Collector Groups with the same Identifier")
        issue_nr = REPETETIVE_GROUP_ISSUE
        tool.Modelcheck.add_issues(element.GlobalId, description, issue_nr, None)

    # GROUP ISSUES
    @classmethod
    def subgroup_issue(cls, child_ident):
        description = QCoreApplication.translate("Aggregation",
                                                 "Collector Group contains wrong subelements ('{}' not allowed)").format(
            child_ident)
        issue_nr = SUBGROUP_ISSUE
        tool.Modelcheck.add_issues(tool.Modelcheck.get_active_guid(), description, issue_nr, None)

    @classmethod
    def no_group_issue(cls, element):
        description = QCoreApplication.translate("Aggregation", "Element without group assertion")
        issue_nr = NO_GROUP_ISSUE
        tool.Modelcheck.add_issues(element.GlobalId, description, issue_nr, None)

    @classmethod
    def entity_is_in_group(cls, entity: ifcopenshell.entity_instance):
        return bool([assignment for assignment in getattr(entity, "HasAssignments", []) if
                     assignment.is_a("IfcRelAssignsToGroup")])
